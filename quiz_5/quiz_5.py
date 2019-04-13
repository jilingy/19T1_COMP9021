# Prompts the user for a positive integer that codes a set S as follows:
# - Bit 0 codes 0
# - Bit 1 codes -1
# - Bit 2 codes 1
# - Bit 3 codes -2
# - Bit 4 codes 2
# - Bit 5 codes -3
# - Bit 6 codes 3
# ...
# Computes a derived positive integer that codes the set of running sums
# ot the members of S when those are listed in increasing order.
#
# Written by *** and Eric Martin for COMP9021


from itertools import accumulate
import sys

try:
    encoded_set = int(input('Input a positive integer: '))
    if encoded_set < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

#建立字典 例如：
#Bit 0 codes 0
#Bit 1 codes -1
#Bit 2 codes 1
#......
#如果是偶数就是减
#如果是奇数就是加
def creating_dic(encoded_set):
    dict_codes = {}
    binum = f'{encoded_set:b}'
    l = len(binum)
    for i in range(l):
        dict_codes[-1] = 0
        if i % 2 == 0:
            dict_codes[i] = dict_codes[i - 1] - (-i)
        else:
            dict_codes[i] = dict_codes[i - 1] + (-i)
    dict_codes.pop(-1)
    return dict_codes

#二进制反方向写
#如果出现 1 在二进制上，在字典字典里取到相应的值
def get_result(encoded_set):
    binum = f'{encoded_set:b}'
    l = len(binum)
    reverse_binum = binum[::-1]
    result = []
    for i in range(l):
        if reverse_binum[i] == '1':
            result.append(creating_dic(encoded_set)[i])
    result = sorted(result)
    return result

#按规定的格式输出
def display_encoded_set(encoded_set):
    new_result = map(lambda x: str(x), get_result(encoded_set))  # 如果list中不是字符串，而是数字,转换成str
    str_list = ', '.join(new_result)
    print('{' + str_list + '}')


def code_derived_set(encoded_set):
    encoded_running_sum = 0
    derived_encoded_set = []
    num_list_new = []
    has_one = []  # 下标存着1的角标
    new_dict = {}  # 把字典反过来 值对下标
    binumber = 0 # 二进制
    sum = 0
    t = 0
    # 为了 123 例子可能出现key没有-6的情况， 所以加了1000
    dict1 = {}
    binum = f'{encoded_set:b}'
    l = len(binum)
    for i in range(l+1000):
        dict1[-1] = 0
        if i % 2 == 0:
            dict1[i] = dict1[i - 1] - (-i)
        else:
            dict1[i] = dict1[i - 1] + (-i)
    dict1.pop(-1)

    for i in get_result(encoded_set):
        sum = t + i
        t = sum
        derived_encoded_set.append(sum)
    derived_encoded_set = set(derived_encoded_set)
    derived_encoded_set = sorted(derived_encoded_set)
    new_dict = {values: keys for keys, values in dict1.items()} #字典keys,values 倒转
    for i in derived_encoded_set:
        has_one.append(new_dict[i])
    has_one = sorted(has_one) #has_one:有1的位数
    length = len(has_one)
    if length == 0:
        encoded_running_sum = 0
    else:
        max_length = has_one[length - 1]
        zerolist = f'{0:0{max_length + 1}}'
        lista = list(zerolist) #把字符串00000...变成list: 0000...
        for i in has_one:
            lista[i] = 1
        num_list_new = [str(x) for x in lista] #含有int的list变成string
        num_list_new = num_list_new[::-1] #翻转
        "".join(num_list_new)
        encoded_running_sum = int("".join(num_list_new), 2)
    return encoded_running_sum

print('The encoded set is: ', end='')
display_encoded_set(encoded_set)
encoded_running_sum = code_derived_set(encoded_set)
print('The derived encoded set is: ', end='')
display_encoded_set(encoded_running_sum)
print('  It is encoded by:', encoded_running_sum)

