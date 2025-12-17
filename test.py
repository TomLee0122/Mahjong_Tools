import copy

INITIAL_COMPLETE_STATUS = {'incom': False,
                           'com': False, 'com_w_pair': [False, []]}


def test_function_1(complete_status: dict):
    complete_status['com_w_pair'][1] = [1, 2]
    return complete_status


print(int('2s'))
test_dict = {1: 1, 3: 2}
print(type(list(test_dict.keys())[0]), list(test_dict.items()))
print(len(test_dict))
print(6 % 3)
print([1, 2]+[2, 1])

test_dict_1 = copy.deepcopy(INITIAL_COMPLETE_STATUS)
test_dict_1['com_w_pair'][1] = [1, 2]
print(INITIAL_COMPLETE_STATUS, test_dict_1)

test_function_1(copy.deepcopy(INITIAL_COMPLETE_STATUS))
print(INITIAL_COMPLETE_STATUS)
for name in test_dict:
    print(name)
