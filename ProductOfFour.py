""" 
	The product of four integers in a consecutive aritmetic sequence (difference = "increment")
	added to the increment integer value raised to the fourth power is always a squared integer
	value. As an example:
	sequence 2 4 6 8  (increment = 2): 2 * 4 * 6 * 8 + 2^4 = 384 + 16 = 400

	This program computes and reports these integer sequences up to a maximum user specified increment.
	This is done across a range of sequence values, also user specified.

	See incrementMax and startOfSequenceMax below.

	See the on-line encyclopedia of integer sequences #A062938 (https://oeis.org/A062938)
	This sequence, generalized for all increments (not only inc=1), is used in the
	code below to evaluate the square roots without having to use the
	sqrt() function. 

	For increment=1: The square roots are the values in sequence #A028387. 
	For increment=2: The square roots are the positive values in sequence #A028875
	For increment=3: The square roots are the positive values in sequence #A190576
	For increment=4: The square roots are the positive values in sequence #A134594
	For increment=5 through increment=25, no sequences were found referencing the
	square roots.
"""
import os
import errno
import sys
import collections
import time
import csv
import json

splits = {}
splits[0] = time.time()
# for debugging purposes, run with a smaller number of initial integers and
# a smaller number of sequence increments. Set debug=False to run with
# larger values
arg1 = "t"
DEBUG = True
if len(sys.argv) > 1:
	arg1 = sys.argv[1].lower()
	if arg1.startswith("f") or arg1 == "0":
		DEBUG = False

PATH = os.path.dirname(__file__) + "/"
with open(PATH + "ProductOfFour.json","r") as jsonFile:
	jsonData = jsonFile.read()
	settings = json.loads(jsonData)
	if DEBUG:
		TEST_NODE = settings["debug"]["test_node"]
		START_OF_SEQUENCE_MAX = settings["debug"]["start_of_sequence_max"]
		INCREMENT_MAX = settings["debug"]["increment_max"]
	else:
		TEST_NODE = settings["max"]["test_node"]
		START_OF_SEQUENCE_MAX = settings["max"]["start_of_sequence_max"]
		INCREMENT_MAX = settings["max"]["increment_max"]

	OUTPUT_FOLDER = settings["output_folder"]
	# True=generate spreadsheet data, False=no spreadsheet data
	GENERATE_SHEET = settings["generate_sheet"]
	# True=generate ...txt files, false no files
	GENERATE_REPORT = settings["generate_report"]
	# True=generate ...INCn_.csv and ...INCn.txt files, false, no increment output
	GENERATE_INCREMENT_OUTPUT = settings["generate_increment_output"]
	# True=generate ...squares.csv & txt, false no squares output
	GENERATE_SQUARES_OUTPUT = settings["generate_squares_output"]

	# number of INC_... files to write (one each of .csv and .txt)
	MAX_INCREMENT_FILES = settings["max_increment_files"]

	SQUARES_PAGES_PER_FILE = settings["squares_pages_per_file"]
	SQUARES_LINES_PER_PAGE = settings["squares_lines_per_page"]
	INCREMENTS_LINES_PER_PAGE = settings["increments_lines_per_page"]
	ODDSEQUENCES_SINGLET = settings["Odd_Sequences_Include_Singlets"]

	# set addThousandsSeparator to False to cause large numbers to be written without
	# a thousands, millions, ... ',' separator.
	ADD_THOUSANDS_SEPARATOR = settings["add_thousands_separator"]

# Function to format numbers with comma separators
def FormatWithCommas(num:int):
	return f'{num:,}' if ADD_THOUSANDS_SEPARATOR and isinstance(num,(int,float)) else str(num)

if not isinstance(MAX_INCREMENT_FILES,(int,float)):
	MAX_INCREMENT_FILES = INCREMENT_MAX # write all of them

# get working directory of this python program, add
# an Output subdirectory (if necessary).
OUTPUT_DIR = PATH + OUTPUT_FOLDER
try:
	os.mkdir(OUTPUT_DIR)
except OSError as error:
	if not error.errno == errno.EEXIST:
		print(f"Failed to create: {OUTPUT_DIR}")
		exit()

DIR_CSV = OUTPUT_DIR + "/"
DIR_TXT = OUTPUT_DIR + "/"

