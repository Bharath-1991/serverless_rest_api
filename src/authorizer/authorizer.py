import json
import os

import jwt



def lambda_handler(event, context):

    if 'session' in event['methodArn'] and 'POST' in event['methodArn']:
        return generate_policy('test', 'Allow', event['methodArn'])
    whole_auth_token = event.get('authorizationToken')
    if not whole_auth_token:
        raise Exception('Unauthorized')

    print('Client token: ' + whole_auth_token)
    print('Method ARN: ' + event['methodArn'])

    # token_parts = whole_auth_token.split(' ')
    # auth_token = token_parts[1]
    # token_method = token_parts[0]
    #
    # if not (token_method.lower() == 'bearer' and auth_token):
    #     print("Failing due to invalid token_method or missing auth_token")
    #     raise Exception('Unauthorized')

    try:
        # principal_id = jwt_verify(auth_token, AUTH0_CLIENT_PUBLIC_KEY)
        principal_id = jwt_verify(whole_auth_token, 'my-secret')
        policy = generate_policy(principal_id, 'Allow', event['methodArn'])
        return policy
    except Exception as e:
        print(f'Exception encountered: {e}')
        raise Exception('Unauthorized')


def jwt_verify(auth_token, public_key):
    payload = jwt.decode(auth_token, public_key, algorithms=['HS256'])
    return payload


def generate_policy(principal_id, effect, resource):
    return {
        'principalId': 'test-user',
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": resource

                }
            ]
        }
    }


# {'type': 'TOKEN', 'methodArn': 'arn:aws:execute-api:eu-west-1:196526350825:z84jo7br18/ESTestInvoke-stage/GET/', 'authorizationToken': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzb21lIjoicGF5bG9hZCJ9.Joh1R2dYzkRvDkqv3sygm5YyK8Gi4ShZqbhK2gxcs2U'}

# def create_200_response(message):
#     headers = {
#         # Required for CORS support to work
#         'Access-Control-Allow-Origin': '*',
#         # Required for cookies, authorization headers with HTTPS
#         'Access-Control-Allow-Credentials': True,
#     }
#     return create_aws_lambda_response(200, {'message': message}, headers)
#
#
# def create_aws_lambda_response(status_code, message, headers):
#     return {
#         'statusCode': status_code,
#         'headers': headers,
#         'body': json.dumps(message)
#     }