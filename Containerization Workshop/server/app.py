from splunk_otel.tracing import start_tracing
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from flask import Flask, make_response, request
import json

app = Flask(__name__)

def setup_tracing():
    start_tracing()
    FlaskInstrumentor().instrument_app(app)

@app.route('/echo', methods=['GET', 'POST'])
def echo():
    log_dict = {'requestdata': str(request.data),
            'requestheaders': str(request.headers)
            }
    return(json.dumps(log_dict,indent=2,separators=(',', ':')))
if __name__ == '__main__':
    app.run(host='0.0.0.0')