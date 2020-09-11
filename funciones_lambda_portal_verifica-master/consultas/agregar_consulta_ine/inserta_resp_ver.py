import json
import boto3
import os
import time
from botocore.exceptions import ClientError

def insert_ver_resp(id_consulta, jsonEnvio, event, context):
    
    try:
        dynamodb = boto3.resource('dynamodb')
        nombre_tabla = os.environ['consultaVer']
        tabla = dynamodb.Table(nombre_tabla)
        
        resp_ver={
            "response": {
                "fechaHoraPeticion": time.strftime("%m/%d/%Y %H:%M:%S")+"",
                "indiceSolicitud": None,
                "dataResponse": {
                    "respuestaSituacionRegistral": None,
                    "respuestaComparacion": {
                        "anioRegistro": None,
                        "claveElector": True,
                        "apellidoPaterno": True,
                        "anioEmision": False,
                        "numeroEmisionCredencial": False,
                        "nombre": True,
                        "curp": True,
                        "apellidoMaterno": True,
                        "ocr": True
                    },
                    "codigoRespuestaDatos": 205
                },
                "minutiaeResponse": {
                    "codigoRespuestaMinucia": 0,
                    "similitud2": "100.0%",
                    "similitud7": "100.0%"
                },
                "tiempoProcesamiento": 731,
                "codigoRespuesta": 0
            },
            "signature": {
                "signedInfo": {
                    "canonicalizationMethod": {
                        "algorithm": "http://www.w3.org/TR/2001/REC-xml-c14n-20010315"
                    },
                    "signatureMethod": {
                        "algorithm": "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"
                    },
                    "reference": {
                        "digestMethod": {
                            "algorithm": "http://www.w3.org/2001/04/xmlenc#sha256"
                        },
                        "digestValue": "tfMy10/CFT63GDQwt96rTnFiM29yOyl+zzrwJXqOeG4=",
                        "uri": "#DATA"
                    }
                },
                "signatureValue": "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256",
                "keyInfo": {
                    "x509Data": {
                        "x509SerialNumber": "INE_2018"
                    }
                }
            },
            "timestamp": {
                "momento": "20180614212752.27Z",
                "indice": "2f00000000201806140000000000000000000000000099089150968835",
                "numeroSerie": "20180614212752.27Z"
            }
        }
        
        
        response = tabla.put_item(Item = {
            "id_consulta": id_consulta,
            "jsonEnvio": jsonEnvio,
            "jsonRespuesta": resp_ver
        })
        
            
    except ClientError as e:
        respuesta = {
            "code": e.response['ResponseMetadata']['HTTPStatusCode'],
            "message": e.response['Error']['Message'],
            "response": {
                "jsonEnvio": jsonEnvio,
                "jsonRespuesta": resp_ver
            }
        }
    else:
        respuesta = {
            "code": response['ResponseMetadata']['HTTPStatusCode'],
            "message": "Registro insertado de forma exitosa",
            "response": {
                "jsonEnvio": jsonEnvio,
                "jsonRespuesta": resp_ver
            }
        }

    return respuesta
