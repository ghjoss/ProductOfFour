import itertools
def unique_combinations(items):
	unique_combinations = []
	for r in range(1, len(items) + 1):
		combinations = itertools.combinations(items, r)
		unique_combinations.extend(combinations)
	# print(f'uc2{combinations})')
	return list(unique_combinations)
	
def AppendDictionary(L, newDict, index):
	L[index].append(newDict)

def divisors(num):
	numSq = num ** 2
	
	return [d for d in range(1,numSq+1) if numSq%d == 0]

def sigma_2(num,divisors):
	numSq = num ** 2
	sig2 = sum(d**2 for d in divisors)
	return sig2

def create_list_of_lists(num_lists):
  """Creates a list of lists with a specified number of sublists.

  Args:
    num_lists: The desired number of sublists.

  Returns:
    A list of lists.
  """

  result = []
  for _ in range(num_lists):
    result.append([])
  return result

m2 = create_list_of_lists(10)
for i in range(1,30):
	if i % 50 == 0:
		print(i)
	d = divisors(i)
	#print(d)
	newDivisors = unique_combinations(d)[-1]
	product = 1
	for divItem in newDivisors:
		product *= divItem
	print(f'{i}:{product} ')
	s2 = sigma_2(i,d)
	s2m = s2 % 10
	AppendDictionary(m2,{i:s2},s2m)

# with open("sigma2.out","w") as f:
	# print(f'sigma[2,n] mod 10',file=f)
	# for i in range (0,10):
		# print(i,file=f)
		# for d in m2[i]:
			# print(d,file=f)


# print(sigma_2(11))
# print(sigma_2(121))
# print(sigma_2(122))
# print(sigma_2(29))
# print(sigma_2(4205))

# print(sigma_2(11))
# print(sigma_2(605))
