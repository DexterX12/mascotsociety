import profile
from typing import final
from flask import Flask, request, render_template
from io import BytesIO
from datetime import datetime
from py_as.datastream.input_data_stream import InputDataStream
from handling.handler import handle_message
from profile import ProfileHandler
import logging

app = Flask(__name__, static_folder="./static", static_url_path="/", template_folder="static")
logging.getLogger('werkzeug').disabled = True

profile_handler = ProfileHandler()
profile_handler.load_from_file('profile.pet')

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/api", methods=["POST", "GET"])
def handle_rpc():
    content = request.get_data()
    request_body = InputDataStream(BytesIO(content))
    try:
        encapsulation_type = request_body.read_uint8()
        msg_type = request_body.read_uint8()
        session_id = request_body.read_string()
        
        print(f"Encapsulation: {encapsulation_type}, Msg Type: {msg_type}")
        
        context = {'session_id': session_id, "profile": profile_handler}
        response_payload = handle_message(msg_type, request_body, context)

        final_response = b'\x00' + bytes([msg_type]) + response_payload

        print(f"Final response hex: {final_response.hex()}")
        return final_response, 200, {'Content-Type': 'application/octet-stream'}

    except Exception as e:
        print(f"Error decoding request: {e}")
        import traceback
        traceback.print_exc()
        return "Error", 500

if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(port=8881)