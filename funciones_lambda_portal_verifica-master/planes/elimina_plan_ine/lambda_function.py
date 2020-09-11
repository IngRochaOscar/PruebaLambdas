import json
import boto3
import os
import base64
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
            if 'cognito:groups' in tid_json and len(tid_json["cognito:groups"][0]) != 0 and "PortalAdminRoot" in tid_json["cognito:groups"][0]:
                
                #se verifica que el id del plan no sea una cadena vacia
                if 'id_plan' in event and len(event['id_plan']) != 0:
                    response = tabla.delete_item(
                        Key={
                            'id_plan': event["id_plan"]
                        }
                    )    
                else:
                    respuesta = {
                        "code": 400,
                        "message": "No se cuenta con los datos necesarios para realizar la operación"
                    }
                    return respuesta
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
            "message": "Ocurrio un problema el intentar eliminar la información : ErrorType: " + str(e)
        }
    else:
        respuesta = {
            "code": response['ResponseMetadata']['HTTPStatusCode'],
            "message": "Plan eliminado de forma exitosa"
        }

    return respuesta