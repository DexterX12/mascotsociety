from datetime import datetime, timezone

from .call_types.call_type_init import handle_init
from .call_types.call_type_load_player_profile import handle_load_player_profile
from .call_types.call_type_save_player_profile import handle_save_player_profile
from .call_types.call_type_get_new_home_extra_rooms_data import handle_get_new_home_extra_rooms_data
from .call_types.call_type_get_users_via_profile_fields import handle_get_users_via_profile_fields
from .call_types.call_type_purchase_cash_item import handle_purchase_cash_item
from .call_types.call_type_purchase_multiple_cash_or_coin_items import handle_purchase_multiple_cash_or_coin_items
from .call_types.call_type_purchase_mystery_box import handle_purchase_mystery_box
from .call_types.call_type_get_cafe_users import handle_get_cafe_users
from .call_types.call_type_redeem_voucher import handle_redeem_voucher
from .call_types.call_type_purchase_extra_room import handle_purchase_extra_room
from .call_types.call_type_exchange_cash_for_coins import handle_exchange_cash_for_coins
from .call_types.call_type_handle_fishing_action import handle_fishing_action
from .call_types.call_type_reset_map import handle_reset_map
from .call_types.call_type_save_digging_game import handle_save_digging_game
from .call_types.call_type_get_collaborative_build_items import handle_get_collaborative_build_items
from .call_types.call_type_complete_quest import handle_complete_quest

from ..utils.datastream.output_data_stream import OutputDataStream
from ..utils.datastream.input_data_stream import InputDataStream
from ..constants import CallTypes
from .. import profile_handler

def handle_batch(stream: InputDataStream, context: dict) -> bytes:
    batch_mode = stream.readUint8()
    request_count = stream.readUintvar32()

    response = OutputDataStream()
    response.writeUintvar32(request_count)

    for index in range(request_count):
        sub_type = stream.readUint8()
        payload = stream.readByteArray()
        try:
            body = handle_message(sub_type, InputDataStream(payload), context) or b""
            response.writeUint8(sub_type)
            response.writeByteArray(body)
        except Exception as exc:
            print(f"[batch] sub-request {index} (type {sub_type}) failed: {exc}")
            response.writeUint8(0)
            response.writeByteArray(b"")

    return response.getvalue()

def handle_message(msg_type:int, stream:InputDataStream, context:dict):
    if not msg_type in CallTypes.__dict__.values():
        print("Incoming non registered request: ", msg_type)
        print("Skipping...")
        return b''
    
    command_name = list(CallTypes.__dict__.keys())[list(CallTypes.__dict__.values()).index(msg_type)]

    print("Incoming request: ", command_name)

    if msg_type == CallTypes.CALL_TYPE_BATCH_OPERATION:
        return handle_batch(stream, context)

    elif msg_type == CallTypes.CALL_TYPE_INIT:
        return handle_init(stream, context)
    
    elif msg_type == CallTypes.CALL_TYPE_GET_SERVER_TIME:
        response = OutputDataStream()
        response.writeDate(datetime.now(timezone.utc))
        return response.getvalue()

    elif msg_type == CallTypes.CALL_TYPE_RECORD_GAME_EVENT:
        return b''

    elif msg_type == CallTypes.CALL_TYPE_POLL_EVENTS:
        return b''

    elif msg_type == CallTypes.CALL_TYPE_GET_CURRENCY_BALANCE:
        response = OutputDataStream()
        response.writeUintvar32(profile_handler.cash)
        return response.getvalue()

    elif msg_type == CallTypes.CALL_TYPE_INBOX_GET_LETTERS:
        response = OutputDataStream()
        response.writeArray([], lambda x: None)
        return response.getvalue()

    elif msg_type == CallTypes.CALL_TYPE_GET_EMAIL_PERMISSIONS:
        return b''
        # Response: Array of Strings
        # response_body = write_array([], None)

    elif msg_type == CallTypes.CALL_TYPE_INBOX_GET_RESTRICTED_SEND_USERS:
        return b''
        # Response: Array of Strings
        # response_body = write_array([], None)

    elif msg_type == CallTypes.CALL_TYPE_EXCHANGE_CASH_FOR_COINS:
        return handle_exchange_cash_for_coins(stream)
        
    elif msg_type == CallTypes.CALL_TYPE_PURCHASE_CASH_ITEM:
        return handle_purchase_cash_item(stream)
    
    elif msg_type == CallTypes.CALL_TYPE_PURCHASE_MULTIPLE_CASH_OR_COIN_ITEMS:
        return handle_purchase_multiple_cash_or_coin_items(stream)
    
    elif msg_type == CallTypes.CALL_TYPE_PURCHASE_EXTRA_ROOM:
        return handle_purchase_extra_room(stream)

    elif msg_type == CallTypes.CALL_TYPE_PURCHASE_MYSTERY_BOX:
        return handle_purchase_mystery_box(stream)
    
    elif msg_type == CallTypes.CALL_TYPE_REDEEM_VOUCHER:
        return handle_redeem_voucher(stream)

    elif msg_type == CallTypes.CALL_TYPE_LOAD_PLAYER_PROFILE:
        return handle_load_player_profile(stream, context)

    elif msg_type == CallTypes.CALL_TYPE_SAVE_PLAYER_PROFILE:
        return handle_save_player_profile(stream, context)

    elif msg_type == CallTypes.CALL_TYPE_GET_NEW_HOME_EXTRA_ROOMS_DATA:
        return handle_get_new_home_extra_rooms_data(stream)
    
    elif msg_type == CallTypes.CALL_TYPE_GET_USERS_VIA_PROFILE_FIELDS:
        return handle_get_users_via_profile_fields(stream, context)
    
    elif msg_type == CallTypes.CALL_TYPE_GET_CAFE_USERS:
        return handle_get_cafe_users(stream)
    
    elif msg_type == CallTypes.CALL_TYPE_HANDLE_FISHING_ACTION:
        return handle_fishing_action(stream)
    
    elif msg_type == CallTypes.CALL_TYPE_RESET_MAP:
        return handle_reset_map(stream)

    elif msg_type == CallTypes.CALL_TYPE_SAVE_DIGGING_GAME:
        return handle_save_digging_game(stream)
    
    elif msg_type == CallTypes.CALL_TYPE_GET_COLLABORATIVE_BUILD_ITEMS:
        return handle_get_collaborative_build_items(stream)
    
    elif msg_type == CallTypes.CALL_TYPE_COMPLETE_QUEST:
        return handle_complete_quest(stream)

    else:
        print(command_name, " is an existing but unhandled request!")
        print("Skipping...")
        return b''