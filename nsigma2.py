import itertools
import math
""" 
def unique_combinations(items):
	unique_combinations = []
	for r in range(1, len(items) + 1):
		combinations = itertools.combinations(items, r)
		unique_combinations.extend(combinations)
	# print(f'uc2{combinations})')
	return list(unique_combinations)
 """	
def AppendDictionary(L, newDict, index):
	L[index].append(newDict)

# σ₂(n²)
def sigma_2(num):
	num_2 = num * num
	sum = 0
	for d in range(1,num+1):
		if num_2%d == 0:
			sum += d*d
			d = int(num_2/d)
			if d != num:
				sum += d * d
	return sum

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

import _100KPrimes
# add the primes as keys to a dictionary "primeDict"
primesDict = {} # add the p

for w in _100KPrimes.primes:
	primesDict[w] = True

maxSigma: int  = 25000
maxModsInLine: int = 30
heartBeat: int = 0
m2 = create_list_of_lists(10)

with open("_sigma2Mod10.py","w") as f:
	print("sigma2Mod10=[0,",file=f)
	numsInLine: int = 0
	line: str = ""
	for i in range(1,maxSigma+1):
	#	print(i)
	#	i2 = i*i
	#	i4 = i2*i2
		s2 = sigma_2(i)
		s2m = s2 % 10
		line += f'{s2m}, '
		numsInLine += 1
		heartBeat += 1
		if heartBeat == 200:
			print(i)
			heartBeat = 0
		if numsInLine == maxModsInLine:
			print(line,file=f)
			line = ""
			numsInLine = 0
		ast = "*" if i in primesDict else " "
		AppendDictionary(m2,{i:f'{s2}  {ast}'},s2m)

	s2m = sigma_2(maxSigma+1) % 10
	print(f'{s2m}]',file=f)	
#	AppendDictionary(m2,{i:f'{s2}({s})  {ast}'},s2m)
	

with open("nsigma2.out","w") as f:
	cbs = r'{'
	cbe = r'}'
#	hdr = f"{cbs}n: 'sigma[2,n²](sigma[2,n])'{cbe} mod 10"
	hdr = f"{cbs}n: 'sigma[2,n²]' {cbe} mod 10"
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
