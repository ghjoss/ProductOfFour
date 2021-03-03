#
# The product of four consecutive numbers + 1 is always an integer squared.
# Calculate the first n products +1, their square roots and the factors of those
# square roots. Print out the results.
#
import sys
import collections
import time

sys.path.append('.')
import _50KPrimes

splits = {}
splits[0] = time.time()

debug = False
bash = True		# =False/apps is on windows drive F as accessed from win10  =True/app is on windows drive F as accessed from bash on win10
# directory names must end with a directory specification separator (/ for linux, \ for ms Windows). Otherwise the final node will
# be treates as a file name prefix.
if bash:
	dirCSV = "/mnt/f/source/PythonApps/ProductOfFourSheet/Output/"
	dirTXT = "/mnt/f/source/PythonApps/ProductOfFourSheet/Output/"
else:
	dirCSV = "f:\\source\\PythonApps\\ProductOfFourSheet\\Output\\"
	dirTXT = "f:\\source\\PythonApps\\ProductOfFourSheet\\Output\\"

# for debugging, work with a smaller set of numbers and increments
if debug:
	testNode="TEST_"
	n = 500
	incMax = 2
else:
	testNode = ""
	n = 5551 				# top of range, will actually iterate n - 1
	incMax = 1201

generateSheet = True					# True=generate spreadsheet data, False=no spreadsheet data
generateReport = True					# True=generate text report, False=no text report

if not generateSheet and not generateReport:
	print("Must run to generate either sheet or text report or both, but not neither.")
	exit()

# add the primes as keys to a dictionary "primeDict"
primesDict = {} # add the p
for w in _50KPrimes.primes:
	primesDict[w] = True

squaresDict = {}			# dictionary of lists of the generated squares and square roots. Key = square number
squaresList = {}			# list of generated squares and square roots
factorsDict = {}			# dictionary of lists of the prime factors of the square roots
factorsList = []			# list of the prime factors of the square roots


if generateSheet:				
	headerCSV = "i,num,sq.Root"+",factor"*13

if generateReport:
	headerTXT = "{0:>8}{1:^30}num**0.5(factors)".format("i","num")
	headerLTXT = "-" * 72
					
for increment in range(1,incMax):
	inc4 = increment ** 4

	header0 = "increment == {0:d}".format(increment)
	if bash:
		header1 = "num == (i x (i+{0:d}) x (i+{1:d}) x (i+{2:d}) + {3:d})".format(increment,2*increment,3*increment,inc4) + " -or-  num == (i x {0:d} + (i + {0:d})²)²".format(increment)
	else:
		header1 = "num == (i × (i+{0:d}) × (i+{1:d}) × (i+{2:d}) + {3:d})".format(increment,2*increment,3*increment,inc4) + " -or-  num == (i × {0:d} + (i + {0:d})²)²".format(increment)

	if generateSheet:
		#open the report for output
		fCSV = open(dirCSV + 'ProductOfFour_Increment_'+testNode+str(increment)+'.csv', 'w')
		print(headerCSV + header0 + '\n' + header1,file=fCSV)
		
	if generateReport:
		primeRoots = 0
		maxRootFactor = 0
		maxNum = 0

		fTXT = open(dirTXT + 'ProductOfFour_Increment_'+testNode+str(increment)+'.txt', 'w') # for running on laptop machine

	#loop through the first "n" integers, calculating the product of four consecutive
	#numbers, starting at the current index. Note that observation and analysis has
	#shown that the square root of the product for the current index (== i) can
	#be calculated as the sum: i + (i+1)**2. This is probably faster than doing the 
	#product and then taking the square root.
	for i in range(1,n):
		factorsList = []

		if generateReport:	
			if i % 45 == 1:
					if i > 1:
						print("",file=fTXT)
					print(headerLTXT,file=fTXT)
					print(header0,file=fTXT)
					print(header1,file=fTXT)
					print(headerTXT,file=fTXT)
					print(headerLTXT,file=fTXT)
							
		#num = i * (i + increment) * (i + 2*increment) * (i + 3*increment) + inc4
		#factorizationTestNum = sqrtNum = num ** 0.5
		# alternative, equivalent values
		i1Sum = i + increment
		factorizationTestNum = sqrtNum = i*increment + i1Sum * i1Sum  #factorizationTestNum = sqrtNum = i*increment + (i+increment)²
		#num = (iProd + i1Sum**2)**2
		num = sqrtNum * sqrtNum
		if num in squaresDict: # have we already seen this number when processing a previous arithmetic sequence?
			#yes, append the current value of i and the increment to the list entry for this number
			l = squaresDict[num]	#get the list
			l.append(i)				#add current '1st of the four arithmetic sequence' value (i)
			l.append(increment)		#add the current increment value
			squaresDict[num] = l	#replace the dictionary entry for this list (key='num')
		else:
			#no, add a new dictionary entry with key = 'num' (a list)
			squaresDict[num] = [num,sqrtNum,i,increment]

		
		# get prime factors of the square root of the calculated number
		if num in factorsDict:		#have we already found the factors of this number?
			#yes, just retrieve the previously determined factors
			factorsList=factorsDict[num]
		else:
			#no, this is a number we have not yet factored
			if sqrtNum in primesDict:	# is the current square root one of the first 50K primes in the primes list
				#yes, no need to factor further
				factorsList.append(sqrtNum)
				if generateReport and sqrtNum > maxRootFactor:
					maxNum = num
					maxRootFactor = sqrtNum
			else:
				#no, this is the first time factoring the sqrtNum
				breakJ = 0	# controls whether to leave the "while j <...." loop below
				j = 0		# loop index for the list[] of the first 50000 primes
				sqrtFactorizationTestNum = sqrtNum ** 0.5	#max value to test
				while j < len(_50KPrimes.primes) and breakJ == 0:
					p = _50KPrimes.primes[j]
					# There is no need to continue trying to find factors of the current
					# test number if we have not found one yet and the next prime > square
					# root of the test number or if the test number is in the table of 
					# 50,000 primes.				
					if p > sqrtFactorizationTestNum or factorizationTestNum in primesDict:
						factorsList.append(factorizationTestNum)
						if generateReport and factorizationTestNum >= maxRootFactor:
							maxNum = num
							maxRootFactor = factorizationTestNum
						break # while j < len(primes) and breakJ == 0
					else:	
						while factorizationTestNum % p == 0:
							if p > maxRootFactor:
								maxNum = num
								maxRootFactor = p
							factorizationTestNum /= p
							factorizatoinTestNum = int(factorizationTestNum)
							if factorizationTestNum == 1:
