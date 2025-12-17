import os
import copy
from constants import CURRENT_CARD_NUM, SINGLE_CARD_MAX_NUM
import errors
import utilities


class Mahjong_Cards():
    # Read the cards in
    def __init__(self):
        self.p_cards = utilities.initialize_card_dict('p')
        self.p_card_num = 0
        self.m_cards = utilities.initialize_card_dict('m')
        self.m_card_num = 0
        self.s_cards = utilities.initialize_card_dict('s')
        self.s_card_num = 0
        self.z_cards = utilities.initialize_card_dict('z')
        self.z_card_num = 0
        self.raw_card_string = None
        self.card_list = None
        self.card_count = None

    def check_correctness_cards(self):
        if self.card_count != CURRENT_CARD_NUM:
            raise errors.Mahjong_Card_Num_Error(self.card_count)
        for current_check_type in [self.p_cards, self.m_cards, self.s_cards, self.z_cards]:
            temp_length = len(current_check_type)
            for i in range(temp_length):
                if current_check_type[i] > SINGLE_CARD_MAX_NUM:
                    raise errors.Single_Card_Num_Error(current_check_type[i])

    def read_cards(self, raw_card_string: str, check: bool = True):
        self.raw_card_string = raw_card_string
        self.card_list = raw_card_string.split(' ')
        self.card_count = len(self.card_list)

        for current_cards in self.card_list:
            current_card_type = current_cards[-1]
            try:
                current_card_number = int(current_cards[:-1])
            except ValueError:
                if check:
                    raise errors.Undefined_Mahjong_Card_Error(current_cards)
                else:
                    continue

            if current_card_type == 'p':
                if check and (current_card_number > 9 or current_card_number < 0):
                    raise errors.Undefined_Mahjong_Card_Error(
                        str(current_card_number)+current_card_type)
                self.p_cards[current_card_number] += 1
                self.p_card_num += 1
                continue
            if current_card_type == 'm':
                if check and (current_card_number > 9 or current_card_number < 0):
                    raise errors.Undefined_Mahjong_Card_Error(
                        str(current_card_number)+current_card_type)
                self.m_cards[current_card_number] += 1
                self.m_card_num += 1
                continue
            if current_card_type == 's':
                if check and (current_card_number > 9 or current_card_number < 0):
                    raise errors.Undefined_Mahjong_Card_Error(
                        str(current_card_number)+current_card_type)
                self.s_cards[current_card_number] += 1
                self.s_card_num += 1
                continue
            if current_card_type == 'z':
                if check and (current_card_number > 9 or current_card_number < 0):
                    raise errors.Undefined_Mahjong_Card_Error(
                        str(current_card_number)+current_card_type)
                self.z_cards[current_card_number] += 1
                self.z_card_num += 1
                continue
            if check:
                raise errors.Undefined_Mahjong_Card_Error(current_card_type)

        if check:
            self.check_correctness_cards()

        self.p_cards[5] += self.p_cards[0]
        self.m_cards[5] += self.m_cards[0]
        self.s_cards[5] += self.s_cards[0]

        self.card_info = {'p': self.p_cards, 'm': self.m_cards,
                          's': self.s_cards, 'z': self.z_cards}

    def check_which_tenpai_on(self, card_type: str, check_type: str = 'com_w_pair'):
        assert card_type in ['p', 'm', 's', 'z']
        assert check_type in ['com', 'com_w_pair']
        tenpai_on_list = []
        for current_card in self.card_info[card_type]:
            temp_card_dict = copy.copy(self.card_info[card_type])
            temp_card_dict[current_card] += 1
            if check_type == 'com':
                if utilities.check_if_complete_set(temp_card_dict, card_type, None)[check_type]:
                    tenpai_on_list.append(str(current_card) + card_type)
            else:
                if utilities.check_if_complete_set(temp_card_dict, card_type, None)[check_type][0]:
                    tenpai_on_list.append(str(current_card) + card_type)
        return tenpai_on_list

    def check_if_tenpai(self):
        self.p_status = utilities.check_if_complete_set(self.p_cards, 'p')
        self.m_status = utilities.check_if_complete_set(self.m_cards, 'm')
        self.s_status = utilities.check_if_complete_set(self.s_cards, 's')
        self.z_status = utilities.check_if_complete_set(self.z_cards, 'z')
        self.status_dict = {
            'p': self.p_status, 'm': self.m_status, 's': self.s_status, 'z': self.z_status}
        self.tenpai_status = {'incom': [], 'com': [], 'com_w_pair': []}

        for current_status in list(self.status_dict.items()):
            if current_status[1]['incom']:
                self.tenpai_status['incom'].append(current_status[0])
            if current_status[1]['com']:
                self.tenpai_status['com'].append(current_status[0])
            if current_status[1]['com_w_pair'][0]:
                self.tenpai_status['com_w_pair'].append(current_status[0])

        self.incom_count = len(self.tenpai_status['incom'])
        self.com_count = len(self.tenpai_status['com'])
        self.com_w_pair_count = len(self.tenpai_status['com_w_pair'])

        if self.incom_count == 0 and self.com_w_pair_count == 2:
            tenpai_list_1 = self.check_which_tenpai_on(
                self.tenpai_status['com_w_pair'][0], check_type='com')
            tenpai_list_2 = self.check_which_tenpai_on(
                self.tenpai_status['com_w_pair'][1], check_type='com')
            return [True, tenpai_list_1+tenpai_list_2]
        if self.incom_count == 1 and self.com_w_pair_count == 0:
            tenpai_list_1 = self.check_which_tenpai_on(
                self.tenpai_status['incom'][0], check_type='com_w_pair')
            if len(tenpai_list_1) >= 1:
                return [True, tenpai_list_1]
        if self.incom_count == 1 and self.com_w_pair_count == 1:
            tenpai_list_1 = self.check_which_tenpai_on(
                self.tenpai_status['incom'][0], check_type='com')
            if len(tenpai_list_1) >= 1:
                return [True, tenpai_list_1]
        return [False]


if __name__ == '__main__':
    example_1 = '1m 1m 1m 2m 3m 4m 5m 6m 7m 7m 9m 9m 9m'
    my_cards = Mahjong_Cards()
    my_cards.read_cards(example_1)
    print(my_cards.check_which_tenpai_on('m', check_type='com_w_pair'))
