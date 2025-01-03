from .scraper import get_trc_sender_address, get_erc_sender_address


def get_sender_address(hash_id):
    if hash_id.startswith('0x'):
        sender_address = get_erc_sender_address(hash_id)
    else:
        sender_address = get_trc_sender_address(hash_id)

    return sender_address
