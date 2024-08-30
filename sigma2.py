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

def sigma_2(num): 
	divisors = [d for d in range(1,num+1) if num%d == 0]
	return sum(d*d for d in divisors)

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
for i in range(1,2001):
	print(i)
	s2 = sigma_2(i*i)
	s = sigma_2(i)
	s2m = s2 % 10
	sm = s % 10
	AppendDictionary(m2,{i:f'{s2}({s})'},s2m)

with open("sigma2.out","w") as f:
	cbs = r'{'
	cbe = r'}'
	hdr = f"{cbs}n: 'sigma[2,n²](sigma[2,n])'{cbe} mod 10"
	print(hdr,file=f)
	lines = 1
	for i in range (0,10):
		print(f'{i}: count={len(m2[i])}',file=f)
		lines += 1
		for d in m2[i]:
			print(d,file=f)
			lines += 1
			if lines % 50 == 0:
				print(hdr,file=f)
