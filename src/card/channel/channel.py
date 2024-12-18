class Channel:
    def __init__(self, name, apply_fee, top_up_fee):
        self.name = name
        self.apply_fee = apply_fee
        self.top_up_fee = top_up_fee

    def get_name(self):
        return self.name

    def get_apply_fee(self):
        return self.apply_fee

    def get_top_up_fee(self):
        return self.top_up_fee


class FinancialOne(Channel):
    def __init__(self):
        super().__init__('Financial One', 0, 0)
