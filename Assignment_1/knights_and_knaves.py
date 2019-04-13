import re
initialization=input('Which text file do you want to use for the puzzle? ')
with open(initialization, 'r') as file:
    #得到所有的sirs
    fileString = file.readlines() #读取每一行文字
    if fileString == None or len(fileString) <= 0:
        print(None)
    passage=''
    dict={}
    for line in fileString:
        passage += line.strip() #变成连串的文字
        passage += ' '
    sentences = re.split(r'[.?!][\'\"]* *', passage) #分割出现。？！

    nameList=set()
    for row in sentences: #把sirs求出来
        if row != "": #如果一行不为空
            l = row.split(' ')
            for i in l[1:]:
                if ',' in i:#如果出现","替换成""
                    i = i.replace(",", "")
                if '\"' in i:
                    i = i.replace('\"', "")
                if i.istitle() and i != 'I' and i != 'Sirs' and i != 'Sir' and i != 'Knave' and i != 'Knight' and i != 'Knaves' and i != 'Knights':
                    nameList.add(i)
    nameList=sorted(nameList)
    print("The Sirs are:"," ".join(nameList))

    statement=''
    for line in fileString:
        statement += line.strip()
        statement += ' '
    statement=statement.replace("?",".")#?替换成.
    statement=statement.replace("!",".")#!替换成.
    statement=statement.replace(".\"","\".")#".替换成."
    statement=statement.split(".")#.分割完整的句子
    sirs_in_sentence=set()
    dict_of_speak = {}#说话的人以及所说的话，说的话会变成一个个单词

    for i in statement:
        if '"' in i: #如果statement出现引号
            front,sentence,back= i.split('"')
            split_sentence=sentence.split()
            for i in range(1, len(split_sentence)):
                if ',' in split_sentence[i]:
                    split_sentence[i] = split_sentence[i].replace(",", "")
                if split_sentence[i] != 'Sir' and split_sentence[i] != 'Sirs' and split_sentence[i] != 'Knave' \
                        and split_sentence[i] != 'Knight' and split_sentence[i] != 'Knaves' \
                        and split_sentence[i] != 'Knights' and split_sentence[i] != 'I' and split_sentence[i].istitle():
                    sirs_in_sentence.add(split_sentence[i])

            name_of_talking=None
            split_sentence=front.split() #front找说话的人
            for i in range(1,len(split_sentence)):
                if ',' in split_sentence[i]:
                    split_sentence[i] = split_sentence[i].replace(",", "")
                if split_sentence[i] != 'Sir' and split_sentence[i] != 'Sirs' and split_sentence[i] != 'Knave' \
                        and split_sentence[i] != 'Knight' and split_sentence[i] != 'Knaves' \
                        and split_sentence[i] != 'Knights' and split_sentence[i] != 'I' and split_sentence[i].istitle():
                    sirs_in_sentence.add(split_sentence[i])
                    name_of_talking=split_sentence[i]

            if not name_of_talking:
                split_sentence=back.split()#back后找说话的人
                for i in range(1,len(split_sentence)):
                    if ',' in split_sentence[i]:
                        split_sentence[i] = split_sentence[i].replace(",", "")
                    if split_sentence[i] != 'Sir' and split_sentence[i] != 'Sirs' and split_sentence[i] != 'Knave' \
                            and split_sentence[i] != 'Knight' and split_sentence[i] != 'Knaves' \
                            and split_sentence[i] != 'Knights' and split_sentence[i] != 'I' and split_sentence[i].istitle():
                        sirs_in_sentence.add(split_sentence[i])
                        name_of_talking=split_sentence[i]

            if name_of_talking not in dict_of_speak:#如果说话的人不在字典里
                dict_of_speak[name_of_talking] = [sentence.split()] #创立{说话的人：说的话}字典
            if name_of_talking in dict_of_speak:#如果说话的人在字典里
                if [sentence.split()]!=dict_of_speak[name_of_talking]:
                    dict_of_speak[name_of_talking].append(sentence.split())#创立{说话的人：说的话，说的话2}

    #求出所有相关的人
    role_involve = set()
    for name_of_talking in dict_of_speak:
        if len(role_involve) == len(nameList):#当前所涉及的人等于所有相关sirs的数量时
            break
        role_involve.add(name_of_talking) #相关的人加上说话的人
        for diff_sentence in dict_of_speak[name_of_talking]: #说话人所有的每一句话
            for i in range(len(diff_sentence)): #除掉逗号，
                if ',' in diff_sentence[i]:
                    diff_sentence[i] = diff_sentence[i].replace(",", "")
            if len(role_involve) == len(nameList):
                break
            for split_words in diff_sentence:   #把每一句话拆分成一个个单词
                if split_words in nameList:
                    role_involve.add(split_words)
                elif split_words == 'us':
                    role_involve = nameList
                    break
    role_involve=sorted(role_involve) #字母排序
    role_not_involve = list(set(nameList).difference(set(role_involve)))

    subject_index={} #主语配下标（二进制的第几位）e.g.{A:0, B:1, C:2, H:3}
    for i, name_of_talking in enumerate(role_involve): #下标从 0 开始给说话的人赋值
        subject_index[name_of_talking]=i

    roles_with_index = {} #{说话的人：涉及的人1的下标，涉及人2的下标} e.g.{A:[2,3],B:[1]}
    for name_of_talking in dict_of_speak: #说话的人
        for diff_sentence in dict_of_speak[name_of_talking]: #说话的人对应的句子
            for i in range(len(diff_sentence)): #除掉逗号，
                if ',' in diff_sentence[i]:
                    diff_sentence[i] = diff_sentence[i].replace(",", "")
            list_of_index=[] #寄存这句话提到了谁
            for split_words in diff_sentence: #说话的人对应的句子的一个个单词分割
                if split_words == 'us':
                    for i in nameList:
                        list_of_index.append(subject_index[i])
                elif split_words == 'I':  #如果提到I
                    list_of_index.append(subject_index[name_of_talking]) #把说话人的index加进list
                elif split_words in nameList: #如果这些分割的单词有出现sirs所有的name里面
                    list_of_index.append(subject_index[split_words]) #把这个split_word的index加进list
            if name_of_talking in roles_with_index: #如果说话的人在字典里了
                roles_with_index[name_of_talking].append(list_of_index) #{说话的人：涉及的人1的下标，涉及人2的下标}
            elif name_of_talking not in roles_with_index:#如果人不在字典里
                roles_with_index[name_of_talking]=[list_of_index]#{说话的人：涉及的人1的下标}
            for i in range(len(diff_sentence)):
                if ',' in diff_sentence[i]:
                    diff_sentence[i] = diff_sentence[i].replace(",", "")

    dict_of_knight = {} #说话的人：所说的话所涉及的knight或者knave
    for name_of_talking in dict_of_speak: #说话的人
        for diff_sentence in dict_of_speak[name_of_talking]: #说话的人对应的句子
            #print(diff_sentence)
            for i in range(len(diff_sentence)): #除掉逗号，
                if ',' in diff_sentence[i]:
                    diff_sentence[i] = diff_sentence[i].replace(",", "")
            if name_of_talking not in dict_of_knight: #如果人不在字典dict_of_knight里
                if 'Knaves' in diff_sentence or 'Knave' in diff_sentence:
                    dict_of_knight[name_of_talking] = [False]
                else:
                    dict_of_knight[name_of_talking] = [True]
            elif name_of_talking in dict_of_knight: #如果人已经在字典dict_of_knight里
                if 'Knaves' in diff_sentence or 'Knave' in diff_sentence:
                    dict_of_knight[name_of_talking].append(False)
                else:
                    dict_of_knight[name_of_talking].append(True)

    #count: 分别数一句话里多少个knight或者knave
    def is_true(solutions, role_related, sentence_of_role, kni_or_kna, names_of_speaking):
        count=0
        if kni_or_kna: #如果说话这个人说的这句话提到了knight,knights
            for i in role_related:
                if solutions[i] == '1':
                    count += 1
        else: #如果说话这个人说的这句话提到了knave,knaves
            for i in role_related:
                if solutions[i] == '0':
                    count += 1
        if 'one' in sentence_of_role:
            if 'exactly' in sentence_of_role or 'Exactly' in sentence_of_role and count==1: #exactly的情况,count等于1
                return True
            elif 'most' in sentence_of_role and count <= 1: #at most的情况 最多一个所以count小于等于1
                return True
            elif 'least' in sentence_of_role and count >= 1: #at least的情况 最少一个所以count大于等于一11
                return True
            return False
        else:
            if 'or' in sentence_of_role: #disjunction 'or'在分割的句子里
                if count > 0:
                    return True
                else:
                    return False
            else:
                if count == len(role_related): #I, all of us, and  (所有conjunction，因为出了上述的所有情况) 所有的人同真同假
                    return True
                else:
                    return False

    #solutions:传入的二进制，可能的reslut
    #roles_with_index[a][i]:说话的人说的话涉及的人在二进制里的下标
    #dict_of_speak[a][i]：说话的人说的话
    #dict_of_knight[a][i]: 说话的人说的这句话是有关knight还是knave的
    #a speaker, e.g.: Andrew
    def evaluate(solutions):
        for a in dict_of_speak: #字典的键，说话的人
            for i in range(len(dict_of_speak[a])):
                each_role_index = subject_index[a] #每个人对应的下标
                if solutions[each_role_index] == '0': #说假话的人说了真话，返回false
                    if is_true(solutions, roles_with_index[a][i], dict_of_speak[a][i], dict_of_knight[a][i], a) == True: #如果knave 说了真话 返回false
                       return False
                elif solutions[each_role_index] == '1':  #说真话的人说了假话，返回false
                    if is_true(solutions, roles_with_index[a][i], dict_of_speak[a][i], dict_of_knight[a][i], a) == False:  # 如果knight 说了假 返回false
                        return False
        return True

    #求涉及的人数的二进制
    #检测所有的solution是否正确
    # result：用来存所有的solution
    result = []
    num_of_role_involve = len(role_involve)
    for i in range(2 ** num_of_role_involve):
        if evaluate(f"{i:0{num_of_role_involve}b}"):
            result.append(f"{i:0{num_of_role_involve}b}")

    #len(result)相当于result里存放的结果的数量
    if len(result) == 1 and len(role_not_involve)== 0: #如果有没被提到的人 一定不止一个result
        print("There is a unique solution:")
        for name in nameList: #遍历所有的sirs
            if result[0][subject_index[name]] == '1': #reslut里存的二进制的第[对应这个人所对应的下标]得到的是1说明这个人是knight
                print(f'Sir {name} is a Knight.')
            if result[0][subject_index[name]] == '0':#reslut里存的二进制的第[对应这个人所对应的下标]得到的是0说明这个人是knight
                print(f'Sir {name} is a Knave.')
    elif len(result) == 0: #如果数量=0
        print("There is no solution.")
    else:
        num_of_solutions = len(result) * (2 ** len(role_not_involve))
        print(f'There are {num_of_solutions} solutions.')
        

