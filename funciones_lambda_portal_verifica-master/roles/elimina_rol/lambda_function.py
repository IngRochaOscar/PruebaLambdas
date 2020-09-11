import json
import boto3
import os
from botocore.exceptions import ClientError

def lambda_handler(event, context):

    try:
        dynamodb = boto3.resource('dynamodb')
        nombre_tabla = os.environ['roles_verifica']
        tabla = dynamodb.Table(nombre_tabla)
        
        response = tabla.delete_item(
            Key={
                'id_rol': event["id_rol"]
            }
        )
            
    except ClientError as e:
        respuesta = {
            "code": e.response['ResponseMetadata']['HTTPStatusCode'],
            "message": e.response['Error']['Message']
        }
    except Exception as e:
        respuesta = {
            "code": 400,
            "message": "Ocurrio un problema el intentar eliminar la información : ErrorType: " + str(e)
        }
    else:
        respuesta = {
            "code": response['ResponseMetadata']['HTTPStatusCode'],
            "message": "Rol eliminado de forma exitosa",
        }

    return respuesta