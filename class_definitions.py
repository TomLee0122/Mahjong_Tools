import os
import copy
from constants import CURRENT_CARD_NUM, SINGLE_CARD_MAX_NUM
import errors
import utilities


class Mahjong_Cards():
    # Read the cards in
    def __init__(self, separator: str = ' ') -> None:
        self.separator = separator
        self.card_info = {'p': utilities.initialize_card_dict('p'), 'm': utilities.initialize_card_dict(
            'm'), 's': utilities.initialize_card_dict('s'), 'z': utilities.initialize_card_dict('z')}
        self.num_info = {'p': 0, 'm': 0, 's': 0, 'z': 0}
        return

    def check_correctness_cards(self) -> None:
        if self.card_count != CURRENT_CARD_NUM:
            raise errors.Mahjong_Card_Num_Error(self.card_count)
        for current_check_type in self.card_info.values():
            temp_length = len(current_check_type)
            for i in range(temp_length):
                if current_check_type[i] > SINGLE_CARD_MAX_NUM:
                    raise errors.Single_Card_Num_Error(current_check_type[i])
        return

    def read_cards(self, raw_card_string: str, check: bool = True) -> None:
        self.raw_card_string = raw_card_string
        self.card_list = raw_card_string.split(self.separator)
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

            if current_card_number > 9 or current_card_number < 0 or current_card_type not in ['p', 'm', 's', 'z']:
                if check:
                    raise errors.Undefined_Mahjong_Card_Error(current_cards)
            else:
                self.card_info[current_card_type][current_card_number] += 1
                self.num_info[current_card_type] += 1

        if check:
            self.check_correctness_cards()

        self.card_info['p'][5] += self.card_info['p'][0]
        self.card_info['m'][5] += self.card_info['m'][0]
        self.card_info['s'][5] += self.card_info['s'][0]

        return

    def check_which_tenpai_on(self, card_type: str, check_type: str) -> list[str]:
        assert card_type in ['p', 'm', 's', 'z']
        assert check_type in ['com', 'com_w_pair']
        tenpai_on_list = []
        for current_card in self.card_info[card_type]:
            self.card_info[card_type][current_card] += 1
            if check_type == 'com':
                if utilities.check_if_complete_set(self.card_info[card_type], card_type)[check_type]:
                    tenpai_on_list.append(str(current_card) + card_type)
            else:
                if utilities.check_if_complete_set(self.card_info[card_type], card_type)[check_type][0]:
                    tenpai_on_list.append(str(current_card) + card_type)
            self.card_info[card_type][current_card] -= 1
        return tenpai_on_list

    def check_if_tenpai(self) -> list:
        p_status = utilities.check_if_complete_set(
            self.card_info['p'], 'p')
        m_status = utilities.check_if_complete_set(
            self.card_info['m'], 'm')
        s_status = utilities.check_if_complete_set(
            self.card_info['s'], 's')
        z_status = utilities.check_if_complete_set(
            self.card_info['z'], 'z')

        status_dict = {
            'p': p_status, 'm': m_status, 's': s_status, 'z': z_status}
        tenpai_status = {'incom': [], 'com': [], 'com_w_pair': []}

        for card_type, status in status_dict.items():
            if status['incom']:
                tenpai_status['incom'].append(card_type)
            if status['com']:
                tenpai_status['com'].append(card_type)
            if status['com_w_pair'][0]:
                tenpai_status['com_w_pair'].append(card_type)
        incom_count = len(tenpai_status['incom'])
        # com_count = len(tenpai_status['com'])
        com_w_pair_count = len(tenpai_status['com_w_pair'])

        if incom_count == 0 and com_w_pair_count == 2:
            tenpai_list_1 = self.check_which_tenpai_on(
                tenpai_status['com_w_pair'][0], check_type='com')
            tenpai_list_2 = self.check_which_tenpai_on(
                tenpai_status['com_w_pair'][1], check_type='com')
            return [True, tenpai_list_1+tenpai_list_2]

        if incom_count == 1 and com_w_pair_count == 0:
            tenpai_list_1 = self.check_which_tenpai_on(
                tenpai_status['incom'][0], check_type='com_w_pair')
            if tenpai_list_1:
                return [True, tenpai_list_1]

        if incom_count == 1 and com_w_pair_count == 1:
            tenpai_list_1 = self.check_which_tenpai_on(
                tenpai_status['incom'][0], check_type='com')
            if tenpai_list_1:
                return [True, tenpai_list_1]

        return [False]


if __name__ == '__main__':
    # example_1 = "1m 1m 2m 2m 3s 4s 5s 6p 7p 8p 9p 9p 9p"
    example_1 = "1m 1m 1m 2m 3m 4m 5m 6m 7m 8m 9m 9m 9m"
    my_cards = Mahjong_Cards()
    my_cards.read_cards(example_1)
    print(my_cards.check_which_tenpai_on('m', check_type='com_w_pair'))
