import requests
from time import sleep
from random import randint, random, seed
import json
# from opentelemetry import trace


url = 'http://127.0.0.1:5000/echo'

def pythonrequests():
    payload = {'fruit': 'value'}
    a = random.randint(1,4)
    if a == 2:
        requestURL = 'http://127.0.0.1:5000/echo'
        payload = {'fruit': 'banana'}
    elif a == 3:
        requestURL = 'http://127.0.0.1:5000/echo'
        payload = {'fruit': 'strawberry'}
    elif a == 4:
        requestURL = 'http://127.0.0.1:5000/echo'
        payload = {'fruit': 'apple'}
    else:
        requestURL = 'http://127.0.0.1:5000/lookHere'
        payload = {'fruit': 'banana'}
        # customizedSpan = trace.get_current_span()
        # customizedSpan.set_attribute("fruit", payload['fruit'])
        try:
            r=requests.put(requestURL, params=payload)
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
    # customizedSpan = trace.get_current_span()
    # customizedSpan.set_attribute("fruit", payload['fruit'])
    try:
        r=requests.post(requestURL, params=payload)
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
#    seed(1)
    y = random()
    #print('Sleeping: ', round(y,2))
    sleep(round(y,2))