if not GENERATE_SHEET and not GENERATE_REPORT:
	print("Check the file ProductOf_Four.json:\n" \
	   "Either of the values generate_sheet and generate_report \n (or both) must be true. Both were 'false'.")
	exit()
if not GENERATE_INCREMENT_OUTPUT and not GENERATE_SQUARES_OUTPUT:
	print("Check the file ProductOfFour.json:\n"
	   "Either of the values generate_increment_output and generate_squares_output \n (or both) must be true. Both were 'false'.")
	exit()
# Prime lists, _100KPrimes or _50KPrimes
sys.path.append('.')
import _100KPrimes				#100,000 prime numbers in a list named "primes"
# maxPrime: in the array of primes, this is the offset of the last
# prime to process.
MAX_PRIME = 100000				#50000

# add the primes as keys to a dictionary "primeDict"
primesDict = {} # add the p

for w in _100KPrimes.primes:
	primesDict[w] = True

squaresDict = {}			# dictionary of lists of the generated squares and square roots. Key = square number
factorsList = []			# list of the prime factors of the square roots
factorsDict = {}			# dictionary of lists of the prime factors of the square roots

if GENERATE_REPORT:
	HEADER_TXT = "{0:<8}{1:^30}R[n]^0.5(factors)".format("n","R[n]")
	HEADER_LTXT = "-" * 72

