# Uses Heath Nutrition and Population statistics,
# stored in the file HNP_Data.csv.gz,
# assumed to be located in the working directory.
# Prompts the user for an Indicator Name. If it exists and is associated with
# a numerical value for some countries or categories, for some the years 1960-2015,
# then finds out the maximum value, and outputs:
# - that value;
# - the years when that value was reached, from oldest to more recents years;
# - for each such year, the countries or categories for which that value was reached,
#   listed in lexicographic order.
# 
# Written by *** and Eric Martin for COMP9021


import sys
import os
import csv
import gzip


filename = 'HNP_Data.csv.gz'
if not os.path.exists(filename):
    print(f'There is no file named {filename} in the working directory, giving up...')
    sys.exit()

indicator_of_interest = input('Enter an Indicator Name: ')

first_year = 1960
number_of_years = 56
max_value = None
countries_for_max_value_per_year = {}

with gzip.open(filename) as csvfile:
    file = csv.reader(line.decode('utf8').replace('\0', '') for line in csvfile)    
    dictionary={}
    for row in file:
        if len(row) == 0:#排除空行
            continue
        if row[2] == indicator_of_interest: #判断输入的字符和第三行的数据是否相等，若相等：
            for i in range(number_of_years): #遍历56年
                if row[4 + i] == '':
                    continue
                float_value = float(row[4 + i])
                max_year=first_year+i #遍历所有年份
                if max_year not in dictionary.keys(): #如果年份不在字典的键里里
                    dictionary[max_year]=float_value,[row[0]] #字典赋值
                elif float_value > dictionary[max_year][0]:#如果下一个年份里所存储的值大于字典的值
                    dictionary[max_year] = float_value, [row[0]]
                elif float_value==dictionary[max_year][0]: #如果所在年份里存储的值等于字典里的值，同一个国家在不同年份有两个相同的最大值
                    dictionary[max_year][1].append(row[0]) #在国家后再加上国家
                else:
                    continue

    if dictionary is not None: #如果字典非空
        value = max((dictionary[max_year][0] for max_year in dictionary),default=None)#最大的年份复制给第一个值，如果为空则value=空
        if value == None:
            max_value=None
        elif int(value) == float(value):
            max_value=int(value)
        else:
            max_value =float(value)
        for max_year in dictionary:
            if dictionary[max_year][0] == max_value:
                countries_for_max_value_per_year[max_year] = sorted(dictionary[max_year][1])
				
if max_value is None:
    print('Sorry, either the indicator of interest does not exist or it has no data.')
else:
    print('The maximum value is:', max_value)
    print('It was reached in these years, for these countries or categories:')
    print('\n'.join(f'    {year}: {countries_for_max_value_per_year[year]}'
                                  for year in sorted(countries_for_max_value_per_year)
                   )
         )
