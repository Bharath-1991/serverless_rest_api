import json
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal


def default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)


def load_response(code, msg):
    out = msg
    if isinstance(msg, list):
        out = {"details":msg}
    return {'statusCode': code,
            'body': json.dumps(out, default=default)}


def lambda_handler(event, context):
    try:
        table_name = os.environ['databaseName']
    except KeyError:
        print('Please input dynamdodb table name')

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    if event['httpMethod'] == 'POST':
        item = json.loads(event['body'])
        table.put_item(Item=item)
        return load_response(200, {'response': 'successfully created new entry'})

    elif event['httpMethod'] == 'GET':
        id = int(event['queryStringParameters'].get('id'))
        response = table.query(KeyConditionExpression=Key('id').eq(id))
        items = response['Items']
        items_count = len(items)
        # if items_count>0:
        #     return load_response(200, items[0])
        # elif items_count >1:
        #     return load_response(200, items[])
        return load_response(200, items)

    elif event['httpMethod'] == 'PUT':
        item = json.loads(event['body'])
        table.update_item(Key={'id': item['id']},
                          UpdateExpression='SET age = :val1,first_name = :val2,last_name = :val3',
                          ExpressionAttributeValues={':val1': item['age'], ':val2': item['first_name'],
                                                     ':val3': item['last_name']})
        return load_response(200, {'response': 'successfully updated the record'})

    elif event['httpMethod'] == 'DELETE':
        id = int(event['queryStringParameters'].get('id'))

        table.delete_item(
            Key={
                'id': id,
                 })
        return load_response(200, {'response': 'successfully deleted the record'})