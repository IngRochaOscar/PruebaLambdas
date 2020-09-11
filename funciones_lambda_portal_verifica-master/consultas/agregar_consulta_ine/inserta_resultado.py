import json
import boto3
import os
from botocore.exceptions import ClientError

def insert_resumen(comparacion):

    try:
        dynamodb = boto3.resource('dynamodb')
        nombre_tabla = os.environ['consultaVer']
        tabla = dynamodb.Table(nombre_tabla)
        
        response = tabla.put_item(
            Item=comparacion
        )
            
    except ClientError as e:
        respuesta = {
            "code": e.response['ResponseMetadata']['HTTPStatusCode'],
            "message": e.response['Error']['Message']
        }
    else:
        respuesta = {
                "code": response['ResponseMetadata']['HTTPStatusCode'],
                "message": "Registro insertado de forma exitosa"
        }

    return respuesta
