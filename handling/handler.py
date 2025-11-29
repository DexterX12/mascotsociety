from .call_types.call_type_init import handle_init
from .call_types.call_type_load_player_profile import handle_load_player_profile
from .call_types.call_type_save_player_profile import handle_save_player_profile
from .call_types.call_type_get_new_home_extra_rooms_data import handle_get_new_home_extra_rooms_data
from .call_types.call_type_get_users_via_profile_fields import handle_get_users_via_profile_fields
from py_as.datastream.output_data_stream import OutputDataStream
from py_as.datastream.input_data_stream import InputDataStream
from constants import CALL_TYPES
from constants import type_to_int

def handle_batch(stream:InputDataStream, context: dict) -> bytes:
    batch_mod = stream.read_uint8()
    count = stream.read_uintvar32()
    print(f"Batch Mod: {batch_mod}, Count: {count}")
    
    # Batch Response: [Count] + ( [Type] [ByteArray(Body)] ) * Count
    response_body = OutputDataStream()
    response_body.write_uintvar32(count)
    
    for i in range(count):
        try:
            sub_request_type = stream.read_uint8()
            sub_request_body = stream.read_byte_array()
            print(f"  [{i}] Processing SubRequest Type: {sub_request_type}, Size: {len(sub_request_body)}")
            
            sub_request_response = handle_message(sub_request_type, InputDataStream(sub_request_body), context)
            
            response_body.write_uint8(sub_request_type)
            response_body.write_byte_array(sub_request_response)
            
        except EOFError as e:
            print(f"  [{i}] Error: {e}")
            break

    return response_body.getvalue()

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