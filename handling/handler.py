from datetime import datetime, timezone
from .call_types.call_type_init import handle_init
from .call_types.call_type_load_player_profile import handle_load_player_profile
from .call_types.call_type_save_player_profile import handle_save_player_profile
from .call_types.call_type_get_new_home_extra_rooms_data import handle_get_new_home_extra_rooms_data
from .call_types.call_type_get_users_via_profile_fields import handle_get_users_via_profile_fields
from utils.datastream.output_data_stream import OutputDataStream
from utils.datastream.input_data_stream import InputDataStream
from constants import CALL_TYPES
from constants import type_to_int

def handle_batch(stream: InputDataStream, context: dict) -> bytes:
    batch_mode = stream.read_uint8()
    request_count = stream.read_uintvar32()

    response = OutputDataStream()
    response.write_uintvar32(request_count)

    for index in range(request_count):
        sub_type = stream.read_uint8()
        payload = stream.read_byte_array()
        try:
            body = handle_message(sub_type, InputDataStream(payload), context) or b""
            response.write_uint8(sub_type)
            response.write_byte_array(body)
        except Exception as exc:
            print(f"[batch] sub-request {index} (type {sub_type}) failed: {exc}")
            response.write_uint8(ERROR_RESPONSE)
            response.write_byte_array(b"")
            # Optional: skip executing the remaining requests for BATCHMODE_CONDITIONAL

    return response.getvalue()

def handle_message(msg_type:int, stream:InputDataStream, context:dict):
    if not CALL_TYPES.get(msg_type):
        print("Incoming non registered request: ", msg_type)
        print("Skipping...")
        return b''

    print("Incoming request: ", CALL_TYPES[msg_type])

    if msg_type == type_to_int(CALL_TYPES, "CALL_TYPE_BATCH_OPERATION"):
        return handle_batch(stream, context)

    elif msg_type == type_to_int(CALL_TYPES, "CALL_TYPE_INIT"):
        return handle_init(stream, context)
    
    elif msg_type == type_to_int(CALL_TYPES, "CALL_TYPE_GET_SERVER_TIME"):
        response = OutputDataStream()
        response.writeDate(datetime.now(timezone.utc))
        return response.getvalue()

    elif msg_type == type_to_int(CALL_TYPES, "CALL_TYPE_RECORD_GAME_EVENT"):
        return b''

    elif msg_type == type_to_int(CALL_TYPES, "CALL_TYPE_POLL_EVENTS"):
        return b''

    elif msg_type == type_to_int(CALL_TYPES, "CALL_TYPE_GET_CURRENCY_BALANCE"): # 234
        response = OutputDataStream()
        response.write_uintvar32(context['profile'].cash)
        return response.getvalue()

    elif msg_type == type_to_int(CALL_TYPES, "CALL_TYPE_INBOX_GET_LETTERS"):
        return b''
        # response_body = write_array([], None)

    elif msg_type == type_to_int(CALL_TYPES, "CALL_TYPE_GET_EMAIL_PERMISSIONS"):
        return b''
        # Response: Array of Strings
        # response_body = write_array([], None)

    elif msg_type == type_to_int(CALL_TYPES, "CALL_TYPE_INBOX_GET_RESTRICTED_SEND_USERS"):
        return b''
        # Response: Array of Strings
        # response_body = write_array([], None)
        
    elif msg_type == type_to_int(CALL_TYPES, "CALL_TYPE_GET_CASH_BALANCE"):
        return b''
        # response_body = write_uintvar32(500) # Example

    elif msg_type == type_to_int(CALL_TYPES, "CALL_TYPE_LOAD_PLAYER_PROFILE"):
        return handle_load_player_profile(stream, context)

    elif msg_type == type_to_int(CALL_TYPES, "CALL_TYPE_SAVE_PLAYER_PROFILE"):
        return handle_save_player_profile(stream, context)

    elif msg_type == type_to_int(CALL_TYPES, "CALL_TYPE_GET_NEW_HOME_EXTRA_ROOMS_DATA"):
        return handle_get_new_home_extra_rooms_data(stream)
    
    elif msg_type == type_to_int(CALL_TYPES, "CALL_TYPE_GET_USERS_VIA_PROFILE_FIELDS"):
        return handle_get_users_via_profile_fields(stream, context)
    else:
        print(CALL_TYPES[msg_type], " is an existing but unhandled request!")
        print("Skipping...")
        return b''