# import jwt
#
# def generate_session_token():
#     try:
#         secret_key = 'my-secret'
#         body = {"user_id":"test-user",
#                 "password":"test123"}
#
#         encoded_jwt = jwt.encode(body, secret_key, algorithm='HS256')
#
#         return str(encoded_jwt)
#
#     except Exception as ex:
#         print(ex)
#
# print(generate_session_token())


import jwt
import json

def lambda_handler(event,context):
    try:
        secret_key = event.get('headers').get('jwt_secret')
        body = json.loads(event['body'])

        encoded_jwt = jwt.encode(body, secret_key, algorithm='HS256')
        res = {'token':str(encoded_jwt)}

        return {'statusCode': 200,
            'body': json.dumps(res)}
    except Exception as ex:
        return {'statusCode': 500,
                'body': json.dumps({"res":str(ex)})}