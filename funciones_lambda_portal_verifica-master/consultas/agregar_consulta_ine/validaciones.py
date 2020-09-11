import json
import boto3
import os
import re

def valida_json_entrada(request):
    camposNoValidos = []
    numEmisionFlag = True
    claveElectFlag = True
    curpFlag = True
    ocrFlag = True
    cicFlag = True
    dateFlag = True
    
    regex_numEmi = re.compile("^[0-9]{2}$")
    regex_claveElect = re.compile("^[A-Z]{6}[0-9]{8}[A-Z]{1}[0-9]{3}$")
    regex_ocr = re.compile("^[0-9]{13}$")
    regex_cic = re.compile("^[0-9]{9}$")
    regex_numeros = re.compile("^[0-9]*$")
    
    #se validan los parametros que no tienen relacion con el CIC
    camposNoValidos = valida_campos_opcionales(request)
    
    #se verifica si se capturo el cic
    if is_campo_presente("cicIn",request):
        
        #se verifica si no cumple con la regex
        if not cumple_regex("cicIn",regex_cic,request):
            cicFlag = False
            camposNoValidos.append("CIC")
        
        #todos los demas campos son opcionales
        #si fueron capturados deben cumplir con su regex
        if is_campo_presente("ocrIn",request) and not cumple_regex("ocrIn",regex_ocr,request):
            ocrFlag = False
            camposNoValidos.append("OCR")
        
        if is_campo_presente("claveElectIn",request) and not cumple_regex("claveElectIn",regex_claveElect,request):
            claveElectFlag = False
            camposNoValidos.append("Clave de elector")
        
        if is_campo_presente("numEmiCredIn",request) and not cumple_regex("numEmiCredIn",regex_numEmi,request):
            numEmisionFlag = False
            camposNoValidos.append("Emision de la credencial")
    
    #si no se capturo el cic
    #debe capturarse el OCR, la clave de elector y la emisión de la credencial
    #deben cumplir con su regex
    else:
        if not is_campo_presente("ocrIn",request) or not cumple_regex("ocrIn",regex_ocr,request):
            ocrFlag = False
            camposNoValidos.append("OCR")
        
        if not is_campo_presente("claveElectIn",request) or not cumple_regex("claveElectIn",regex_claveElect,request):
            claveElectFlag = False
            camposNoValidos.append("Clave de elector")
        
        if not is_campo_presente("numEmiCredIn",request) or not cumple_regex("numEmiCredIn",regex_numEmi,request):
            numEmisionFlag = False
            camposNoValidos.append("Emision de la credencial")

    #se valida la estampa de tiempo 
    if not is_campo_presente("date",request) or not cumple_regex("date",regex_numeros,request):
        dateFlag = True
        camposNoValidos.append("Date")
    
    
    if len(camposNoValidos)!=0:
        return False
    else: 
        return True
    
    
def is_campo_presente(atributo, request):
    if atributo in request and len(request[atributo]) != 0:
        return True
    else:
        return False

def cumple_regex(atributo, expReg, request):
    if expReg.match(request[atributo]):
        return True
    else:
        return False
    
def valida_campos_opcionales(request):
    camposNoValidos = []
    nombreOk = True
    appOk = True
    apmOk = True
    anioRegOk = True
    anioEmiOk = True
    curpOk = True
    regex_nombres = re.compile("^([a-zA-Z]|á|é|í|ó|ú|ü|Á|É|Í|Ó|Ú|Ü|ñ|Ñ| ){2,32}$")
    regex_anio = re.compile("^[1-9][0-9]{3,3}$")
    regex_curp = re.compile("^([A-Z0-9]|Ñ| ){18}$")
    
    if is_campo_presente("nombreIn",request) and not cumple_regex("nombreIn",regex_nombres,request):
        nombreOk = False
        camposNoValidos.append("Nombre(s)")
    
    if is_campo_presente("apPaternoIn",request) and not cumple_regex("apPaternoIn",regex_nombres,request):
        appOk = False
        camposNoValidos.append("Apellido paterno")
    
    if is_campo_presente("apMaternoIn",request) and not cumple_regex("apMaternoIn",regex_nombres,request):
        apmOk = False
        camposNoValidos.append("Apellido materno")
    
    if is_campo_presente("anioRegIn",request) and not cumple_regex("anioRegIn",regex_anio,request):
        anioRegOk = False
        camposNoValidos.append("Año de registro")
    
    if is_campo_presente("anioEmiIn",request) and not cumple_regex("anioEmiIn",regex_anio,request):
        anioEmiOk = False
        camposNoValidos.append("Año de emisión")
        
    if is_campo_presente("curpIn",request) and not cumple_regex("curpIn",regex_curp,request):
        curpOk = False
        camposNoValidos.append("CURP")
        
    #if nombreOk and appOk and apmOk and anioRegOk and anioEmiOk and curpOk: 
    
    return camposNoValidos