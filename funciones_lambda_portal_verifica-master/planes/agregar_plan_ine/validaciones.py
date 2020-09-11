import json
import boto3
import os
import re

def valida_json_entrada(request):
    dateFlag = False
    descFlag = False
    solMaxMesFlag = False
    solMaxMinFlag = False
    costoMesFlag = False
    costoAnualFlag = False
        
    regex_numeros = re.compile("^[0-9]*$")
    regex_caracteres = re.compile("^([a-zA-Z]|á|é|í|ó|ú|Á|É|Í|Ó|Ú|ñ|Ñ| )*$")
    regex_numeros_flotantes = re.compile("^([1-9]\d*)(\.[0-9]{0,2})?$")
    regex_caracteres_desc = re.compile("^([a-zA-Z0-9.,]|á|é|í|ó|ú|Á|É|Í|Ó|Ú|ñ|Ñ| ){1,100}$")
    regex_numeros_max_mes = re.compile("^([1-9][0-9]{2,7})$")
    regex_numeros_max_min = re.compile("^([1-9][0-9]{0,3})$")
    regex_numeros_float_plan = re.compile("^([1-9][0-9]{4,6})(\.[0-9]{1,2})?$")
    
    #se verifica si tiene los 6 parametros y son del tipo de dato esperado
    dateFlag = valida_campo("date", regex_numeros, request)
    descFlag = valida_campo("descripcion", regex_caracteres_desc, request)
    solMaxMesFlag = valida_campo("solMaxMes", regex_numeros_max_mes, request)
    solMaxMinFlag = valida_campo("solMaxMin", regex_numeros_max_min, request)
    costoMesFlag = valida_campo("costoMensual", regex_numeros_float_plan, request)
    costoAnualFlag = valida_campo("costoAnual", regex_numeros_float_plan, request)
    
    return dateFlag and descFlag and solMaxMesFlag and solMaxMinFlag and costoMesFlag and costoAnualFlag
    
        
def valida_campo(atributo, expReg, request):
    if atributo in request and len(request[atributo]) != 0 and expReg.match(request[atributo]):
        return True
    else:
        return False

