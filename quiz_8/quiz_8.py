import re  # split() suffices though
from collections import defaultdict
from copy import deepcopy


class Polynomial:
    def __init__(self, polynomial=None):
        self.polynomial = polynomial
        self.dic = defaultdict()
        if polynomial is not None:
            split_words = polynomial.split()
            powers = []
            coeffs = []
            self.dic = defaultdict()
            for i in range(len(split_words)):
                if 'x^' in split_words[i]:  # 找出 数字x^数字
                    # print('这里是x次方', split_words[i])
                    if '-' in split_words[i]:
                        if i == 0:  # 如果位置是第0个
                            candp = split_words[i].split('x^')
                            coeff = candp[0]
                            coeff = int(coeff)
                            coeffs.append(coeff)
                            power = candp[1]
                            power = int(power)
                            powers.append(power)
                    else:
                        candp = split_words[i].split('x^')
                        coeff = candp[0]
                        if coeff == '':
                            if '-' in split_words[i - 1]:
                                coeffs.append(-1)
                            else:
                                coeffs.append(1)
                        else:
                            coeff = int(coeff)
                            if '-' in split_words[i - 1]:
                                coeff = -coeff
                                coeffs.append(coeff)
                            else:
                                coeffs.append(coeff)
                        power = candp[1]
                        power = int(power)
                        powers.append(power)
                elif 'x' in split_words[i] and 'x^' not in split_words[i]:  # 找出 数字x
                    coeff = split_words[i].split('x')
                    coeff = coeff[0]
                    if coeff == '':
                        if '-' in split_words[i - 1]:
                            coeffs.append(-1)
                        else:
                            coeffs.append(1)
                    else:
                        if coeff == '-':
                            coeffs.append(-1)
                            powers.append(1)
                        else:
                            coeff = int(coeff)
                        if '-' in split_words[i - 1]:
                            if len(split_words)==1:
                                if 1 in coeffs or -1 in coeffs:
                                    continue
                                else:
                                    coeffs.append(coeff)
                                    powers.append(1)
                            else:
                                coeff = -coeff
                                coeffs.append(coeff)
                        else:
                            coeffs.append(coeff)
                    powers.append(1)
                elif '+' not in split_words[i] and len(split_words) == 1:  # p=-2
                    coeff = int(split_words[i])
                    coeffs.append(coeff)
                    powers.append(0)
                elif '-' not in split_words[i] and '+' not in split_words[i]:  # 找出 数字x
                    if '-' in split_words[i - 1]:
                        coeff = -int(split_words[i])
                        coeffs.append(coeff)
                        powers.append(0)
                    else:
                        coeff = int(split_words[i])
                        coeffs.append(coeff)
                        powers.append(0)
            self.dic = dict(zip(powers, coeffs))
            self.polynomial = self.dic

    def __str__(self):
        self.dic = sorted(self.dic.items(), key=lambda x: x[0], reverse=True)
        self.dic = dict(self.dic)
        get_polynomial = 0
        if self.dic == {}:
            return f'{get_polynomial}'
        else:
            list_of_str = []
            for powers, coeffs in self.dic.items():
                if powers == 0:
                    if (coeffs * -1) < 0:
                        coeffs = '+ ' + str(coeffs)
                    else:
                        coeffs = str(coeffs)
                    list_of_str.append(coeffs)
                elif powers == 1:
                    if coeffs == 0:
                        t = '0'
                        list_of_str.append(t)
                    elif coeffs == -1:
                        t = '- x'
                        list_of_str.append(t)
                    elif coeffs == 1:
                        t = 'x'
                        list_of_str.append(t)
                    elif coeffs > 1:
                        t = '+ ' + str(coeffs) + 'x'
                        list_of_str.append(t)
                    elif coeffs < 1:
                        t = str(coeffs) + 'x'
                        list_of_str.append(t)

                elif powers > 1:
                    if coeffs > 0:
                        if coeffs == 1:
                            t = '+ ' + 'x^' + str(powers)
                        else:
                            t = '+ ' + str(coeffs) + 'x^' + str(powers)
                        list_of_str.append(t)
                    if coeffs < 0:
                        if coeffs == -1:
                            t = '-x^' + str(powers)
                        else:
                            t = str(coeffs) + 'x^' + str(powers)
                        list_of_str.append(t)
        list_of_str = " ".join(list_of_str)
        #print(len(list_of_str),'666')
        if list_of_str =='- x':
            list_of_str = '-x'
        list_of_str = list_of_str.replace("-", "- ")
        if list_of_str[0] == '+':
            list_of_str = list_of_str[2:]
        if list_of_str[0] == '-':
            list_of_str = '-' + list_of_str[2:]
        if '-  ' in list_of_str:
            list_of_str = list_of_str.replace("-  ", "- ")

        return list_of_str

    def __add__(self, other):
        p = Polynomial()
        # dictionary = deepcopy(self.polynomial)
        for keys, values in other.dic.items():
            if keys in self.dic:
                p.dic[keys] = other.dic[keys] + self.dic[keys]
            else:
                p.dic[keys] = other.dic[keys]
        return p

    def __mul__(self, other):
        p = Polynomial()
        for keys_1, values_1 in other.dic.items():
            for keys_2, values_2 in self.dic.items():
                powers = keys_1 + keys_2
                coeffs = values_1 * values_2
                if powers in p.dic:
                    p.dic[powers] += coeffs
                else:
                    p.dic[powers] = coeffs
        return p

    def __sub__(self, other):
        p = Polynomial()
        for keys, values in other.dic.items():
            if keys in self.dic:
                p.dic[keys] = self.dic[keys] - other.dic[keys]
            else:
                p.dic[keys] = -other.dic[keys]
        return p

