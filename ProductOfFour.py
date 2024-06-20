#
# The product of four integers in a consecutive aritmetic sequence added to the increment integer value
# raided to the fourth power is always a squared integer value.
#
# This program computes and reports these integer sequences up to a maximum user specified increment across
# a range of sequence value, also user specified.  See incrementMax and intMax below.
#
import sys
import collections
import time
import csv

#Prime lists
sys.path.append('.')
import _100KPrimes #100,000 prime numbers in an array named "primes"
# maxPrime: in the array of primes, this is the offset of the last
# prime to process.
maxPrime = 100000 #50000

splits = {}
splits[0] = time.time()

debug = False
lav = len(sys.argv)
if lav > 1:
	arg1 = sys.argv[1]
else:
	arg1 = "W"
if arg1.startswith("B"):
	bash = True
else:
	bash = False

# bash=False apps is on windows drive D as accessed from win10  =True/app is on windows drive F as accessed from bash on win10
# directory names must end with a directory specification separator (/ for linux, \ for ms Windows). Otherwise the final node will
# be treates as a file name prefix.
if bash:
	dirCSV = "/mnt/d/source/PythonApps/ProductOfFourSheet/Output/"
	dirTXT = "/mnt/d/source/PythonApps/ProductOfFourSheet/Output/"
else:
	winDrive = "D:"  # the windows drive for the output files
	dirCSV = winDrive + "\\source\\PythonApps\\ProductOfFourSheet\\Output2\\"
	dirTXT = winDrive + "\\source\\PythonApps\\ProductOfFourSheet\\Output2\\"

# for debugging, work with a smaller set of integers and increments
if debug:
	testNode="TEST_"
	intMax = 51
	incrementMax = 21
else:
	testNode = ""
	intMax = 5551 				# top of range, will actually iterate n - 1
	incrementMax = 1201

generateSheet = True					# True=generate spreadsheet data, False=no spreadsheet data
generateReport = True					# True=generate text report, False=no text report

if not generateSheet and not generateReport:
	print("Must run to generate either sheet or text report or both, but not neither.")
	exit()

# add the primes as keys to a dictionary "primeDict"
primesDict = {} # add the p

for w in _100KPrimes.primes:
	primesDict[w] = True

squaresDict = {}			# dictionary of lists of the generated squares and square roots. Key = square number
squaresList = {}			# list of generated squares and square roots
factorsDict = {}			# dictionary of lists of the prime factors of the square roots
factorsList = []			# list of the prime factors of the square roots



if generateReport:
	headerTXT = "{0:>8}{1:^30}num**0.5(factors)".format("i","num")
	headerLTXT = "-" * 72
					
