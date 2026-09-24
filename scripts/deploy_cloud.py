"""Package and deploy the shared bot. Receipts and secrets stay in research/hosting.

Run without --apply to prepare and check bundles. --apply creates or updates
AWS resources. The bootstrap bucket is retained separately from the stack.
"""
import argparse
import hashlib
import json
from pathlib import Path
import secrets
import shutil
import zipfile

from backup_private import AWS, ROOT, load_env
from cloud_stack import template

WORK = ROOT / 'research/hosting'
MODULES = ('cloud_bot.py', 'research_answer.py', 'knowledge_corpus.py', 'fast_search.py',
           'model_costs.py', 'jev_triage.py', 'answer_writer.py', 'backup_private.py')
ASSETS = ('index.html', 'app.js', 'style.css', 'evidence.mjs', 'bot-client.mjs', 'case-examples.mjs', 'answer-design.mjs', 'file-input.mjs')


def private_json(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n')
    path.chmod(0o600)


def prepare():
    WORK.mkdir(parents=True, exist_ok=True, mode=0o700)
    from case_designs import validate_public_catalog
    validate_public_catalog(json.loads((ROOT/'docs/bot-cases.json').read_text()),
                            json.loads((ROOT/'docs/case-designs.json').read_text()))
    values = load_env(ROOT / '.env.local')
    private_values = [v.encode() for v in values.values() if len(v) >= 8]
    docs = sorted(p for p in (ROOT/'docs').rglob('*') if p.suffix in ('.md', '.json') and p.is_file())
    inputs = [*(ROOT/'scripts'/name for name in MODULES), ROOT/'infra/lambda_function.py',
              *(ROOT/'web'/name for name in ASSETS), *docs]
    for path in inputs:
        if path.is_symlink() or any(v in path.read_bytes() for v in private_values):
            raise ValueError('Unsafe deployment input: '+str(path.relative_to(ROOT)))
    archive = WORK/'worker.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as bundle:
        for name in MODULES:
            bundle.write(ROOT/'scripts'/name, 'scripts/'+name)
        bundle.write(ROOT/'infra/lambda_function.py', 'lambda_function.py')
        for path in docs:
            bundle.write(path, path.relative_to(ROOT).as_posix())
    site = WORK/'site'
    site.mkdir(exist_ok=True)
    for name in ASSETS:
        shutil.copy2(ROOT/'web'/name, site/name)
    # Build an exact allowlisted asset tree; no private directories are copied.
    if (site/'docs').exists():
        shutil.rmtree(site/'docs')
    for path in docs:
        target = site/path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    private_json(WORK/'template.json', template())
    return archive, site, values


def deploy(daily_limit=None, max_concurrent=None):
    archive, site, values = prepare()
    if not values.get('jev_api_key'):
        raise ValueError('Missing Jev key in .env.local.')
    aws = AWS('us-east-1')
    owner = aws.call('sts', 'get-caller-identity')['Account']
    receipt = WORK/'deployment.json'
    if receipt.exists():
        config = json.loads(receipt.read_text())
        if config['account'] != owner:
            raise ValueError('Deployment receipt belongs to another account.')
    else:
        config = {'account': owner, 'region': 'us-east-1', 'stack': 'jev-bot-hosted',
                  'bucket': 'jev-bot-hosted-'+secrets.token_hex(10), 'bucket_created': False}
        private_json(receipt, config)
    capacity = config.setdefault('capacity', {'daily_limit': 5000, 'max_concurrent': 10})
    if daily_limit is not None: capacity['daily_limit'] = daily_limit
    if max_concurrent is not None: capacity['max_concurrent'] = max_concurrent
    if not 1 <= capacity['daily_limit'] <= 100000 or not 1 <= capacity['max_concurrent'] <= 50:
        raise ValueError('Invalid daily or simultaneous answer limit.')
    bucket = config['bucket']
    if not config.get('bucket_created'):
        aws.call('s3api', 'create-bucket', '--bucket', bucket, '--object-ownership', 'BucketOwnerEnforced')
        config['bucket_created'] = True
        private_json(receipt, config)
    aws.call('s3api', 'put-public-access-block', '--bucket', bucket, '--public-access-block-configuration',
             'BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true')
    aws.call('s3api', 'put-bucket-encryption', '--bucket', bucket, '--server-side-encryption-configuration',
             json.dumps({'Rules': [{'ApplyServerSideEncryptionByDefault': {'SSEAlgorithm': 'AES256'}}]}))
    aws.call('s3api', 'put-bucket-lifecycle-configuration', '--bucket', bucket, '--lifecycle-configuration',
             json.dumps({'Rules': [{'ID': 'ExpireJobResults', 'Status': 'Enabled', 'Filter': {'Prefix': 'jobs/'},
                                    'Expiration': {'Days': 1}},
                                   {'ID': 'ExpireReusedAnswers', 'Status': 'Enabled', 'Filter': {'Prefix': 'cache/'},
                                    'Expiration': {'Days': 7}}]}))
    key = 'deploy/'+hashlib.sha256(archive.read_bytes()).hexdigest()+'.zip'
    aws.call('s3api', 'put-object', '--bucket', bucket, '--key', key, '--body', str(archive), '--server-side-encryption', 'AES256')
    # CLI sync prints only public asset paths; subprocess output remains captured.
    import subprocess
    result = subprocess.run(['aws', 's3', 'sync', str(site), 's3://'+bucket+'/site/', '--region', aws.region,
                             '--cache-control', 'public,max-age=300', '--only-show-errors'],
                            env=aws.env, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError('Static asset upload failed; inspect AWS S3 permissions.')
    params = {'Bucket': bucket, 'CodeKey': key, 'JevKey': values['jev_api_key'], 'GlmKey': values.get('glm_key', ''),
              'WriterAvailable': str(bool(values.get('glm_key'))).lower(),
              'DailyLimit': str(capacity['daily_limit']), 'MaxConcurrent': str(capacity['max_concurrent'])}
    parameter_path = WORK/'parameters.json'
    private_json(parameter_path, [{'ParameterKey': k, 'ParameterValue': v} for k, v in params.items()])
    try:
        aws.call('cloudformation', 'validate-template', '--template-body', 'file://'+str(WORK/'template.json'))
        stacks = aws.call('cloudformation', 'list-stacks')['StackSummaries']
        previous = next((s for s in stacks if s['StackName'] == config['stack'] and s['StackStatus'] != 'DELETE_COMPLETE'), None)
        action = 'update-stack' if previous else 'create-stack'
        args = ['--stack-name', config['stack'], '--template-body', 'file://'+str(WORK/'template.json'),
                '--parameters', 'file://'+str(parameter_path), '--capabilities', 'CAPABILITY_IAM']
        if not previous:
            args += ['--disable-rollback']
        elif previous['StackStatus'] in ('CREATE_FAILED', 'UPDATE_FAILED'):
            args += ['--disable-rollback']
        try:
            response = aws.call('cloudformation', action, *args)
            config['stack_id'] = response['StackId']
            private_json(receipt, config)
        except RuntimeError as exc:
            if 'No updates are to be performed' not in str(exc):
                raise
        print('Deployment submitted. Poll stack events; then verify HTTPS and an answer job.', flush=True)
    finally:
        parameter_path.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--daily-limit', type=int, help='Shared answer starts per UTC day; preserved across later deploys.')
    parser.add_argument('--max-concurrent', type=int, help='Simultaneous answer slots; preserved across later deploys.')
    args = parser.parse_args()
    if args.apply:
        deploy(args.daily_limit, args.max_concurrent)
    else:
        archive, site, _ = prepare()
        print(f'Bundle checked: {archive.stat().st_size} bytes; {sum(p.is_file() for p in site.rglob("*"))} public assets.')


if __name__ == '__main__':
    main()
