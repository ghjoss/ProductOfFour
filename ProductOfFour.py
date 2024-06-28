""" 
	The product of four integers in a consecutive aritmetic sequence (difference = "increment")
	added to the increment integer value raised to the fourth power is always a squared integer
	value. As an example:
	sequence 2 4 6 8  (increment = 2): 2 * 4 * 6 * 8 + 2^4 = 384 + 16 = 400

	This program computes and reports these integer sequences up to a maximum user specified increment.
	This is done across a range of sequence values, also user specified.

	See incrementMax and startOfSequenceMax below.

	See the on-line encyclopedia of integer sequences #A062938 (https://oeis.org/A062938)
	For increment=1: The square roots are the values in sequence #A028387. This sequence,
						generalized for all increments (not only inc=1), is used in the
						code below to evaluate the square roots without having to use the
						sqrt() function. 
	For increment=2: The square roots are the positive values in sequence #A028875
	For increment=3: The square roots are the positive values in sequence #A190576
	For increment=4: The square roots are the positive values in sequence #A134594
"""
import sys
import collections
import time
import csv

# set addThousandsSeparator to False to cause large numbers to be written without
# a thousands, millions, ... ',' separator.
ADD_THOUSANDS_SEPARATOR = True

# Function to format numbers with comma separators


def FormatWithCommas(num:int):
	return f'{num:,}' if ADD_THOUSANDS_SEPARATOR else str(num)


splits = {}
splits[0] = time.time()

# To run in a non-Windows environment, pass in a capital "B"
arg1 = sys.argv[1].lower() if len(sys.argv) > 1 else "W"
BASH = True if arg1.startswith("b") else False
# bash==False: The program is on windows a drive whose letter is defined in variable 'drive' as accessed from win10
# bash==True: program is running on Linux
#
# Whether running in Linux or Windows, directory names must end with a directory specification separator
# (/ for linux, \ for ms Windows). Otherwise the final node will be treated as a file name prefix.
# Note the defaults below assume either native windowns python app or a Windows SUbsystem for Linux (WSL)
# python app. Set your directories to match your own environment (native Linux or Mac).

DRIVE = "d"
if BASH:
	DIR_CSV = "/mnt/" + DRIVE + "/source/PythonApps/ProductOfFourSheet/Output/"
	DIR_TXT = "/mnt/d/source/PythonApps/ProductOfFourSheet/Output/"
else:
	# assumes Debian or ubuntu running in WSL (Windows Subystem for Linux)
	WIN_DRIVE = DRIVE + ":"  # the windows drive for the output files
	DIR_CSV = WIN_DRIVE + "\\source\\PythonApps\\ProductOfFourSheet\\Output\\"
	DIR_TXT = WIN_DRIVE + "\\source\\PythonApps\\ProductOfFourSheet\\Output\\"

# for debugging purposes, run with a smaller number of initial integers and
# a smaller number of sequence increments. Set debug=False to run with
# larger values
DEBUG = True
if DEBUG:
	TEST_NODE = "TEST_"			# when debugging, prepend 'TEST_' to the output file names
	START_OF_SEQUENCE_MAX = 200
	INCREMENT_MAX = 50
# startOfSequenceMax = 5551 and incrementMax = 1201 runs for about 10 minutes on a PC running
# Windows 10 on a Core i7 running at 2.4Ghz. Memory = 32GB.
else:
	TEST_NODE = ""
	START_OF_SEQUENCE_MAX = 5551 				# top of range, will actually iterate n - 1
	INCREMENT_MAX = 1201

GENERATE_SHEET = True			# True=generate spreadsheet data, False=no spreadsheet data
GENERATE_REPORT = True			# True=generate text report, False=no text report

if not GENERATE_SHEET and not GENERATE_REPORT:
	print("Must run to generate either sheet or text report or both, but not neither.")
	exit()

# Prime lists, _100KPrimes or _50KPrimes
sys.path.append('.')
import _100KPrimes				#100,000 prime numbers in a list named "primes"
# maxPrime: in the array of primes, this is the offset of the last
# prime to process.
MAX_PRIME = 100000 				#50000

# add the primes as keys to a dictionary "primeDict"
primesDict = {} # add the p

for w in _100KPrimes.primes:
	primesDict[w] = True

squaresDict = {}			# dictionary of lists of the generated squares and square roots. Key = square number
factorsList = []			# list of the prime factors of the square roots
factorsDict = {}			# dictionary of lists of the prime factors of the square roots

if GENERATE_REPORT:
	HEADER_TXT = "{0:>8}{1:^30}num**0.5(factors)".format("i","num")
	HEADER_LTXT = "-" * 72

