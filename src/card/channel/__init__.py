from .channel import FinancialOne


def get_channel(name):
    if name is 'FO':
        return FinancialOne()
