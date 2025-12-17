import errors
import copy

INITIAL_COMPLETE_STATUS = {'incom': False,
                           'com': False, 'com_w_pair': [False, []]}


def initialize_card_dict(card_type: str):
    if card_type not in ['p', 'm', 's', 'z']:
        raise errors.Undefined_Mahjong_Card_Error(card_type)
    if card_type in ['p', 'm', 's']:
        return {i: 0 for i in range(0, 10)}
    else:
        return {i: 0 for i in range(0, 8)}


def initialize_complete_status():
    return copy.deepcopy(INITIAL_COMPLETE_STATUS)


def incomplete_operator(complete_status: dict):
    assert complete_status.keys() == {'incom', 'com', 'com_w_pair'}
    complete_status['incom'] = True
    complete_status['com'] = False
    complete_status['com_w_pair'] = [False, []]
    return complete_status

# Use depth-first search to check if the card set is complete


def check_if_complete_set(card_dict: dict, card_type: str) -> dict:
    complete_status = initialize_complete_status()
    if card_type not in ['p', 'm', 's', 'z']:
        raise errors.Undefined_Mahjong_Card_Error(card_type)
    card_num = 0
    for i in card_dict:
        card_num += card_dict[i]
    if card_num == 0:
        if not complete_status['com_w_pair'][0]:
            complete_status['com'] = True
        return complete_status
    if card_num % 3 == 1:
        complete_status = incomplete_operator(complete_status)
        return complete_status
    # Find the first non-zero number card
    i = 1
    while card_dict[i] == 0:
        i += 1

    if card_type == 'z':
        if card_dict[i] == 1:
            complete_status = incomplete_operator(complete_status)
            return complete_status
        elif card_dict[i] == 2:
            card_dict[i] -= 2
            temp_complete_status = check_if_complete_set(
                card_dict, card_type)
            card_dict[i] += 2
            if temp_complete_status['com']:
                complete_status['com_w_pair'][0] = True
                complete_status['com_w_pair'][1].append(i)
            else:
                complete_status = incomplete_operator(complete_status)
            return complete_status
        else:
            card_dict[i] -= 3
            temp_complete_status = check_if_complete_set(
                card_dict, card_type)
            card_dict[i] += 3
            if temp_complete_status['com']:
                complete_status['com'] = True
            elif temp_complete_status['com_w_pair'][0]:
                complete_status['com_w_pair'][0] = True
                complete_status['com_w_pair'][1] += temp_complete_status['com_w_pair'][1]
            else:
                complete_status = incomplete_operator(complete_status)
            return complete_status
    else:
        if card_num % 3 == 0:
            if card_dict[i] >= 3:
                card_dict[i] -= 3
                temp_complete_status = check_if_complete_set(
                    card_dict, card_type)
                card_dict[i] += 3
                if temp_complete_status['com']:
                    complete_status['com'] = True
                    return complete_status
            if i <= 7 and card_dict[i+1] >= 1 and card_dict[i+2] >= 1:
                card_dict[i] -= 1
                card_dict[i+1] -= 1
                card_dict[i+2] -= 1
                temp_complete_status = check_if_complete_set(
                    card_dict, card_type)
                card_dict[i] += 1
                card_dict[i+1] += 1
                card_dict[i+2] += 1
                if temp_complete_status['com']:
                    complete_status['com'] = True
                    return complete_status
            complete_status = incomplete_operator(complete_status)
            return complete_status
        # card_num % 3 == 2
        else:
            if card_dict[i] >= 3:
                card_dict[i] -= 3
                temp_complete_status = check_if_complete_set(
                    card_dict, card_type)
                card_dict[i] += 3
                if temp_complete_status['com_w_pair'][0]:
                    complete_status['com_w_pair'][0] = True
                    complete_status['com_w_pair'][1] += temp_complete_status['com_w_pair'][1]
            if card_dict[i] >= 2:
                card_dict[i] -= 2
                temp_complete_status = check_if_complete_set(
                    card_dict, card_type)
                card_dict[i] += 2
                if temp_complete_status['com']:
                    complete_status['com_w_pair'][0] = True
                    complete_status['com_w_pair'][1].append(i)
            if card_dict[i] >= 1:
                if i <= 7 and card_dict[i+1] >= 1 and card_dict[i+2] >= 1:
                    card_dict[i] -= 1
                    card_dict[i+1] -= 1
                    card_dict[i+2] -= 1
                    temp_complete_status = check_if_complete_set(
                        card_dict, card_type)
                    card_dict[i] += 1
                    card_dict[i+1] += 1
                    card_dict[i+2] += 1
                    if temp_complete_status['com_w_pair'][0]:
                        complete_status['com_w_pair'][0] = True
                        complete_status['com_w_pair'][1] += temp_complete_status['com_w_pair'][1]
            if complete_status['com_w_pair'][0]:
                complete_status['incom'] = False
                complete_status['com_w_pair'][1] = list(
                    set(complete_status['com_w_pair'][1]))
            else:
                complete_status = incomplete_operator(complete_status)
            return complete_status


if __name__ == '__main__':
    # example_1 = {i: 0 for i in range(1, 8)}
    # example_1[2] = 3
    # example_1[3] = 3
    # example_1[4] = 2
    # example_1[6] = 3
    # print(check_if_complete_set(example_1, 'z'))
    example_2 = {i: 0 for i in range(10)}
    example_2[1] = 3
    example_2[2] = 1
    example_2[3] = 1
    example_2[8] = 3
    print(check_if_complete_set(example_2, 's'))
    # example_3 = {i: 0 for i in range(1, 10)}
    # example_3[1] = 4
    # example_3[2] = 1
    # example_3[3] = 1
    # example_3[4] = 1
    # example_3[5] = 1
    # example_3[6] = 1
    # example_3[7] = 1
    # example_3[8] = 1
    # example_3[9] = 3
    # print(check_if_complete_set(example_3, 'm'))
