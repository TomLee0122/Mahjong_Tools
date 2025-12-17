import copy

CURRENT_CARD_NUM = 13
SINGLE_CARD_MAX_NUM = 4
CARDS = ['0m', '1m', '2m', '3m', '4m', '5m', '6m', '7m', '8m', '9m', '0p', '1p', '2p', '3p', '4p', '5p', '6p', '7p',
         '8p', '9p', '0s', '1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', '1z', '2z', '3z', '4z', '5z', '6z', '7z']
ONE_NINE_CARDS = ['1m', '9m', '1s', '9s', '1p',
                  '9p', '1z', '2z', '3z', '4z', '5z', '6z', '7z']
NONE_ONE_NINE_CARDS = copy.copy(CARDS)
for current_cards in ONE_NINE_CARDS:
    NONE_ONE_NINE_CARDS.remove(current_cards)