# the difference between successive integers in the product of four integers is represented by the
# variable 'increment'. These increments will be iterated from 1 through INCREMENT_MAX. The program will 
# calculate START_OF_SEQUENCE_MAX products for each difference.
for increment in range(1,INCREMENT_MAX):
	# to the product of four integers separated by 'increment' will be added increment to the 4th power
	# this will make the product + the 4th power of increment a perfect square integer.
	inc4 = increment ** 4
	sqrtModList = []	# list of the first <increment> values of <increment> mod(square-root-of calculated integer)
	numModList = []		# list of the first <increment> values of <increment> mod(calculated integer)

	# for this increment, determine and print the headers.
	HEADER_0 = "increment == {0:d}".format(increment)
	HEADER_1 = "R[n] == (n x (n+{0:d}) x (n+{1:d}) x (n+{2:d}) + {3:d})".format(increment,2*increment,3*increment,inc4) + " -or-	 R[n] == (n x {0:d} + (n + {0:d})²)²".format(increment)

	# headers for .CSV file (spreadsheet)
	if GENERATE_SHEET and GENERATE_INCREMENT_OUTPUT and increment <= MAX_INCREMENT_FILES:
		HDR_1 = ["n","R[n]","(R[n])^.5","S[n]^2","S[n]","(S[n]+(R[n])^.5)/2","(S[n]+(R[n])^.5)/2)^.5"]
		HDR_2 = "factor"
		HEADER_CSV = HDR_1 + [HDR_2]*13 + [f"  increment=={increment:.0f}  S[n]=(R[n]+R[n-{increment:.0f}]+R[n-{2*increment:.0f}]/3)^.5"]
		# open the report for output
		fCSV = open(DIR_CSV + TEST_NODE+'Inc_'+str(increment)+'.csv', 'w',newline='')
		writer = csv.writer(fCSV)
		writer.writerow(HEADER_CSV)

	if GENERATE_REPORT:
		primeRoots = 0
		maxRootFactor = 0
		maxNum = 0

		if GENERATE_INCREMENT_OUTPUT and increment <= MAX_INCREMENT_FILES:
			fTXT = open(DIR_TXT + TEST_NODE+'Inc_'+str(increment)+'.txt', 'w') # for running on laptop machine

	# loop through the first "startOfSequenceMax" integers, calculating the product of four integers that are
	# in an arithmetic sequencce separated by the current increment
	# Note that analysis has shown that the square root of the product for the current index (== i) can
	# be calculated as the sum: (i + (i+increment)**2). This is probably faster than doing the product and then taking the square root.
	for startInteger in range(1,START_OF_SEQUENCE_MAX):
		factorsList = []
		# the text file output header is printed every 45 lines.
		if GENERATE_REPORT and GENERATE_INCREMENT_OUTPUT and increment <= MAX_INCREMENT_FILES:
			if startInteger % INCREMENTS_LINES_PER_PAGE == 1:
					if startInteger > 1:
						print("", file=fTXT)
					print(HEADER_LTXT, file=fTXT)
					print(HEADER_0, file=fTXT)
					print(HEADER_1, file=fTXT)
					print(HEADER_TXT, file=fTXT)
					print(HEADER_LTXT, file=fTXT)

		# squareNum = i * (i + increment) * (i + 2*increment) * (i + 3*increment) + increment**4
		# factorizationTestNum = sqrtNum = num ** 0.5
		# alternative, equivalent values
		i1Sum = startInteger + increment
		factorizationTestNum = sqrtNum = startInteger*increment + i1Sum * i1Sum	 #factorizationTestNum = sqrtNum = i*increment + (i+increment)²
		# squareNum = (iProd + i1Sum**2)**2
		squareNum = sqrtNum * sqrtNum

		# calculate the modulo values starting with increment = 2.
		if startInteger <= increment and increment > 1:
			sqrtModList.append(sqrtNum % increment)
			numModList.append(squareNum % increment)

		if squareNum in squaresDict:	  # have we already seen this number when processing a previous arithmetic sequence?
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

		if GENERATE_SHEET and GENERATE_INCREMENT_OUTPUT and increment <= MAX_INCREMENT_FILES:
			if startInteger >= 2*increment + 1:
				sheetRow = startInteger + 1
				csvRow = [startInteger, squareNum, sqrtNum,f"=(B{sheetRow}+B{sheetRow-increment}+B{sheetRow-2*increment})/3",f"=SQRT(D{sheetRow})", \
			   f"=(C{sheetRow}+E{startInteger+1})/2",f"=SQRT(F{startInteger+1})"] + factorsList
			else:
				csvRow = [startInteger, squareNum, sqrtNum,"_","_","_","_"] + factorsList
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

			
			if GENERATE_INCREMENT_OUTPUT and increment <= MAX_INCREMENT_FILES:
				startIntegerT = FormatWithCommas(startInteger)
				squareNumT = FormatWithCommas(squareNum)
				sqrtNumT = FormatWithCommas(sqrtNum)
				print(f'{startIntegerT:8}{squareNumT:^30}{sqrtNumT:^}({factors})', file=fTXT)

		if squareNum not in factorsDict:
			factorsDict[squareNum] = factorsList

		# every so often: show that we're still alive
		if startInteger > 1 and startInteger % 250 == 1:
			sys.stdout.write(".")
			sys.stdout.flush()
			if startInteger % 2500 == 1:
				print(f"{startInteger} products analyzed")

	if GENERATE_REPORT:
		if GENERATE_INCREMENT_OUTPUT and increment <= MAX_INCREMENT_FILES:
			print(f"There are {primeRoots:d} prime square roots out of {START_OF_SEQUENCE_MAX - 1:d} calculations.", file=fTXT)
			print(f"Maximum prime factor: {maxRootFactor:.0f} (at test for {maxNum:.0f})", file=fTXT)

			if increment % 2 == 1:
				moduloMidpoint = (increment - 1) / 2
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


	if GENERATE_SHEET and GENERATE_INCREMENT_OUTPUT and increment <= MAX_INCREMENT_FILES:
		fCSV.close()
	if GENERATE_REPORT and GENERATE_INCREMENT_OUTPUT and increment <= MAX_INCREMENT_FILES:
		fTXT.close()

	ct = len(splits)
	splits[ct] = time.time()
	print(f"Processing complete for increment {increment:d}, duration {(splits[ct] - splits[ct-1]):4.3f}")
#end 'for increment in range(1,...'

if GENERATE_SQUARES_OUTPUT:
	#
	# Each calculated square number was added as a key to a dictionary (squaresDict). That dictionary keeps track of all the
	# four number arithmetic sequences and the difference between consecutive numbers in that sequence.
	# So, for instance, the number 43681 (209 * 209) is generated by:
	#	13 * 14 * 15 * 16 + 1	(start = 13,diff = 1: 1**4)
	#	8 * 13 * 18 * 23 + 625	(start = 8, diff = 5: 5**4)
	#	5 * 13 * 21 * 29 + 4096 (start = 5, diff = 8: 8**4)
	#	1 * 14 * 27 * 40 + 28561 (start = 1, diff = 13: 13 ** 4)
	# Thus the dictionary entry for 43681 is: 43681,209,13,1,8,5,5,8,1,13
	#
	print("Multiple starting integer/increment pairs generate the same square number. Iterate over the")
	print("squaresDict collection to find these sequences/increment pairs.")
	# "e.g.: 43861 == 209*209 
	# == 13*14*15*16+1 
	# == 8*13*18*23+625 (5^4) 
	# == 5*13*21*29+512 (8^4) 
	# == 1 * 14 * 27 * 40 + 28561 (13^4)")