for increment in range(1,incrementMax):
	inc4 = increment ** 4
	sqrtModList = []	# list of the first <increment> values of <increment> mod(square-root-of calculated integer)
	numModList = []		# list of the first <increment> values of <increment> mod(calculated integer)

	header0 = "increment == {0:d}".format(increment)
	if bash:
		header1 = "num == (i x (i+{0:d}) x (i+{1:d}) x (i+{2:d}) + {3:d})".format(increment,2*increment,3*increment,inc4) + " -or-  num == (i x {0:d} + (i + {0:d})²)²".format(increment)
	else:
		header1 = "num == (i x (i+{0:d}) x (i+{1:d}) x (i+{2:d}) + {3:d})".format(increment,2*increment,3*increment,inc4) + " -or-  num == (i x {0:d} + (i + {0:d})²)²".format(increment)

	if generateSheet:
		hdr1 = ["i","num","sq.Root"]
		hdr2 = "factor"			
		headerCSV = hdr1 + [hdr2]*13 + ["increment=="+"{0:d}".format(increment)]
		#open the report for output
		fCSV = open(dirCSV + 'Inc_'+testNode+str(increment)+'.csv', 'w',newline='')
		writer = csv.writer(fCSV)
		writer.writerow(headerCSV)
		#print(headerCSV + header0 + '\n' + header1,file=fCSV)
		
	if generateReport:
		primeRoots = 0
		maxRootFactor = 0
		maxNum = 0

		fTXT = open(dirTXT + 'Inc_'+testNode+str(increment)+'.txt', 'w') # for running on laptop machine

	#loop through the first "intMax" integers, calculating the product of four integers
	# in an arithmetic sequencce separated by the current increment
	#Note that analysis has shown that the square root of the product for the current index (== i) can
	#be calculated as the sum: i + (i+1)**2. This is probably faster than doing the product and then taking the square root.
	for i in range(1,intMax):
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
		# calculate the modulo values starting with increment = 2.
		if i <= increment and increment > 1:
			sqrtModList.append(sqrtNum % increment)
			numModList.append(num % increment)

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
				while j < maxPrime and breakJ == 0:
					p = _100KPrimes.primes[j]
					# There is no need to continue trying to find factors of the current
					# test number if we have not found one yet and the next prime > square
					# root of the test number or if the test number is in the table of 
					# primes.				
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
			csvRow = [i,num,sqrtNum]+factorsList
			writer.writerow(csvRow)
			#print(i,num,sqrtNum,*factorsList,sep=",",file=fCSV)

		if generateReport:
			factors = ""
			l = len(factorsList) - 1
			if l == 0:
				primeRoots += 1
			for idx,word in enumerate(factorsList):
				if idx < l:
					factors += str(int(word)) + " x "
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
		print("There are {0:d} prime square roots out of {1:d} calculations.".format(primeRoots,intMax - 1),file=fTXT)
		print("Maximum prime factor: {0:d} (at test for {1:d})".format(maxRootFactor,maxNum),file=fTXT)

		if increment % 2 == 1:
			moduloMidpoint = (increment -1) / 2
			incrementIsOdd = True
		else:
			moduloMidpoint = increment / 2
			incrementIsOdd = False

		moduloPrint = ""
		moduloPrintHeader = "Calculated number modulo " + str(increment) + " cycle: "
		moduloPrintHeaderLen = len(moduloPrintHeader)
		offset = 0
		rightAst = ""
		for m in numModList:
			offset += 1
			if offset == moduloMidpoint:
				if incrementIsOdd:
					strM = ('* ' + str(m)).rjust(11)
					rightAst = " *"
				else:
					strM = ("* " + str(m) + " *").rjust(11)
			else:
				strM = (str(m) + rightAst).rjust(11)
				rightAst = ""

			moduloPrint = moduloPrint + strM
			if len(moduloPrint) >= 110 and increment != 1:
				print(moduloPrintHeader + moduloPrint,file=fTXT)
				moduloPrintHeader = " " * moduloPrintHeaderLen
				moduloPrint = ""

		if moduloPrint != "" and increment != 1:
			print(moduloPrintHeader + moduloPrint,file=fTXT)

		offset = 0
		rightAst = ""
		moduloPrint = ""
		# pad print header to be as long as the prior header
		moduloPrintHeader = ("Square root modulo " + str(increment) + " cycle: ").ljust(moduloPrintHeaderLen)

		offset = 0
		rightAst = ""
		for m in sqrtModList:
			offset += 1
			if offset == moduloMidpoint:
				if incrementIsOdd:
					strM = ('* ' + str(m)).rjust(11)
					rightAst = " *"
				else:
					strM = ("* " + str(m) + " *").rjust(11)
			else:
				strM = (str(m) + rightAst).rjust(11)
				rightAst = ""

			moduloPrint = moduloPrint + strM
			if len(moduloPrint) >= 110 and increment != 1:
				print(moduloPrintHeader + moduloPrint,file=fTXT)
				moduloPrintHeader = " " * moduloPrintHeaderLen
				moduloPrint = ""

		if moduloPrint != "" and increment != 1:
			print(moduloPrintHeader + moduloPrint,file=fTXT)


	if generateSheet:
		fCSV.close()
	if generateReport:
		fTXT.close()
	ct = len(splits)
	splits[ct] = time.time()
	print("Processing complete for increment {inc:d}".format(inc=increment))
