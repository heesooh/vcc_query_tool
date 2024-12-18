from channel import get_channel


class Card:
    def __init__(
            self,
            name,
            channel_name,
            monthly_fee,
            min_top_up_amount,
            internal_apply_fee,
            internal_top_up_rate,
            client_apply_fee,
            client_top_up_rate
    ):
        self.name = name
        self.channel_name = channel_name
        self.monthly_fee = monthly_fee
        self.min_top_up_amount = min_top_up_amount
        self.internal_apply_fee = internal_apply_fee
        self.internal_top_up_rate = internal_top_up_rate
        self.client_apply_fee = client_apply_fee
        self.client_top_up_rate = client_top_up_rate

        self.channel = get_channel(channel_name)

    def get_name(self):
        return self.name

    def get_channel_name(self):
        return self.channel_name

    def get_monthly_fee(self):
        return self.monthly_fee

    def get_min_top_up_amount(self):
        return self.min_top_up_amount

    def get_apply_fee(self):
        return self.internal_apply_fee + self.client_apply_fee + self.channel.get_apply_fee()

    def get_internal_apply_fee(self):
        return self.internal_apply_fee

    def get_client_apply_fee(self):
        return self.client_apply_fee

    def top_up_rate(self):
        return self.internal_top_up_rate + self.client_top_up_rate + self.channel.get_top_up_fee()

    def get_internal_top_up_rate(self):
        return self.internal_top_up_rate

    def get_client_top_up_rate(self):
        return self.client_top_up_rate


class MWCard(Card):
    def __init__(self, channel_name):
        super().__init__(
            'Mountain Wolf Card',
            channel_name,
            5,
            20,
            0,
            0.018,
            5,
            0.012
        )


class UCard(Card):
    def __init__(self, channel_name):
        super().__init__(
            'U Card',
            channel_name,
            5,
            20,
            3,
            0.018,
            5,
            0.012
        )


class KimCard(Card):
    def __init__(self, channel_name):
        super().__init__(
            'Kim Card',
            channel_name,
            5,
            20,
            3,
            0.018,
            5,
            0.012
        )
