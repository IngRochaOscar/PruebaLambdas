import json
import boto3
import os
import uuid
import time
import calendar
from botocore.exceptions import ClientError

def compara_respuesta(id_consulta, event, response_resp_ver):

    accesos_base = "PortalAdminRoot,PortalAdmin"+event["idEntidad"]+",PortalConsulta"+event["idEntidad"]+",PortalReportes"+event["idEntidad"]

    dataRes = { 
        "id_consulta": id_consulta,
        'username': event["username"],
        'date': event["date"],
        'nombreIn': event["nombreIn"],
        'apPaternoIn': event["apPaternoIn"],
        'codPostIn': event["codPostIn"],
        'latitudIn': event["latitudIn"],
        'longitudIn': event["longitudIn"],
        'apMaternoIn': event["apMaternoIn"],
        'anioRegIn': event["anioRegIn"],
        'anioEmiIn': event["anioEmiIn"],
        'numEmiCredIn': event["numEmiCredIn"],
        'claveElectIn': event["claveElectIn"],
        'curpIn': event["curpIn"],
        'ocrIn': event["ocrIn"],
        'cicIn': event["cicIn"],
        'idEntidad': event["idEntidad"],
        'acceso_rol': accesos_base,
        'minucia2In': event["minucia2In"],
        'minucia7In': event["minucia7In"],
        "respuesta": {
            'username': event["username"],
            'idEntidad': event["idEntidad"],
            "fechaReqOut": response_resp_ver["response"]["jsonRespuesta"]["response"]["fechaHoraPeticion"],
            "indiceSolOut": None,
            "tiempoProcOut": response_resp_ver["response"]["jsonRespuesta"]["response"]["tiempoProcesamiento"],
            "codRespOut":  response_resp_ver["response"]["jsonRespuesta"]["response"]["codigoRespuesta"],
            "codRespDatosOut": response_resp_ver["response"]["jsonRespuesta"]["response"]["dataResponse"]["codigoRespuestaDatos"],
            "tipoSitRegOut": None,
            "tipoRepRoboOut": None,
            "ocrOut": evaluaResp(response_resp_ver["response"]["jsonRespuesta"]["response"]["dataResponse"]["respuestaComparacion"]["ocr"]),
            "nombreOut": evaluaResp(response_resp_ver["response"]["jsonRespuesta"]["response"]["dataResponse"]["respuestaComparacion"]["nombre"]),
            "apPaternoOut": evaluaResp(response_resp_ver["response"]["jsonRespuesta"]["response"]["dataResponse"]["respuestaComparacion"]["apellidoPaterno"]),
            "apMaternoOut": evaluaResp(response_resp_ver["response"]["jsonRespuesta"]["response"]["dataResponse"]["respuestaComparacion"]["apellidoMaterno"]),
            "anioRegOut": evaluaResp(response_resp_ver["response"]["jsonRespuesta"]["response"]["dataResponse"]["respuestaComparacion"]["anioRegistro"]),
            "anioEmiOut": evaluaResp(response_resp_ver["response"]["jsonRespuesta"]["response"]["dataResponse"]["respuestaComparacion"]["anioEmision"]),
            "numEmiCredOut": evaluaResp(response_resp_ver["response"]["jsonRespuesta"]["response"]["dataResponse"]["respuestaComparacion"]["numeroEmisionCredencial"]),
            "claveElectOut": evaluaResp(response_resp_ver["response"]["jsonRespuesta"]["response"]["dataResponse"]["respuestaComparacion"]["claveElector"]),
            "curpOut": evaluaResp(response_resp_ver["response"]["jsonRespuesta"]["response"]["dataResponse"]["respuestaComparacion"]["curp"]),
            "codRespMinOut": evaluaResp(response_resp_ver["response"]["jsonRespuesta"]["response"]["minutiaeResponse"]["codigoRespuestaMinucia"]),
            "minucia2Out": response_resp_ver["response"]["jsonRespuesta"]["response"]["minutiaeResponse"]["similitud2"],
            "minucia7Out": response_resp_ver["response"]["jsonRespuesta"]["response"]["minutiaeResponse"]["similitud7"],
            "canMethAlgOut": response_resp_ver["response"]["jsonRespuesta"]["signature"]["signedInfo"]["canonicalizationMethod"]["algorithm"],
            "signMethAlgOut": response_resp_ver["response"]["jsonRespuesta"]["signature"]["signedInfo"]["signatureMethod"]["algorithm"],
            "digestMethAlgOut": response_resp_ver["response"]["jsonRespuesta"]["signature"]["signedInfo"]["reference"]["digestMethod"]["algorithm"],
            "digestValOut": response_resp_ver["response"]["jsonRespuesta"]["signature"]["signedInfo"]["reference"]["digestValue"],
            "uriOut": response_resp_ver["response"]["jsonRespuesta"]["signature"]["signedInfo"]["reference"]["uri"],
            "x509SerNumOut": response_resp_ver["response"]["jsonRespuesta"]["signature"]["keyInfo"]["x509Data"]["x509SerialNumber"],
            "momentoOut": response_resp_ver["response"]["jsonRespuesta"]["timestamp"]["momento"],
            "indiceOut": response_resp_ver["response"]["jsonRespuesta"]["timestamp"]["indice"],
            "numSerOut": response_resp_ver["response"]["jsonRespuesta"]["timestamp"]["numeroSerie"],
            "exceptOut": None,
            "exceptDescOut": None,
            "fechaFormateada": time.strftime("%m/%d/%Y %H:%M:%S")+""
        },
        "jsonEnvio": response_resp_ver["response"]["jsonEnvio"],
        "jsonRespuesta": response_resp_ver["response"]["jsonRespuesta"]
    }

    return dataRes

def evaluaResp(boolean_value):
    if boolean_value:
        return 1
    elif boolean_value == False:
        return 0
    else:
        return None
