import json
import boto3
import os
from botocore.exceptions import ClientError

def lambda_handler(event, context):

    try:
        dynamodb = boto3.resource('dynamodb')
        nombre_tabla = os.environ['consultaine']
        tabla = dynamodb.Table(nombre_tabla)
        
        response = tabla.delete_item(
            Key={
                'username_q': event["username"],
                'date_q': event["date"]
            }
        )
            
    except ClientError as e:
        respuesta = {
            "code": e.response['ResponseMetadata']['HTTPStatusCode'],
            "message": e.response['Error']['Message']
        }
    else:
        respuesta = {
            "code": response['ResponseMetadata']['HTTPStatusCode'],
            "message": "Usuario eliminado de forma exitosa",
        }

    return respuesta