"""Show deployment status and save public stack outputs in the private receipt."""
import json
from backup_private import AWS, ROOT
from deploy_cloud import private_json


def main():
    path = ROOT/'research/hosting/deployment.json'
    config = json.loads(path.read_text())
    aws = AWS(config['region'])
    stack = aws.call('cloudformation', 'describe-stacks', '--stack-name', config['stack'])['Stacks'][0]
    print('Stack:', stack['StackStatus'])
    resources = aws.call('cloudformation', 'list-stack-resources', '--stack-name', config['stack'])['StackResourceSummaries']
    print('Resources:', ', '.join(f"{r['LogicalResourceId']}={r['ResourceStatus']}" for r in resources))
    if 'FAILED' in stack['StackStatus']:
        for event in aws.call('cloudformation', 'describe-stack-events', '--stack-name', config['stack'])['StackEvents']:
            if 'FAILED' in event['ResourceStatus']:
                print(event['LogicalResourceId'], event.get('ResourceStatusReason', ''))
    outputs = {row['OutputKey']: row['OutputValue'] for row in stack.get('Outputs', [])}
    if outputs:
        config.update(outputs=outputs, status=stack['StackStatus'])
        private_json(path, config)
        print('URL:', outputs['URL'])


if __name__ == '__main__':
    main()