# the difference between successive integers in the product of four integers is represented by the
# variable 'increment'. These increments will be iterated from 1 through incrementMax. The program will 
# calculate 'startOfSequenceMax' products for each difference.
for increment in range(1,INCREMENT_MAX):
	# to the product of four integers separated by 'increment' will be added increment to the 4th power
	# this will make the product + the 4th power of increment a perfect square integer.
	inc4 = increment ** 4
	sqrtModList = []	# list of the first <increment> values of <increment> mod(square-root-of calculated integer)
	numModList = []		# list of the first <increment> values of <increment> mod(calculated integer)

	# for this increment, determine and print the headers.
	HEADER_0 = "increment == {0:d}".format(increment)
	HEADER_1 = "num == (i x (i+{0:d}) x (i+{1:d}) x (i+{2:d}) + {3:d})".format(increment,2*increment,3*increment,inc4) + " -or-  num == (i x {0:d} + (i + {0:d})²)²".format(increment)

	# headers for .CSV file (spreadsheet)
	if GENERATE_SHEET:
		HDR_1 = ["i","num","sq.Root"]
		HDR_2 = "factor"
		HEADER_CSV = HDR_1 + [HDR_2]*13 + ["increment=="+"{0:d}".format(increment)]
		# open the report for output
		fCSV = open(DIR_CSV + TEST_NODE+'Inc_'+str(increment)+'.csv', 'w',newline='')
		writer = csv.writer(fCSV)
		writer.writerow(HEADER_CSV)

	if GENERATE_REPORT:
		primeRoots = 0
		maxRootFactor = 0
		maxNum = 0

		fTXT = open(DIR_TXT + TEST_NODE+'Inc_'+str(increment)+'.txt', 'w') # for running on laptop machine

	# loop through the first "startOfSequenceMax" integers, calculating the product of four integers that are
	# in an arithmetic sequencce separated by the current increment
	# Note that analysis has shown that the square root of the product for the current index (== i) can
	# be calculated as the sum: (i + (i+increment)**2). This is probably faster than doing the product and then taking the square root.
	for startInteger in range(1,START_OF_SEQUENCE_MAX):
		factorsList = []
		# the text file output header is printed every 45 lines.
		if GENERATE_REPORT:
			if startInteger % 45 == 1:
					if startInteger > 1:
						print("",file=fTXT)
					print(HEADER_LTXT,file=fTXT)
					print(HEADER_0,file=fTXT)
					print(HEADER_1,file=fTXT)
					print(HEADER_TXT,file=fTXT)
					print(HEADER_LTXT,file=fTXT)

		# squareNum = i * (i + increment) * (i + 2*increment) * (i + 3*increment) + increment**4
		# factorizationTestNum = sqrtNum = num ** 0.5
		# alternative, equivalent values
		i1Sum = startInteger + increment
		factorizationTestNum = sqrtNum = startInteger*increment + i1Sum * i1Sum  #factorizationTestNum = sqrtNum = i*increment + (i+increment)²
		# squareNum = (iProd + i1Sum**2)**2
		squareNum = sqrtNum * sqrtNum

		# calculate the modulo values starting with increment = 2.
		if startInteger <= increment and increment > 1:
			sqrtModList.append(sqrtNum % increment)
			numModList.append(squareNum % increment)

		if squareNum in squaresDict:      # have we already seen this number when processing a previous arithmetic sequence?
			# yes, append the current value of i and the increment to the list entry for this number
			sqList = squaresDict[squareNum]	 # get the list
			sqList.append(startInteger)		 # add current '1st of the four arithmetic sequence' value (i)
			sqList.append(increment)		 # add the current increment value
		else:
			# no, add a new dictionary entry with key = 'num' (a list)
			squaresDict[squareNum] = [squareNum, sqrtNum, startInteger, increment]

		# get prime factors of the square root of the calculated number
		if squareNum in factorsDict:		#have we already found the factors of this number?
			# yes, just retrieve the previously determined factors
			factorsList = factorsDict[squareNum]
		else:
			# no, this is a number we have not yet factored
			if sqrtNum in primesDict:	# is the current square root one of the first 50K primes in the primes list
				# yes, no need to factor further
				factorsList.append(sqrtNum)
				if GENERATE_REPORT and sqrtNum > maxRootFactor:
					maxNum = squareNum
					maxRootFactor = sqrtNum
			else:
				# no, this is the first time factoring the sqrtNum
				breakJ = 0	# controls whether to leave the "while j <...." loop below
				j = 0		# loop index for the list[] of the first 50000 primes
				sqrtFactorizationTestNum = sqrtNum ** 0.5  # max value to test
				while j < MAX_PRIME and breakJ == 0:
					p = _100KPrimes.primes[j]
					# There is no need to continue trying to find factors of the current
					# test number if we have not found one yet and the next prime > square
					# root of the test number or if the test number is in the table of
					# primes.
					if p > sqrtFactorizationTestNum or factorizationTestNum in primesDict:
						factorsList.append(factorizationTestNum)
						if GENERATE_REPORT and factorizationTestNum >= maxRootFactor:
							maxNum = squareNum
							maxRootFactor = factorizationTestNum
						break  # while j < len(primes) and breakJ == 0
					else:
						while factorizationTestNum % p == 0:
							if p > maxRootFactor:
								maxNum = squareNum
								maxRootFactor = p
							factorizationTestNum /= p
							factorizatoinTestNum = int(factorizationTestNum)
							if factorizationTestNum == 1:
								factorsList.append(p)
								breakJ = 1
								break  # while factorizationTestNum %p == 0
							else:
								factorsList.append(p)
						sqrtFactorizationTestNum = factorizationTestNum ** 0.5
						j = j + 1
				#end 'while j < len(primes) and breakJ == 0

		if GENERATE_SHEET:
			csvRow = [startInteger, squareNum, sqrtNum] +  factorsList
			writer.writerow([FormatWithCommas(number) for number in csvRow])

		if GENERATE_REPORT:
			factors = ""
			lFactors = len(factorsList) - 1
			if lFactors == 0:
				primeRoots += 1
			for idx, word in enumerate(factorsList):
				wordC = FormatWithCommas(int(word))
				if idx < lFactors:
					factors += wordC+ " x "
				else:
					factors += wordC

			startIntegerT = FormatWithCommas(startInteger)
			squareNumT = FormatWithCommas(squareNum)
			sqrtNumT = FormatWithCommas(sqrtNum)
			print("{0:8}{1:^30}".format(startIntegerT, squareNumT)+"{0:^}({1})".format(sqrtNumT, factors), file=fTXT)

		if squareNum not in factorsDict:
			factorsDict[squareNum] = factorsList

		# every so often: show that we're still alive
		if startInteger > 1 and startInteger % 250 == 1:
			sys.stdout.write(".")
			sys.stdout.flush()
			if startInteger % 2500 == 1:
				print("{0:d} products analyzed".format(startInteger))

	if GENERATE_REPORT:
		print("There are {0:d} prime square roots out of {1:d} calculations.".format(primeRoots, START_OF_SEQUENCE_MAX - 1), file=fTXT)
		print("Maximum prime factor: {0:d} (at test for {1:d})".format(maxRootFactor, maxNum),file=fTXT)

		if increment % 2 == 1:
			moduloMidpoint = (increment -1) / 2
			incrementIsOdd = True
		else:
			moduloMidpoint = increment / 2
			incrementIsOdd = False

		moduloPrint = ""
		moduloPrintHeader = "Calculated number modulo " + str(increment) + " cycle: "
		moduloPrintHeaderLen = len(moduloPrintHeader)
		rightAst = ""
		for offset, m in enumerate(numModList, start=1):
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
				print(moduloPrintHeader + moduloPrint, file=fTXT)
				moduloPrintHeader = " " * moduloPrintHeaderLen
				moduloPrint = ""

		if moduloPrint != "" and increment != 1:
			print(moduloPrintHeader + moduloPrint, file=fTXT)

		rightAst = ""
		moduloPrint = ""
		# pad print header to be as long as the prior header
		moduloPrintHeader = ("Square root modulo " + str(increment) + " cycle: ").ljust(moduloPrintHeaderLen)

		rightAst = ""
		for offset, m in enumerate(sqrtModList, start=1):
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
				print(moduloPrintHeader + moduloPrint, file=fTXT)
				moduloPrintHeader = " " * moduloPrintHeaderLen
				moduloPrint = ""

		if moduloPrint != "" and increment != 1:
			print(moduloPrintHeader + moduloPrint, file=fTXT)


	if GENERATE_SHEET:
		fCSV.close()
	if GENERATE_REPORT:
		fTXT.close()

	splits[len(splits)] = time.time()
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
# Thus the dictionary entry for 43681 is: 43681,209,13,1,8,5,5,8,1,13
#
print("Multiple starting integer/increment pairs generate the same square number. Iterate over the")
print("squaresDict collection to find these sequences/increment pairs.")
print("e.g.: 43861 == 209*209 == 13*14*15*16+1 == 8*13*18*23+625 (5^4) == 5*13*21*29+512 (8^4) == 1 * 14 * 27 * 40 + 28561 (13^4)")
osq = collections.OrderedDict(sorted(squaresDict.items())) #osq: o_rdered sq_uares dictionary
osqCt = 0
lMax = -1
with open(DIR_TXT+TEST_NODE+"bigdictionary.txt","w") as bdo:
    for o in osq:
        listLen = len(osq[o])
        if listLen > 6:
            print(listLen, ":", osq[o], file=bdo)
            osqCt += 1
            if listLen > lMax:
                lMax = listLen
    print("Max length of dictionary entries: {0:d}".format(lMax), file=bdo)

