import class_definitions

if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        raw_cards_string = file.read().replace('\n', '')
        my_cards = class_definitions.Mahjong_Cards()
        my_cards.read_cards(raw_card_string=raw_cards_string)
        print(my_cards.check_if_tenpai())
