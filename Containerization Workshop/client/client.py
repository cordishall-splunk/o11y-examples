import requests
from time import sleep
from random import randint, random, seed
import json

seed(1)
url = 'http://127.0.0.1:5000/echo'

def pythonrequests():
    payload = {'key': 'value'}
    a = randint(1,2)
    if a == 2:
        requestURL = 'http://127.0.0.1:5000/echo'
    else:
        requestURL = 'http://127.0.0.1:5000/lookHere'
    try:
        r=requests.post(url, params=payload)
        log_dict = {'httpMETHOD': "post",
            'httpURL': str(r.url),
            'httpSTATUS': str(r.status_code),
            'httpCONTENT': str(r.content)
            }
        print(json.dumps(log_dict,indent=2,separators=(',', ':')))
    except requests.exceptions.RequestException as err:
        log_dict = {'error': str(err),   
            }
        print(json.dumps(log_dict,indent=2,separators=(',', ':')))

while True:
    pythonrequests()
    y = random()
    #print('Sleeping: ', round(y,2))
    sleep(round(y,2))