if osqCt == 0:
    print("No data",file=bdo)

if GENERATE_SHEET:
	print("Squares analysis .csv sheets")		 
	header = ["Number","Root"]
	header2 = ["1st of four","Incr"]
	header2_len = 2 * (lMax - len(header))
	header3 = ["factor"]
	fullHdr = header + header2 * (lMax - 2) + header3*13
	fileNo = 1
	outputLineCount = 0

	for key, val in osq.items():
		vCSV = [FormatWithCommas(number) for number in val.copy()]

		outputLineCount += 1
		if outputLineCount % 250000 == 1:
			if outputLineCount != 1:
				fsqCSV.close()
			fsqCSV = open(DIR_CSV + TEST_NODE+"squares_"+str(fileNo)+".csv","w",newline='')
			writer = csv.writer(fsqCSV)
			writer.writerow(fullHdr)
			fileNo += 1

		factorsList = factorsDict[key]
		# csv() does not like empty values
		for startInteger in range(header2_len - len(val) + 2):
			vCSV.append("_")

		newlist = vCSV + factorsList
		writer.writerow(newlist)
	splits[len(splits)] = time.time()
	fsqCSV.close()

if GENERATE_REPORT:
	print("Squares analysis .txt reports ")
	fsqTXT = open(DIR_TXT + TEST_NODE+"squares.txt","w")
	lines = 0
	header = "{0:^30}".format("Number(Root)")
	header2 = "{0:^15}{1:^10}".format("1st of four","incr")
	header = header + header2 * 4 + "Prime Factors"
	headerL = "-" * len(header)

	for key, val in osq.items():
		vTXT = [FormatWithCommas(number) for number in val.copy()]
		if lines % 45 == 0:
			if lines != 0:
				print("", file=fsqTXT)
			print(headerL, file=fsqTXT)
			print(header, file=fsqTXT)
			print(headerL, file=fsqTXT)
		factorsList = factorsDict[key]
		factors = ""
		lFactors = len(factorsList) - 1
		for idx, word in enumerate(factorsList):
			wordC = FormatWithCommas(int(word))
			if idx < lFactors:
				factors += wordC + " x "
			else:
				factors += wordC

		squareNum = vTXT[0]
		sqrt = vTXT[1]
		vTXT2 = vTXT[2:] # slice off number and sqare root
		appendLen = lMax + 4 - len(vTXT2)
		vTXT2 = vTXT2 + ["-"] * appendLen

		# print(vTXT[2:])
		# print("{0:^2}: {1}".format(len(v2),v2))
		# print("")

		try:
			for idx, val in enumerate(vTXT2):
				if not idx % 8 == 0:
					continue
				if vTXT2[idx] == "-":
					break
				i1Sum = vTXT2[idx]
				inc1 = vTXT2[idx+1]
				i2 = vTXT2[idx+2]
				inc2 = vTXT2[idx+3]
				i3 = vTXT2[idx+4]
				inc3 = vTXT2[idx+5]
				i4 = vTXT2[idx+6]
				inc4 = vTXT2[idx+7]

				if idx == 0:
					numSqrt = "{0:^30}".format("{0}({1})".format(squareNum, sqrt))+"{0:^15}{1:^10}{2:^15}{3:^10}{4:^15}{5:^10}{6:^15}{7:^10}".format(i1Sum, inc1, i2,inc2, i3, inc3, i4, inc4)
					print("{0:s}{1:s}".format(numSqrt,factors),file=fsqTXT)
				else:
					numSqrt = "{: <30}".format(" ")+"{0:^15}{1:^10}{2:^15}{3:^10}{4:^15}{5:^10}{6:^15}{7:^10}".format(i1Sum, inc1, i2, inc2, i3, inc3, i4,inc4)
					print("{0:s}".format(numSqrt),file=fsqTXT)
		except IndexError:
			print("Index out of range")
			print(idx, vTXT2)
			sys.exit()

		lines += 1
	splits[len(splits)] = time.time()

ct = len(splits)
splits[ct] = time.time()

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
