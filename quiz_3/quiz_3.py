# Written by Eric Martin for COMP9021



import sys
from random import seed, randint, randrange


try:
    arg_for_seed, upper_bound, length =\
            (int(x) for x in input('Enter three integers: ').split())
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()


def length_of_longest_increasing_sequence(L):
	L1=L+L #To connect two list
	l=len(L)
	l1=len(L1)
	increasing_length = 1
	max_increasing_length = 0
	if l<=1:
		return l
	for i in range(l1-3):
		if L1[i+1] >= L1[i]: 
			increasing_length = increasing_length + 1 #current max increasing length 
		else:
			increasing_length = 1
			
		if increasing_length > max_increasing_length:
			max_increasing_length = increasing_length
		if max_increasing_length >= l: #if all elements are same, return the length of L
			return l
	return max_increasing_length

def max_int_jumping_in(L):
	l=len(L)
	if l<=0:
		return l
	str1=""
	dic1={}
	biggest = 0
	biggest = L[0]
	
	for i in range(l):
		str1=str(L[i])
		dic1={}
		dic1[str(L[i])]=i #viewed str(L[i]) as a key
		while(str1!=""):
			i=L[i]
			if(str(L[i]) not in dic1.keys()) and (i not in dic1.values()):
				str1=str1+str(L[i])
				dic1[str(L[i])]=i
			elif(i in dic1.values()):
				break
			else:
				str1=str1+str(L[i])
				break
		if(int(str1)>biggest):
			biggest=int(str1)
	return biggest
	
seed(arg_for_seed)
L_1 = [randint(0, upper_bound) for _ in range(length)]
print('L_1 is:', L_1)
print('The length of the longest increasing sequence\n'
      '  of members of L_1, possibly wrapping around, is:',
      length_of_longest_increasing_sequence(L_1), end = '.\n\n'
     )
L_2 = [randrange(length) for _ in range(length)]
print('L_2 is:', L_2)
print('The maximum integer built from L_2 by jumping\n'
      '  as directed by its members, from some starting member\n'
      '  and not using any member more than once, is:',
      max_int_jumping_in(L_2)
     )


