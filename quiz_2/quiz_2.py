# Written by *** and Eric Martin for COMP9021


def rule_encoded_by(rule_nb):
    '''
    "rule_nb" is supposed to be an integer between 0 and 15.
    '''
    values = [int(d) for d in f'{rule_nb:04b}']
    return {(p // 2, p % 2): values[p] for p in range(4)}

def describe_rule(rule_nb):
    '''
    "rule_nb" is supposed to be an integer between 0 and 15.
    '''
    rule = rule_encoded_by(rule_nb)
    print('The rule encoded by', rule_nb, 'is: ', rule)
    print()

    for key,value in rule.items():
        print('After','{}'.format(key[0]),'followed by','{}'.format(key[1])+',','we draw',value)
    # INSERT YOUR CODE HERE TO PRINT 4 LINES


def draw_line(rule_nb, first, second, length):
    '''
    "rule_nb" is supposed to be an integer between 0 and 15.
    "first" and "second" are supposed to be the integer 0 or the integer 1.
    "length" is supposed to be a positive integer (possibly equal to 0).

    
    Draws a line of length "length" consisting of 0's and 1's,
    that starts with "first" if "length" is at least equal to 1,
    followed by "second" if "length" is at least equal to 2,
    and with the remaining "length" - 2 0's and 1's determined by "rule_nb".
    '''
    rule = rule_encoded_by(rule_nb)
    list=""
    for i in range(length):
        if i==0:
            list+=str(first)
            #print(str(first), end='')
        elif i==1:
            list+=str(second)
            #print(str(second), end='')
        elif i>=2:
	        list+=str(rule[(int(list[i-2]),int(list[i-1]))])
    print(list)
		
def uniquely_produced_by_rule(line):
    '''
    "line" is assumed to be a string consisting of nothing but 0's and 1's.

    Returns an integer n between 0 and 15 if the rule encoded by n is the
    UNIQUE rule that can produce "line"; otherwise, returns -1.
    '''
    length = len(line)
    if len(line) < 6:
        return -1
    list=[0]*16
    count=0
    for j in range(16): 
        for i in range(2,length): 
            rule = rule_encoded_by(j)
            if line[i]!= str(rule[(int(line[i-2]),int(line[i-1]))]):
                break
            elif i==length-1 and line[i]== str(rule[(int(line[i-2]),int(line[i-1]))]):
                list[count]=j
                count=count+1
                break
            else:
                continue
    if count==0 or count>1:
        return -1
    else:
        return list[0]