osq = collections.OrderedDict(sorted(squaresDict.items())) #osq: o_rdered sq_uares dictionary
osqCt = 0
lMax = -1

oddSequences = {}
with open(DIR_TXT+TEST_NODE+"bigdictionary.txt","w") as bdo:
	for o in osq:
		listLen = int((len(osq[o]) - 2))
		listLenHalf = listLen / 2
		if ODDSEQUENCES_SINGLET:
			testSeq = 1
		else:
			testSeq = 3
		if not listLenHalf % 2 == 0 and listLenHalf >= testSeq:
			oddSequence = osq[o][2:]
			if oddSequence[0] == oddSequence[-1]:
				n = str(osq[o][0])+"("+str(osq[o][1])+")"
				oddSeqKey = f'{n:>30}) ==> {oddSequence[int(listLenHalf)-1]:<6}'
				factorsKey = osq[o][0]
				oddSequences[oddSeqKey] = "[" + ", ".join(str(num) for num in oddSequence) + "]    (" + ", ".join(f'{num:.0f}' for num in factorsDict[factorsKey]) + ")" 
		print(listLen, ":", osq[o][:2], osq[o][2:], file=bdo)

		osqCt += 1
		if listLen > lMax:
			lMax = listLen
	print(f"\nMax length of dictionary entries: {lMax:d}", file=bdo)
with open(DIR_TXT+TEST_NODE+"OddSequences.txt","w") as odd:
	ons = " " if ODDSEQUENCES_SINGLET else " (>1) "
	print(f'Report of resultant square numbers with an odd number{ons}of n/k pairs:\n', file=odd)
	for k,v in oddSequences.items():
		print(f'{k}: {v}', file=odd)

	if osqCt == 0:
		print("No data", file=bdo)

if GENERATE_SHEET and GENERATE_SQUARES_OUTPUT:
	print("Squares analysis .csv sheets")
	ct = len(splits)
	splits[ct] = time.time()		 
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
			fName = TEST_NODE+"squares_"+str(fileNo)+".csv"
			print(f"Processing {fName}")
			fsqCSV = open(DIR_CSV + fName,"w",newline='')
			writer = csv.writer(fsqCSV)
			writer.writerow(fullHdr)
			fileNo += 1

		factorsList = factorsDict[key]
		# csv() does not like empty values
		for startInteger in range(header2_len - len(val) + 2):
			vCSV.append("_")

		newlist = vCSV + factorsList
		writer.writerow(newlist)
	ct2 = len(splits)
	splits[ct2] = time.time()
	fsqCSV.close()
	print(f".csv analysis duration {splits[ct2] - splits[ct]:4.3f} seconds")

if GENERATE_REPORT and GENERATE_SQUARES_OUTPUT:
	print("Squares analysis .txt reports ")
	oddSeqMax = -1
	ct = len(splits)
	splits[ct] = time.time()
	files = 0
	lines = 0
	pages = 0
	# after this many pages, squaresN.txt is closed and a new file is created
	# (N=1,2,3,...)
	SQUARES_PAGES_PER_FILE = 250
	# number of data lines before printing a new set of headers
	SQUARES_LINES_PER_PAGE = 50 
	header = f"{'Number(Root)':^30}"
	header2 = f"{'1st of four':^15}{'incr':^10}"
	header = header + header2 * 4 + "Prime Factors"
	headerL = "-" * len(header)

	for key, val in osq.items():
		vTXT = [FormatWithCommas(number) for number in val.copy()]
		if lines % SQUARES_LINES_PER_PAGE == 0:
			pages += 1
			if pages % SQUARES_PAGES_PER_FILE == 1:
				if pages > 1:
					fsqTXT.close()
				files += 1
				fName = TEST_NODE+"squares"+f'{files}'+".txt"
				print(f"Processing {fName}")
				fsqTXT = open(DIR_TXT + fName,"w")
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
		ast = " "
		if not len(vTXT2)  % 4 == 0:
			if vTXT2[0] == vTXT2[-1]: # only set * if we have a complete set of n/k
				ast = "*"
		
