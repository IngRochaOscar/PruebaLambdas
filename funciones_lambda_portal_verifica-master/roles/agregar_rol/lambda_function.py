import json
import boto3
import os
import uuid
from boto3.dynamodb.conditions import  Attr
from botocore.exceptions import ClientError

def lambda_handler(event, context):

    try:
        rand_id = uuid.uuid4()
        dynamodb = boto3.resource('dynamodb')
        nombre_tabla = os.environ['roles_verifica']
        tabla = dynamodb.Table(nombre_tabla)
        
        
        #se verifica si se trata de un registro nuevo o actualizacion
        if 'id_rol' in event and len(event["id_rol"]) != 0:
            
            #se trata de una actualización del registro
            response = tabla.put_item(
                Item={
                    'id_rol': event["id_rol"],
                    'username': event["username"],
                    'nombre_rol': event["nombre_rol"],
                    'date': event["date"],
                    'descripcion': event["descripcion"],
                    'grupo_cognito': event["grupo_cognito"],
                    'acceso_rol': event["acceso_rol"]
                }
            )
            
        #se trata de una inseración nueva        
        else:
            
            #se valida si hay una descripcion similar en los registros 
            consulta = tabla.scan(
                        FilterExpression=Attr("nombre_rol").eq(event["nombre_rol"])
                    )
        
            if len(consulta['Items']) == 0:
                response = tabla.put_item(
                    Item={
                        'id_rol': str(rand_id) + event["username"],
                        'username': event["username"],
                        'nombre_rol': event["nombre_rol"],
                        'date': event["date"],
                        'descripcion': event["descripcion"],
                        'grupo_cognito': event["grupo_cognito"],
                        'acceso_rol': event["acceso_rol"]
                    }
                )
            else:
                respuesta = {
                    "code": 201,
                    "message": "Existen registros que podrían contener la misma información, favor de validar"
                }
                return respuesta
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