#								factors = factors + "," + str(p)
								factorsList.append(p)
								breakJ = 1
								break # while factorizationTestNum %p == 0
							else: 
								factorsList.append(p)
						sqrtFactorizationTestNum = factorizationTestNum ** 0.5
						j = j + 1
				#end 'while j < len(primes) and breakJ == 0
		if generateSheet:
			print(i,num,sqrtNum,*factorsList,sep=",",file=fCSV)
		if generateReport:
			factors = ""
			l = len(factorsList) - 1
			if l == 0:
				primeRoots += 1
			for idx,word in enumerate(factorsList):
				if idx < l:
					factors += str(int(word)) + " x " if bash else " × "
				else:
					factors += str(int(word))
			print("{0:8d}{1:^30d}".format(i,num)+"{0:^d}({1})".format(sqrtNum,factors),file=fTXT)

		if not (num in factorsDict):
			factorsDict[num] = factorsList

		# every so often: show that we're still alive
		if i > 1 and i % 250 == 1:
			sys.stdout.write(".")
			sys.stdout.flush()
			if i%2500 == 1:
				print("{0:d} products analyzed".format(i))
	if generateReport:
		print("There are {0:d} prime square roots out of {1:d} calculations.".format(primeRoots,n - 1),file=fTXT)
		print("Maximum prime factor: {0:d} (at test for {1:d})".format(maxRootFactor,maxNum),file=fTXT)

	# end "for in in range(1,n)
	if generateSheet:
		fCSV.close()
	if generateReport:
		fTXT.close()
	ct = len(splits)
	splits[ct] = time.time()
	print("Processing complete for increment {inc:d}".format(inc=increment))
#end 'for increment in range(1,...'

print("Processing analysis of calculated squares...")
osq = collections.OrderedDict(sorted(squaresDict.items()))

if generateSheet:		 
	header = "Number,Root"
	header2 = ",1st of four,Incr"*4
	header = header + header2 + ",factor"*13
	fileNo = 1
	count=0
	for k,v in osq.items():
		count += 1
		if count % 250000 == 1:
			if count != 1:
				fsqCSV.close()
			fsqCSV = open(dirCSV + "squares_"+testNode+str(fileNo)+".csv","w")
			print(header,file=fsqCSV)
			fileNo += 1
		factorsList = factorsDict[k]
		for i in range(1,10-len(v)+1):
			v.append("")
		newlist = v + factorsList
		print(*newlist,sep=",",file=fsqCSV)
	fsqCSV.close()
