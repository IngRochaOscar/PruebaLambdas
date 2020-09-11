import json
import boto3
import os
import base64
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from jwt.__init__ import PyJWT

def lambda_handler(event, context):
    
    try:
        dynamodb = boto3.resource('dynamodb')
        nombre_tabla = os.environ['planesine']
        tabla = dynamodb.Table(nombre_tabla)
        
        if 'Authorization' in event["headers"] and len(event["headers"]["Authorization"]) != 0:
            
            #decoding payload
            tid = event["headers"]["Authorization"]
            payload, _, _, _ = PyJWT._load(PyJWT,tid)
            #se transforma la cadena a json
            tid_json = json.loads(payload);
            
            #se verifica si el payload tiene el grupo
            if 'cognito:groups' in tid_json and len(tid_json["cognito:groups"][0]) != 0 and ("PortalAdminRoot" in tid_json["cognito:groups"][0] or "PortalAdmin" in tid_json["cognito:groups"][0]):
                response = tabla.scan()
            else:
                respuesta = {
                    "code": 400,
                    "message": "No se cuenta con los permisos requeridos, consulte a su administrador"
                }
                
                return respuesta
        else:
            respuesta = {
                "code": 400,
                "message": "Acceso no valido"
            }
            
            return respuesta
            
    except ClientError as e:
        respuesta = {
            "code": e.response['ResponseMetadata']['HTTPStatusCode'],
            "message": e.response['Error']['Message']
        }
    except Exception as e:
        respuesta = {
            "code": 400,
            "message": "Ocurrio un problema al intentar obtener la información : ErrorType: " + str(e)
        }
    else:
        respuesta = {
            "code": response['ResponseMetadata']['HTTPStatusCode'],
            "message": "Información recuperada de forma exitosa",
            "response": response["Items"]
        }

    return respuesta
