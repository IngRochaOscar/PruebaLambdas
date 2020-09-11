import json
import boto3
import os
import uuid
import base64
from boto3.dynamodb.conditions import  Attr
from botocore.exceptions import ClientError
from jwt.__init__ import PyJWT
from validaciones import valida_json_entrada

def lambda_handler(request, context):

    try:
        event = request["body"]
        headers = request["headers"]
        rand_id = uuid.uuid4()
        dynamodb = boto3.resource('dynamodb')
        nombre_tabla = os.environ['planesine']
        tabla = dynamodb.Table(nombre_tabla)
        
        if 'Authorization' in headers and len(headers["Authorization"]) != 0:
            
            #se validan los parametros de entrada
            validacion = valida_json_entrada(event)
            
            if validacion:
            
                #decoding payload
                tid = headers["Authorization"]
                payload, _, _, _ = PyJWT._load(PyJWT,tid)
                #se transforma la cadena a json
                tid_json = json.loads(payload);
                username_admin = tid_json["email"]
            
                #se verifica si el payload tiene el grupo
                if 'cognito:groups' in tid_json and len(tid_json["cognito:groups"][0]) != 0 and "PortalAdminRoot" in tid_json["cognito:groups"][0]:
                    
                    #se verifica si se trata de un registro nuevo o actualizacion
                    if "id_plan" in event:
            
                        #se trata de una actualización del registro
                        response = tabla.put_item(
                            Item={
                                'id_plan': event["id_plan"],
                                'date': event["date"],
                                'descripcion': event["descripcion"],
                                'solMaxMes': event["solMaxMes"],
                                'solMaxMin': event["solMaxMin"],
                                'costoMensual': event["costoMensual"],
                                'costoAnual': event["costoAnual"],
                                'username_admin': username_admin
                            }
                        )
            
                    #se trata de una inseración nueva        
                    else:
                    
                        #se valida si hay una descripcion similar en los registros 
                        consulta = tabla.scan(
                            FilterExpression=Attr("descripcion").eq(event["descripcion"])
                        )
        
                        if len(consulta['Items']) == 0:
                            response = tabla.put_item(
                                Item={
                                'id_plan': str(rand_id) + event["date"],
                                'date': event["date"],
                                'descripcion': event["descripcion"],
                                'solMaxMes': event["solMaxMes"],
                                'solMaxMin': event["solMaxMin"],
                                'costoMensual': event["costoMensual"],
                                'costoAnual': event["costoAnual"],
                                'username_admin': username_admin
                                }
                            )
                        else:
                            respuesta = {
                                "code": 201,
                                "message": "Existen registros que podrían contener la misma información, favor de validar"
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