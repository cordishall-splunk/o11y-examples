# from splunk_otel.tracing import start_tracing
# from opentelemetry.instrumentation.flask import FlaskInstrumentor
from flask import Flask, make_response, request
import json
# from opentelemetry import trace

app = Flask(__name__)

# def setup_tracing():
#     start_tracing()
#     FlaskInstrumentor().instrument_app(app)

@app.route('/echo', methods=['GET', 'POST'])
def echo():
    log_dict = {'requestdata': str(request.data),
            'requestheaders': str(request.headers)
            }
    # customizedSpan = trace.get_current_span()
    # customizedSpan.set_attribute("queryString", request.query_string)
    return(json.dumps(log_dict,indent=2,separators=(',', ':')))
if __name__ == '__main__':
    app.run(host='0.0.0.0')