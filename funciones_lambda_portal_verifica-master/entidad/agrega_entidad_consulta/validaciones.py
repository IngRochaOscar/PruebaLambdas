import json
import boto3
import os
import re

def valida_json_entrada(request):
    dateFlag = False
    razonSocFlag = False
    rfcFlag = False
    idPlanFlag = False
    avisoPrivFlag = False
    
    regex_numeros = re.compile("^[0-9]*$")
    regex_caracteres_razon_soc = re.compile("^([a-zA-Z0-9.,]|á|é|í|ó|ú|Á|É|Í|Ó|Ú|ñ|Ñ| ){1,150}$")
    regex_caracteres_rfc = re.compile("^([a-zA-Z0-9]|Ñ| ){9,13}$")
    regex_caracteres_idPlan = re.compile("^([a-zA-Z0-9-]|Ñ| ){2,}$")
    
    #se verifica si tiene los 5 parametros y son del tipo de dato esperado
    dateFlag = valida_campo("date", regex_numeros, request)
    razonSocFlag = valida_campo("razonSocial", regex_caracteres_razon_soc, request)
    rfcFlag = valida_campo("rfc", regex_caracteres_rfc, request)
    idPlanFlag = valida_campo("idPlan", regex_caracteres_idPlan, request)
    
    if "avisoPrivacidad" in request and len(request["avisoPrivacidad"]) != 0:
        avisoPrivFlag = True
    
    return dateFlag and razonSocFlag and rfcFlag and idPlanFlag and avisoPrivFlag
    
def valida_campo(atributo, expReg, request):
    if atributo in request and len(request[atributo]) != 0 and expReg.match(request[atributo]):
        return True
    else:
        return False

