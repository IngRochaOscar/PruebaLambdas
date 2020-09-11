import json
import boto3
import os
import uuid
from botocore.exceptions import ClientError

def insert_ver_cons(id_consulta, event, context):
    minucia2 = False
    minucia7 = False
    minuciasObj = {}
    posicionSatelitalObj = {}
    
    try:
        rand_id = uuid.uuid4()
        dynamodb = boto3.resource('dynamodb')
        nombre_tabla = os.environ['consultaVer']
        tabla = dynamodb.Table(nombre_tabla)
        
        #se verifica si se registraron huellas
        if 'minucia2In' in event and len(event["minucia2In"]) != 0:
            minucia2 = True
        else:
            event["minucia2In"] = None
    
        if 'minucia7In' in event and len(event["minucia7In"]) != 0:
            minucia7 = True
        else:
            event["minucia7In"] = None
         
        
        if not minucia2 and not minucia7:
            minuciasObj = None
        else:
            minuciasObj = { "tipo": 2,
                            "ancho": None,
                            "alto": None,
                            "minucia2": event["minucia2In"],
                            "minucia7": event["minucia7In"]}
        
        #se verifica si ubicacion tiene al menos un nodo requerido
        if 'latitudIn' in event and len(event["latitudIn"]) != 1  and 'longitudIn' in event and len(event["longitudIn"]) != 1:
            posicionSatelitalObj = { "latitud": event["latitudIn"],
                                     "longitud": event["longitudIn"]}
        else:
            posicionSatelitalObj = None
        
        jsonEnvio={
                "id_consulta": id_consulta,
                "username": event["username"],
                "data": {
                    "datosCifrados": {
                        "ocr": event["ocrIn"],
                        "cic": event["cicIn"],
                        "nombre": event["nombreIn"],
                        "apellidoPaterno": event["apPaternoIn"],
                        "apellidoMaterno": event["apMaternoIn"],
                        "anioRegistro": event["anioRegIn"],
                        "anioEmision": event["anioEmiIn"],
                        "numeroEmisionCredencial": event["numEmiCredIn"],
                        "claveElector": event["claveElectIn"],
                        "curp": event["curpIn"]
                    },
                    "minucias": minuciasObj,
                    "ubicacion": {
                        "posicionSatelital": posicionSatelitalObj,
                        "localidad": None,
                        "consentimiento": True
                    }
                },
                "signature": {
                    "signedInfo": {
                        "canonicalizationMethod": {
                            "algorithm": None
                        },
                        "signatureMethod": {
                            "algorithm": None
                        },
                        "reference": {
                            "digestMethod": {
                                "algorithm": None
                            },
                        "digestValue": None,
                        "uri": None
                        }
                    },
                    "signatureValue": None,
                    "keyInfo": {
                        "x509Data": {
                            "x509SerialNumber": None
                        }
                    }
                },
                "timestamp": {
                    "momento": None,
                    "indice": None,
                    "numeroSerie": None
                }
            }
            
        response = tabla.put_item(Item = jsonEnvio)
        del jsonEnvio["id_consulta"]
            
    except ClientError as e:
        respuesta = {
            "code": e.response['ResponseMetadata']['HTTPStatusCode'],
            "message": e.response['Error']['Message'],
            "jsonEnvio": jsonEnvio
        }
    else:
        respuesta = {
            "code": response['ResponseMetadata']['HTTPStatusCode'],
            "message": "Registro insertado de forma exitosa",
            "jsonEnvio": jsonEnvio
        }

    return respuesta
