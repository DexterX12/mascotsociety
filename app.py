from flask import Flask, request, render_template
from io import BytesIO
from .utils.datastream.input_data_stream import InputDataStream
from .handling.handler import handle_message
from .constants import Server
from . import database_handler
import logging

app = Flask(__name__, static_folder="./static", static_url_path="/", template_folder="static")
logging.getLogger('werkzeug').disabled = True

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/api", methods=["POST", "GET"])
def handle_rpc():
    content = request.get_data()
    request_body = InputDataStream(BytesIO(content))
    try:
        encapsulation_type = request_body.readUint8()
        msg_type = request_body.readUint8()
        session_id = request_body.readString()

        print(f"Encapsulation: {encapsulation_type}, Msg Type: {msg_type}")
        
        context = {'session_id': session_id}
        response_payload = handle_message(msg_type, request_body, context)

        final_response = b'\x00' + bytes([msg_type]) + response_payload

        #print(f"Final response hex: {final_response.hex()}")
        return final_response, 200, {'Content-Type': 'application/octet-stream'}

    except Exception as e:
        print(f"Error decoding request: {e}")
        import traceback
        traceback.print_exc()
        return "Error", 500
    
with app.app_context():
    database_handler.load()

if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(port=Server.LISTENING_PORT)
    