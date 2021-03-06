import json
import boto3
import os
import uuid
import calendar
import time
import base64
from datetime import datetime
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
from jwt.__init__ import PyJWT
from validaciones import valida_json_entrada

def lambda_handler(request, context):
    try:
        event = request["body"]
        headers = request["headers"]

        rand_id = uuid.uuid4()
        ts = str(calendar.timegm(time.gmtime()))
        dynamodb = boto3.resource('dynamodb')
        nombre_tabla = os.environ['usuarios']
        tabla = dynamodb.Table(nombre_tabla)

        if 'Authorization' in headers and len(headers["Authorization"]) != 0:
            
            #se validan los parametros de entrada
            validacion = valida_json_entrada(event)
            
            if validacion:
                # Se obtiene el mail del admin
                tid = headers["Authorization"]
                payload, _, _, _ = PyJWT._load(PyJWT, tid)
                # se transforma la cadena a json
                tid_json = json.loads(payload);
                event["username_admin"] = tid_json["email"]

                # se verifica si el payload tiene el grupo
                if 'cognito:groups' in tid_json and len(tid_json["cognito:groups"][0]) != 0 and (
                    "PortalAdminRoot" in tid_json["cognito:groups"][0] or "PortalAdmin" in tid_json["cognito:groups"][0]):

                    #se establecen los roles de acceso
                    accesos_base = "PortalAdminRoot,PortalAdmin"+event["entidad"]

                    response = tabla.put_item(
                        Item={
                            'id_usuario': event["id_usuario"],
                            'username_admin': event["username_admin"],
                            'date': event["date"],
                            'date_region': ts,
                            'entidad': event["entidad"],
                            'rol': event["rol"],
                            'grupo_cognito': event["grupoCognito"],
                            'usuario_cognito': event["usuarioCognito"],
                            'nombres': event["nombres"],
                            'apellidoPat': event["apellidoPat"],
                            'apellidoMat': event["apellidoMat"],
                            'sexo': event["sexo"],
                            'rfc': event["rfc"],
                            'acceso_rol': accesos_base
                        }
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
                    "message": "Algunos de los datos enviados son inválidos o no se encuentran en el formato establecido, por favor reviselos y vuelva a intentar"
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
            "message": "Ocurrio un problema el intentar insertar la información : ErrorType: " + str(e)
        }
    else:
        respuesta = {
            "code": response['ResponseMetadata']['HTTPStatusCode'],
            "message": "Registro insertado de forma exitosa"
        }

    return respuesta