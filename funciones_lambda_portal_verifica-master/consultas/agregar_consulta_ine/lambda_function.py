import json
import boto3
import os
import uuid
import time
import calendar
import base64
from botocore.exceptions import ClientError
from inserta_cons_ver import insert_ver_cons
from inserta_resp_ver import insert_ver_resp
from compara_resp import compara_respuesta
from inserta_resultado import insert_resumen
from jwt.__init__ import PyJWT
from validaciones import valida_json_entrada

def lambda_handler(request, context):
    event = request["body"]
    headers = request["headers"]
    rand_id = uuid.uuid4();
    
    if 'Authorization' in headers and len(headers["Authorization"]) != 0:
            
        #decoding payload
        tid = headers["Authorization"]
        payload, _, _, _ = PyJWT._load(PyJWT,tid)
        #se transforma la cadena a json
        tid_json = json.loads(payload);
        
        #se verifica si el payload tiene el grupo
        if 'cognito:groups' in tid_json and len(tid_json["cognito:groups"][0]) != 0 and "PortalAdminRoot" not in tid_json["cognito:groups"][0] and ("PortalAdmin" in tid_json["cognito:groups"][0] or "PortalConsulta" in tid_json["cognito:groups"][0]):
            
            grupo_cognito = tid_json["cognito:groups"][0]
            event["grupoCognito"] = grupo_cognito
            event["username"] = tid_json["email"]
            
            #se extrae el RFC de la entidad del grupo
            if "PortalAdmin" in tid_json["cognito:groups"][0]:
                entidad = grupo_cognito.replace("PortalAdmin","")
            if "PortalConsulta" in tid_json["cognito:groups"][0]:
                entidad = grupo_cognito.replace("PortalConsulta","")
                
            event["idEntidad"] = entidad
            id_consulta = str(rand_id)+event["username"]+entidad    
        
        else:
            respuesta = {
                "code": 400,
                "message": "El usuario no puede realizar consultas"
            }
        
            return respuesta
    else:
        respuesta = {
            "code": 400,
            "message": "Acceso no valido"
        }
            
        return respuesta

    #se validan los parametros de entrada
    validacion = valida_json_entrada(event)
    
    if validacion:
        result =main(id_consulta, event, context)    
    else:
        result = {
            "code": 400,
            "message": "Algunos de los datos enviados son inválidos o no se encuentran en el formato establecido, por favor reviselos y vuelva a intentar"
        }
        
    #print("Respuesta retornada: "+str(result))
    return result
        

def main(id_consulta, event, context):
    respuesta = {}
        
    #se insertan los datos para el envio al servicio de verificacion
    response_insert_ver = insert_ver_cons(id_consulta, event, context)
        
    if response_insert_ver["code"] == 200:
        
        #se inserta el resultado de la verificacion
        response_resp_ver = insert_ver_resp(id_consulta, response_insert_ver["jsonEnvio"], event, context)
        #print("Respuesta de insert de json de regreso: "+str(response_insert_ver))
            
        if response_resp_ver["code"] != 200:
            print("Ocurrio un problema al intentar almacenar los datos de respuesta del servicio: ")
            print("code: "+response_resp_ver["code"]+", message: "+response_resp_ver["message"])

            
        #se hace la comparacion de resultados
        comparacion = compara_respuesta(id_consulta, event, response_resp_ver)

        #se inserta la comparacion de resultados
        response_insert_comp = insert_resumen(comparacion)
            
        #verifica si se insertaron correctamente los resultados, y el json de respuesta
        if response_resp_ver["code"] == 200 and response_insert_comp["code"] == 200:
            respuesta = {
                "code": 200,
                "message": "Flujo de verificacion de datos exitoso",
                "response": comparacion["respuesta"],
                "responseServ": response_resp_ver["response"]["jsonRespuesta"]
            }
                
        elif response_resp_ver["code"] != 200 and response_insert_comp["code"] != 200:
            respuesta = {
                "code": 201,
                "message": "Ocurrio un problema al insertar la respuesta de verificacion y la de comparacion",
                "response": comparacion["respuesta"],
                "responseServ": response_resp_ver["response"]["jsonRespuesta"]
            }
                
        elif response_resp_ver["code"] != 200: 
            respuesta = {
                "code": 202,
                "message": "Ocurrio un problema al insertar la respuesta de verificacion",
                "response": comparacion["respuesta"],
                "responseServ": response_resp_ver["response"]["jsonRespuesta"]
            }
                
        else:
            respuesta = {
                "code": 203,
                "message": "Ocurrio un problema al insertar la respuesta de comparacion",
                "response": comparacion["respuesta"],
                "responseServ": response_resp_ver["response"]["jsonRespuesta"]
            }
                
    else:
        respuesta = {
            "code": response_insert_ver["code"],
            "message": "Ocurrio un problema al insertar los datos que van al servicio de verificacion"
        }   
    
    #se  regresa el resultado de la comparación    
    return respuesta;
