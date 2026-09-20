"""CloudFormation template for the small shared CloudFront deployment."""
def ref(name):
    return {'Ref': name}


def sub(value):
    return {'Fn::Sub': value}


def attr(name, field):
    return {'Fn::GetAtt': [name, field]}


def template():
    resources = {}
    def add(name, kind, **properties):
        resources[name] = {'Type': 'AWS::'+kind, 'Properties': properties}
    add('Jobs', 'DynamoDB::Table', BillingMode='PAY_PER_REQUEST',
        AttributeDefinitions=[{'AttributeName': 'pk', 'AttributeType': 'S'}],
        KeySchema=[{'AttributeName': 'pk', 'KeyType': 'HASH'}],
        TimeToLiveSpecification={'AttributeName': 'ttl', 'Enabled': True})
    trust = {'Version': '2012-10-17', 'Statement': [{'Effect': 'Allow',
             'Principal': {'Service': 'lambda.amazonaws.com'}, 'Action': 'sts:AssumeRole'}]}
    for name in ('Api', 'Worker'):
        logname = sub('/aws/lambda/${AWS::StackName}-'+name.lower())
        add(name+'Logs', 'Logs::LogGroup', LogGroupName=logname, RetentionInDays=30 if name == 'Api' else 7)
        resources[name+'Logs'].update(DeletionPolicy='Retain', UpdateReplacePolicy='Retain')
        policy = [
            {'Effect': 'Allow', 'Action': ['logs:CreateLogStream', 'logs:PutLogEvents'], 'Resource': attr(name+'Logs', 'Arn')},
            {'Effect': 'Allow', 'Action': ['dynamodb:GetItem', 'dynamodb:PutItem', 'dynamodb:UpdateItem', 'dynamodb:DeleteItem'], 'Resource': attr('Jobs', 'Arn')},
            {'Effect': 'Allow', 'Action': ['s3:GetObject'] if name == 'Api' else ['s3:PutObject'],
             'Resource': sub('arn:${AWS::Partition}:s3:::${Bucket}/jobs/*')}]
        if name == 'Api':
            policy.append({'Effect': 'Allow', 'Action': 'lambda:InvokeFunction', 'Resource': attr('Worker', 'Arn')})
        add(name+'Role', 'IAM::Role', AssumeRolePolicyDocument=trust,
            Policies=[{'PolicyName': 'Application', 'PolicyDocument': {'Version': '2012-10-17', 'Statement': policy}}])
        env = {'TABLE': ref('Jobs'), 'BUCKET': ref('Bucket')}
        if name == 'Worker':
            env.update(jev_api_key=ref('JevKey'), glm_key=ref('GlmKey'))
        else:
            env.update(WORKER=ref('Worker'), JEV_AVAILABLE='true',
                       WRITER_AVAILABLE=ref('WriterAvailable'), DAILY_LIMIT=ref('DailyLimit'), MAX_CONCURRENT=ref('MaxConcurrent'))
        add(name, 'Lambda::Function', FunctionName=sub('${AWS::StackName}-'+name.lower()),
            Runtime='python3.12', Handler='lambda_function.'+('api' if name == 'Api' else 'worker'),
            Role=attr(name+'Role', 'Arn'), Code={'S3Bucket': ref('Bucket'), 'S3Key': ref('CodeKey')},
            MemorySize=256 if name == 'Api' else 512, Timeout=25 if name == 'Api' else 900,
            Environment={'Variables': env})
        resources[name]['DependsOn'] = name+'Logs'
    add('AsyncPolicy', 'Lambda::EventInvokeConfig', FunctionName=ref('Worker'), Qualifier='$LATEST',
        MaximumRetryAttempts=0, MaximumEventAgeInSeconds=60)
    add('HttpApi', 'ApiGatewayV2::Api', Name=sub('${AWS::StackName}-api'), ProtocolType='HTTP')
    add('Integration', 'ApiGatewayV2::Integration', ApiId=ref('HttpApi'), IntegrationType='AWS_PROXY',
        IntegrationUri=attr('Api', 'Arn'), PayloadFormatVersion='2.0', TimeoutInMillis=29000)
    for name, route in [('ConfigRoute', 'GET /api/config'), ('CreateRoute', 'POST /api/jobs'), ('JobRoute', 'GET /api/jobs/{id}'), ('FeedbackRoute', 'POST /api/feedback')]:
        add(name, 'ApiGatewayV2::Route', ApiId=ref('HttpApi'), RouteKey=route, Target=sub('integrations/${Integration}'))
    add('Stage', 'ApiGatewayV2::Stage', ApiId=ref('HttpApi'), StageName='$default', AutoDeploy=True,
        DefaultRouteSettings={'ThrottlingBurstLimit': 40, 'ThrottlingRateLimit': 20})
    add('InvokePermission', 'Lambda::Permission', Action='lambda:InvokeFunction', FunctionName=ref('Api'),
        Principal='apigateway.amazonaws.com', SourceArn=sub('arn:${AWS::Partition}:execute-api:${AWS::Region}:${AWS::AccountId}:${HttpApi}/*'))
    add('OAC', 'CloudFront::OriginAccessControl', OriginAccessControlConfig={
        'Name': sub('${AWS::StackName}-s3'), 'OriginAccessControlOriginType': 's3', 'SigningBehavior': 'always', 'SigningProtocol': 'sigv4'})
    add('StaticCache', 'CloudFront::CachePolicy', CachePolicyConfig={
        'Name': sub('${AWS::StackName}-static'), 'DefaultTTL': 300, 'MinTTL': 0, 'MaxTTL': 86400,
        'ParametersInCacheKeyAndForwardedToOrigin': {'EnableAcceptEncodingGzip': True, 'EnableAcceptEncodingBrotli': True,
        'HeadersConfig': {'HeaderBehavior': 'none'}, 'CookiesConfig': {'CookieBehavior': 'none'}, 'QueryStringsConfig': {'QueryStringBehavior': 'none'}}})
    # Forward viewer headers except Host to API Gateway; never cache API responses.
    add('ApiCache', 'CloudFront::CachePolicy', CachePolicyConfig={
        'Name': sub('${AWS::StackName}-api'), 'DefaultTTL': 0, 'MinTTL': 0, 'MaxTTL': 0,
        'ParametersInCacheKeyAndForwardedToOrigin': {'EnableAcceptEncodingGzip': False,
        'HeadersConfig': {'HeaderBehavior': 'none'},
        'CookiesConfig': {'CookieBehavior': 'none'}, 'QueryStringsConfig': {'QueryStringBehavior': 'none'}}})
    add('ApiOriginRequest', 'CloudFront::OriginRequestPolicy', OriginRequestPolicyConfig={
        'Name': sub('${AWS::StackName}-api-origin'), 'HeadersConfig': {'HeaderBehavior': 'allExcept', 'Headers': ['Host']},
        'CookiesConfig': {'CookieBehavior': 'none'}, 'QueryStringsConfig': {'QueryStringBehavior': 'none'}})
    add('Headers', 'CloudFront::ResponseHeadersPolicy', ResponseHeadersPolicyConfig={
        'Name': sub('${AWS::StackName}-headers'), 'SecurityHeadersConfig': {
            'ContentTypeOptions': {'Override': True}, 'FrameOptions': {'FrameOption': 'DENY', 'Override': True},
            'ReferrerPolicy': {'ReferrerPolicy': 'no-referrer', 'Override': True},
            'StrictTransportSecurity': {'AccessControlMaxAgeSec': 31536000, 'Override': True},
            'ContentSecurityPolicy': {'ContentSecurityPolicy': "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'", 'Override': True}}})
    common = {'ViewerProtocolPolicy': 'redirect-to-https', 'ResponseHeadersPolicyId': ref('Headers')}
    add('Distribution', 'CloudFront::Distribution', DistributionConfig={
        'Enabled': True, 'Comment': 'Jev bot shared research assistant', 'DefaultRootObject': 'index.html',
        'HttpVersion': 'http2and3', 'IPV6Enabled': True, 'PriceClass': 'PriceClass_100',
        'ViewerCertificate': {'CloudFrontDefaultCertificate': True},
        'Origins': [
            {'Id': 'site', 'DomainName': sub('${Bucket}.s3.${AWS::Region}.amazonaws.com'), 'OriginPath': '/site',
             'S3OriginConfig': {'OriginAccessIdentity': ''}, 'OriginAccessControlId': ref('OAC')},
            {'Id': 'api', 'DomainName': sub('${HttpApi}.execute-api.${AWS::Region}.amazonaws.com'),
             'CustomOriginConfig': {'OriginProtocolPolicy': 'https-only', 'OriginSSLProtocols': ['TLSv1.2']}}],
        'DefaultCacheBehavior': {**common, 'TargetOriginId': 'site', 'CachePolicyId': ref('StaticCache'),
                                 'Compress': True, 'AllowedMethods': ['GET', 'HEAD']},
        'CacheBehaviors': [{**common, 'PathPattern': '/api/*', 'TargetOriginId': 'api', 'CachePolicyId': ref('ApiCache'), 'OriginRequestPolicyId': ref('ApiOriginRequest'),
                           'AllowedMethods': ['GET', 'HEAD', 'OPTIONS', 'PUT', 'POST', 'PATCH', 'DELETE'], 'CachedMethods': ['GET', 'HEAD']}]
    })
    add('BucketPolicy', 'S3::BucketPolicy', Bucket=ref('Bucket'), PolicyDocument={'Version': '2012-10-17', 'Statement': [
        {'Effect': 'Allow', 'Principal': {'Service': 'cloudfront.amazonaws.com'}, 'Action': 's3:GetObject',
         'Resource': sub('arn:${AWS::Partition}:s3:::${Bucket}/site/*'), 'Condition': {'StringEquals': {
             'AWS:SourceArn': sub('arn:${AWS::Partition}:cloudfront::${AWS::AccountId}:distribution/${Distribution}')}}},
        {'Effect': 'Deny', 'Principal': '*', 'Action': 's3:*',
         'Resource': [sub('arn:${AWS::Partition}:s3:::${Bucket}'), sub('arn:${AWS::Partition}:s3:::${Bucket}/*')],
         'Condition': {'Bool': {'aws:SecureTransport': 'false'}}}]})
    parameters = {name: {'Type': 'String'} for name in ['Bucket', 'CodeKey', 'WriterAvailable']}
    parameters.update({'DailyLimit': {'Type': 'Number', 'Default': 5000, 'MinValue': 1, 'MaxValue': 100000},
                       'MaxConcurrent': {'Type': 'Number', 'Default': 10, 'MinValue': 1, 'MaxValue': 50}})
    parameters.update({name: {'Type': 'String', 'NoEcho': True} for name in ['JevKey', 'GlmKey']})
    return {'AWSTemplateFormatVersion': '2010-09-09', 'Description': 'Private S3, CloudFront and asynchronous Jev research backend',
            'Parameters': parameters, 'Resources': resources, 'Outputs': {
                'URL': {'Value': sub('https://${Distribution.DomainName}')},
                'DistributionId': {'Value': ref('Distribution')}, 'Worker': {'Value': ref('Worker')},
                'Api': {'Value': ref('Api')}, 'JobsTable': {'Value': ref('Jobs')}}}
