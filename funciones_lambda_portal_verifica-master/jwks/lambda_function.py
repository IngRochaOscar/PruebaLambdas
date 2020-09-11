import json
import urllib3

def lambda_handler(event, context):
    http = urllib3.PoolManager()
    
    try:
        r = http.request('GET', 'https://cognito-idp.us-east-1.amazonaws.com/us-east-1_bawhNB8EQ/.well-known/jwks.json')
    except ClientError as e:
        respuesta = {
            "code": 400,
            "message": "Ocurrio un problema al intentar recuperar la llave pública: " +e.data
        }
    except Exception as e:
        respuesta = {
            "code": 400,
            "message": "Ocurrio un problema el intentar recuperar la información : ErrorType: " + str(e)
        }
    else:
        respuesta = {
            'code': r.status,
            'response':r.data,
            'message': "Llave pública recuperada de forma exitosa"
        }
        
    return respuesta