#		appendLen = lMax + 12 - lvTXT2
		vTXT2 = vTXT2 + ["-"] * 16 #appendlen

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
					numSqrt = ast+"{0:^30}".format("{0}({1})".format(squareNum, sqrt))+"{0:^15}{1:^10}{2:^15}{3:^10}{4:^15}{5:^10}{6:^15}{7:^10}".format(i1Sum, inc1, i2,inc2, i3, inc3, i4, inc4)
					print("{0:s}{1:s}".format(numSqrt,factors),file=fsqTXT)
				else:
					numSqrt = " {: <30}".format(" ")+"{0:^15}{1:^10}{2:^15}{3:^10}{4:^15}{5:^10}{6:^15}{7:^10}".format(i1Sum, inc1, i2, inc2, i3, inc3, i4,inc4)
					print(f"{numSqrt:s}", file=fsqTXT)
		except IndexError:
			print("Index out of range")
			print(f'{lMax = } {idx =} {vTXT2 = }')
			sys.exit()

		lines += 1
	splits[len(splits)] = time.time()
	ct2 = len(splits)
	splits[ct2] = time.time()
	print(f".txt analysis duration {splits[ct2] - splits[ct]:4.3f} seconds")

ct = len(splits)
splits[ct] = time.time()
print(f"Total Duration {splits[ct] - splits[0]:4.3f} seconds")
print("Processing complete.")

#n * (n+k) * (n + 2*k) * (n+3*k) + k^4
# =n* (n+2*k) * (n+k)*(n+3*k) + k^4
# =(n^2+2*k*n) * (n^2 + 4*k*n + 3*k^2) + k^4
# =(n^2*n^2 + 2*k*n*n^2) + (4*k*n*n^2 + 4*k*n*2*k*n) + (3*k^2 * n^2 + 3*k^2 * 2*k*n) +k^4
# =n^4		+ 2*k*n^3	 + 4*k*n^3	  + 8*k^2*n^2	 +	3*k^2*n^2	+ 6*k^3*n		 + k^4
# =n^4		+ 6*k*n^3				  + 11*k^2n^2					+ 6*k^3*n		 + k^4
#
# (n*k + (n+k)^2)^2
# =(n*k + n^2 + 2*k*n + k^2)^2
# =(n*k + n^2 + 2*k*n + k^2) * (n*k + n^2 + 2*k*n + k^2)
# =(n*k*n*k + n^2*n*k + 2*k*n*n*k + k^2*n*k) + (n*k*n^2 + n^2*n^2 + 2*k*n*n^2 + k^2*n^2) + (n*k*2*k*n + n^2*2*k*n + 2*k*n*2*k*n + k^2*2*k*n) + (n*k*k^2 + n^2*k^2 + 2*k*n*k^2) + (k^2*k^2)
# =(k^2*n^2 + k*n^3 + 2*k^2*n^2 + k^3*n) + (k*n^3 + n^4 + 2*k*n^3 + k^2*n^2) + (2*k^2*n^2 + 2*k*n^3 + 4*k^2*n^2 + 2*k^3*n) + (k^3*n + k^2*n^2 + 2*k^3*n + k^4)
# =n^4 + (k*n^3 + k*n^3 + 2*k*n^3 + 2*k*n^3) + (k^2n^2 + 2*k^2*n^2 + k^2*n^2 + 2*k^2*n^2 + 4*k^2*n^2 + k^2*n^2) + (k^3*n + 2*k^3*n + k^*n + 2*k^3*n) + k^4
# =n^4 + 6*k*n^3 + 11*k^2n^2 + 6*k^3*n + k^4
#
# (n^2 + 3*k*n + k^2)^2
# =(n^2 + 3*k*n + k^2) * (n^2 + 3*k*n + k^2)
# =n^4 + 3*k*n^3 + n^2*k^2 + 3*k*n^3 + 9*k^2*n^2 + 3*k^3*n + k^2+n^2 + 3*k^3*n + k^4
# =n^4 + (3*k*n^3 + 3*k*n^3) + (n^2*k^2+9*k^2*n^2) + (3*k^3*n + 3*k^3*n) + k^4
# =n^4 + 6*k*n^3 + 11*k^2*n^2 + 6*k^3*n + k^4
#
