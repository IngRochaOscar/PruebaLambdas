import json
import boto3
import os
import re

def valida_json_entrada(request):
    idUsrFlag = False
    dateFlag = False
    rolFlag = False
    nombresFlag = False
    apellidoPatFlag = False
    apellidoMatFlag = False
    sexoFlag = False
    rfcFlag = False
    entidadFlag = False
    grupoCognitoFlag = False
    usuarioCognitoFlag = False

    regex_email = re.compile("^([a-zA-Z0-9._%+-]{2,})+(@[a-zA-Z0-9.-]*)+([.][a-zA-Z0-9]{2,4})$")
    regex_numeros = re.compile("^[0-9]*$")
    regex_rol = re.compile("^([A-Z0-9_]|Ñ| ){19,26}$")
    regex_nombres = re.compile("^([a-zA-Z0-9.]|á|é|í|ó|ú|Á|É|Í|Ó|Ú|ñ|Ñ| ){2,40}$")
    regex_sexo = re.compile("^(H|M| ){1,1}$")
    regex_rfc = re.compile("^([A-Z0-9]|Ñ| ){9,13}$")
    regex_grupo_cognito = re.compile("^([a-zA-Z0-9]|Ñ|ñ ){20,27}$")
    regex_usuario_cognito = re.compile("^([a-zA-Z0-9-])*$")
    
    #se verifica si tiene los 11 parametros y son del tipo de dato esperado
    idUsrFlag = valida_campo("id_usuario", regex_email, request)
    if idUsrFlag and len(request["id_usuario"])>2 and len(request["id_usuario"])<66:
        idUsrFlag = True
    else:
        idUsrFlag = False
    
    dateFlag = valida_campo("date", regex_numeros, request)
    rolFlag = valida_campo("rol", regex_rol, request)
    nombresFlag = valida_campo("nombres", regex_nombres, request)
    apellidoPatFlag = valida_campo("apellidoPat", regex_nombres, request)
    apellidoMatFlag = valida_campo("apellidoMat", regex_nombres, request)
    sexoFlag = valida_campo("sexo", regex_sexo, request)
    rfcFlag = valida_campo("rfc", regex_rfc, request)
    entidadFlag = valida_campo("entidad", regex_rfc, request)
    grupoCognitoFlag = valida_campo("grupoCognito", regex_grupo_cognito, request)
    usuarioCognitoFlag = valida_campo("usuarioCognito", regex_usuario_cognito, request)
    
    return idUsrFlag and dateFlag and rolFlag and nombresFlag and apellidoPatFlag and apellidoMatFlag and sexoFlag and rfcFlag and entidadFlag and grupoCognitoFlag and usuarioCognitoFlag
    
def valida_campo(atributo, expReg, request):
    if atributo in request and len(request[atributo]) != 0 and expReg.match(request[atributo]):
        return True
    else:
        return False

