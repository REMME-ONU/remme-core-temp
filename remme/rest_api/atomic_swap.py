import json
import logging

from remme.clients.atomic_swap import AtomicSwapClient, get_swap_init_payload, get_swap_approve_payload, \
    get_swap_expire_payload, get_swap_set_secret_lock_payload, get_swap_close_payload
from google.protobuf.json_format import MessageToJson

client = AtomicSwapClient()

LOGGER = logging.getLogger(__name__)


def init(**data):
    data = data['payload']
    payload = get_swap_init_payload(**data)
    return client.swap_init(payload)


def approve(**data):
    data = data['payload']
    payload = get_swap_approve_payload(**data)
    return client.swap_approve(payload)


def expire(**data):
    data = data['payload']
    payload = get_swap_expire_payload(**data)
    return client.swap_expire(payload)


def set_secret_lock(**data):
    data = data['payload']
    payload = get_swap_set_secret_lock_payload(**data)
    return client.swap_set_secret_lock(payload)


def close(**data):
    data = data['payload']
    swap_info = client.swap_get(data['swap_id'])
    LOGGER.info('swap_info: {}'.format(swap_info))
    payload = get_swap_close_payload(**data)
    return client.swap_close(payload, receiver_address=swap_info.receiver_address)


def get_swap_info(swap_id):
    swap_info = client.swap_get(swap_id)
    LOGGER.info(f'Get swap info {swap_info}')
    return json.loads(MessageToJson(swap_info, preserving_proto_field_name=True, including_default_value_fields=True))


def get_pub_key_encryption():
    return {'pub_key': client.get_pub_key_encryption()}
