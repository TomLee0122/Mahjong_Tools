from constants import CURRENT_CARD_NUM, SINGLE_CARD_MAX_NUM


class Mahjong_Card_Num_Error(ValueError):
    def __init__(self, card_count):
        self.card_count = card_count
        self.message = f"The number of cards should be {CURRENT_CARD_NUM}, not {self.card_count}!"
        raise ValueError(self.message)


class Undefined_Mahjong_Card_Error(ValueError):
    def __init__(self, card_name):
        self.undefined_card_name = card_name
        self.message = f"Undefined Mahjong card/type: {self.undefined_card_name}!"
        raise ValueError(self.message)


class Single_Card_Num_Error(ValueError):
    def __init__(self, card_num):
        self.card_num = card_num
        self.message = f"The number of the same card should be less than {SINGLE_CARD_MAX_NUM}, but got {self.card_num}!"
        raise ValueError(self.message)