if generateReport:
	fsqTXT = open(dirTXT + "squares.txt","w")
	lines = 0
	header = "{0:^30}".format("Number(Root)")
	header2 = "{0:^15}{1:^10}".format("1st of four","incr")
	header = header + header2 * 4 + "Prime Factors"
	headerL = "-" * len(header)
			  
	for k,v in osq.items():
			   
		if lines % 45 == 0:
			if lines != 0:
				print("",file=fsqTXT)
			print(headerL,file=fsqTXT)
			print(header,file=fsqTXT)
			print(headerL,file=fsqTXT)
		for i in range(1,10-len(v)+1):
			v.append("")
		for idx,word in enumerate(v):
			if idx == 0:
				offset = lines + 1
				num = word
			elif idx == 1:
				sqrt = word
			elif idx == 2:
				i1Sum = word
			elif idx == 3:
				inc1 = word
			elif idx == 4:
				i2 = word
			elif idx == 5:
				inc2 = word
			elif idx == 6:
				i3 = word
			elif idx == 7:
				inc3 = word
			elif idx == 8:
				i4 = word
			elif idx == 9:
				inc4 = word
		factorsList = factorsDict[k]
		factors = ""
		l = len(factorsList) - 1
		for idx,word in enumerate(factorsList):
			if idx < l:
				factors += str(int(word)) + " x " if bash else " × "
			else:
				factors += str(int(word))
		numSqrt = "{0:^30}".format("{0}({1})".format(num,sqrt))+"{0:^15}{1:^10}{2:^15}{3:^10}{4:^15}{5:^10}{6:^15}{7:^10}".format(i1Sum,inc1,i2,inc2,i3,inc3,i4,inc4)
		print("{0:s}{1:s}".format(numSqrt,factors),file=fsqTXT)
		lines += 1
ct = len(splits)
splits[ct] = time.time()

for idx in range(0,ct+1):
	tm = splits[idx]
	if idx != 0:
		print("{interval:3d} {time:4.3f} Duration {duration:4.3f}".format(interval=idx,time=tm,duration=tm - baseTime))
	baseTime = tm
print("Total Duration {duration:4.3f}".format(duration=splits[ct] - splits[0]))
print("Processing complete.")


#n * (n+k) * (n + 2*k) * (n+3*k) + k^4 
#= n* (n+2*k) * (n+k)*(n+3*k) + k^4
#= (n^2+2*k*n) * (n^2 + 4*k*n + 3*k^2) + k^4
#= (n^2*n^2 + 2*k*n*n^2) + (4*k*n*n^2 + 4*k*n*2*k*n) + (3*k^2 * n^2 + 3*k^2 * 2*k*n) +k^4
#= n^4      + 2*k*n^3    + 4*k*n^3    + 8*k^2*n^2    +  3*k^2*n^2   + 6*k^3*n        + k^4
#= n^4      + 6*k*n^3                 + 11*k^2n^2                   + 6*k^3*n        + k^4
#
#(n*k + (n+k)^2)^2
#=(n*k + n^2 + 2*k*n + k^2)^2
#=(n*k + n^2 + 2*k*n + k^2) * (n*k + n^2 + 2*k*n + k^2)
#= (n*k*n*k + n^2*n*k + 2*k*n*n*k + k^2*n*k) + (n*k*n^2 + n^2*n^2 + 2*k*n*n^2 + k^2*n^2) + (n*k*2*k*n + n^2*2*k*n + 2*k*n*2*k*n + k^2*2*k*n) + (n*k*k^2 + n^2*k^2 + 2*k*n*k^2) + (k^2*k^2)
#= (k^2*n^2 + k*n^3 + 2*k^2*n^2 + k^3*n) + (k*n^3 + n^4 + 2*k*n^3 + k^2*n^2) + (2*k^2*n^2 + 2*k*n^3 + 4*k^2*n^2 + 2*k^3*n) + (k^3*n + k^2*n^2 + 2*k^3*n + k^4)
#= n^4 + (k*n^3 + k*n^3 + 2*k*n^3 + 2*k*n^3) + (k^2n^2 + 2*k^2*n^2 + k^2*n^2 + 2*k^2*n^2 + 4*k^2*n^2 + k^2*n^2) + (k^3*n + 2*k^3*n + k^*n + 2*k^3*n) + k^4
#= n^4 + 6*k*n^3 + 11*k^2n^2 + 6*k^3*n + k^4
