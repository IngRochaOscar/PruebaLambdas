import json
import boto3
import os
import base64
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from jwt.__init__ import PyJWT

def lambda_handler(event, context):

    try:
        dynamodb = boto3.resource('dynamodb')
        nombre_tabla_resp = os.environ['consultaVer']
        tabla_resp = dynamodb.Table(nombre_tabla_resp)
        
        if 'Authorization' in event["headers"] and len(event["headers"]["Authorization"]) != 0:
            
            #decoding payload
            tid = event["headers"]["Authorization"]
            payload, _, _, _ = PyJWT._load(PyJWT,tid)
            #se transforma la cadena a json
            tid_json = json.loads(payload);
            
            #se verifica si el payload tiene el grupo
            if 'cognito:groups' in tid_json and len(tid_json["cognito:groups"][0]) != 0 and ("PortalAdminRoot" in tid_json["cognito:groups"][0] or "PortalAdmin" in tid_json["cognito:groups"][0] or "PortalConsulta" in tid_json["cognito:groups"][0] or "PortalReportes" in tid_json["cognito:groups"][0]):
                
                event["grupoCognito"] = tid_json["cognito:groups"][0]
                event["username"] = tid_json["email"]
                
                #se verifica si el grupo es de consulta
                if "PortalConsulta" in event["grupoCognito"]:
                    if 'username' in event and len(event["username"]) != 0:
                        response = tabla_resp.scan(
                            FilterExpression=Attr("acceso_rol").contains(event["grupoCognito"]) & Attr("username").eq(event["username"])
                        ) 
                    else:
                        respuesta = {
                            "code": 400,
                            "message": "Es necesario capturar el usuario de la consulta"
                        }
        
                        return respuesta
                elif "PortalAdminRoot" in event["grupoCognito"]:
                    
                    if 'idEntidad' in event and len(event["idEntidad"]) != 0:
                        response = tabla_resp.query(
                            KeyConditionExpression=Key("idEntidad").eq(event["idEntidad"])
                        )
                    else:
                        response = tabla_resp.scan()
                    
                else:
                    response = tabla_resp.scan(
                        FilterExpression=Attr("acceso_rol").contains(event["grupoCognito"])
                    ) 
                
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
            "message": "Ocurrio un problema el intentar recuperar la información : ErrorType: " + str(e)
        }
    else:
        respuesta = {
            "code": response['ResponseMetadata']['HTTPStatusCode'],
            "message": "Usuario recuperado de forma exitosa",
            "response": response["Items"]
        }

    return respuesta