#end 'for increment in range(1,...'

#
# Each calculated square number was added as a key to a dictionary (squaresDict). That dictionary keeps track of all the
# four number arithmetic sequences and the difference between consecutive numbers in that sequence.
# So, for instance, the number 43681 (209 * 209) is generated by:
# 	13 * 14 * 15 * 16 + 1   (start = 13,diff = 1: 1**4)
# 	8 * 13 * 18 * 23 + 625  (start = 8, diff = 5: 5**4)
# 	5 * 13 * 21 * 29 + 4096 (start = 5, diff = 8: 8**4)
# 	1 * 14 * 27 * 40 + 28561 (start = 1, diff = 13: 13 ** 4)
# Thus the dictionary entry for 43681 is: 43681,209,13,1,8,5,5,8,1,13print("Processing analysis of calculated squares...")
osq = collections.OrderedDict(sorted(squaresDict.items()))
osqCt = 0
lMax = -1
with open("D:\\source\\pythonapps\\productoffoursheet\output2\\bigdictionary.txt","w") as bdo:
    for o in osq:
        l = len(osq[o])
        if l > 6:
            print(l,":",osq[o],file=bdo)
            osqCt += 1
            if l > lMax:
                lMax = l
    print("Max length of dictionary entries: {0:d}".format(lMax), file=bdo)        
if osqCt == 0:
    print("No data",file=bdo)
    
if generateSheet:		 
	header = ["Number","Root"]
	header_len = 2
	header2 = ["1st of four","Incr"]
	header2_len = 2 * (lMax - 2)
	header3 = ["factor"]
	fullHdr = header + header2 * (lMax - 2) + header3*13
	fileNo = 1
	count=0
	for k,v in osq.items():
		count += 1
		if count % 250000 == 1:
			if count != 1:
				fsqCSV.close()
			fsqCSV = open(dirCSV + "squares_"+testNode+str(fileNo)+".csv","w",newline='')
			writer = csv.writer(fsqCSV)
			writer.writerow(fullHdr)
			fileNo += 1
		
		factorsList = factorsDict[k]
		for i in range(header2_len - len(v) + 2):
			v.append("_")
			
		newlist = v + factorsList
		writer.writerow(newlist)
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
				factors += str(int(word)) + " x "
			else:
				factors += str(int(word))
		numSqrt = "{0:^30}".format("{0}({1})".format(num,sqrt))+"{0:^15}{1:^10}{2:^15}{3:^10}{4:^15}{5:^10}{6:^15}{7:^10}".format(i1Sum,inc1,i2,inc2,i3,inc3,i4,inc4)
		print("{0:s}{1:s}".format(numSqrt,factors),file=fsqTXT)
		lines += 1
ct = len(splits)
splits[ct] = time.time()

# for idx in range(0,ct+1):
# 	tm = splits[idx]
# 	if idx != 0:
# 		print("{interval:3d} {time:4.3f} Duration {duration:4.3f}".format(interval=idx,time=tm,duration=tm - baseTime))
# 	baseTime = tm
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
#
#(n^2 + 3*k*n + k^2)^2
#(n^2 + 3*k*n + k^2) * (n^2 + 3*k*n + k^2)
#n^4 + 3*k*n^3 + n^2*k^2 + 3*k*n^3 + 9*k^2*n^2 + 3*k^3*n + k^2+n^2 + 3*k^3*n + k^4
#n^4 + (3*k*n^3 + 3*k*n^3) + (n^2*k^2+9*k^2*n^2) + (3*k^3*n + 3*k^3*n) + k^4
#n^4 + 6*k*n^3 + 11*k^2*n^2 + 6*k^3*n + k^4
#