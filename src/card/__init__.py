from .card import MWCard, UCard, KimCard


def get_card(card_name, channel_name):
    if card_name == 'MW':
        return MWCard(channel_name)
    elif card_name == 'U':
        return UCard(channel_name)
    elif card_name == 'KIM':
        return KimCard(channel_name)
