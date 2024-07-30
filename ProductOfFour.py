""" 
	The product of four integers in an arithmetic progression of four integers when 
	added to the difference value raised to the fourth power is always a squared integer
	value. As an example, for the progession 2 4 6 8  (difference = 2):

					2 * 4 * 6 * 8 + 2^4 = 384 + 16 = 400 = 20^2

	This program computes and reports these squared values up to a maximum user specified difference.
	This is done across a range of starting integer in the progression, also user specified.

	See difference_max and start_Of_progression_max below.

	Also, see the On-line Encyclopedia of Integer Sequences (OEIS) article #A062938 (https://oeis.org/A062938)
	This sequence, generalized for all differences (not only inc=1), is used in the
	code below to evaluate the square roots without having to use the sqrt() function. 

	For difference=1: The square roots of the results are the values in sequence #A028387. 
	For difference=2: The square roots of the results are the positive values in sequence #A028875
	For difference=3: The square roots of the results are the positive values in sequence #A190576
	For difference=4: The square roots of the results are the positive values in sequence #A134594
	For difference=5 through difference=25, no sequences were found in the OEIS referencing the
	square roots.
"""
import os
import shutil
import glob
import errno
import sys
import collections
import time
import csv
import json

splits = {}
splits[0] = time.time()
# for debugging purposes, run with a smaller number of initial integers and
# a smaller number of sequence differences. Set debug=False to run with
# larger values
arg1 = "t"
DEBUG = True
if len(sys.argv) > 1:
	arg1 = sys.argv[1].lower()
	if arg1.startswith("f") or arg1 == "0":
		DEBUG = False

PATH = os.path.dirname(__file__) + "/"
"""
Process the configuration parameters .json file. See ProductOfFour.README.txt
for a description of the paramters.
TODO: Add a schema to validate the json parameters.
For START_OF_PROGRESSION_MAX and DIFFERENCE_MAX, add 1 to the .json file value
so that the upper value for range testing will be correct for loops.
"""
with open(PATH + "ProductOfFour.json","r") as jsonFile:
	jsonData = jsonFile.read()
	settings = json.loads(jsonData)
	if DEBUG:
		TEST_NODE = settings["debug"]["test_node"]
		START_OF_PROGRESSION_MAX = settings["debug"]["start_of_progression_max"] + 1
		DIFFERENCE_MAX = settings["debug"]["difference_max"] + 1
	else:
		TEST_NODE = settings["max"]["test_node"]
		START_OF_PROGRESSION_MAX = settings["max"]["start_of_progression_max"] + 1
		DIFFERENCE_MAX = settings["max"]["difference_max"] + 1

	OUTPUT_FOLDER = settings["output_folder"]
	# True=generate spreadsheet data, False=no spreadsheet data
	GENERATE_CSV_FILES = settings["generate_csv_files"]
	# True=generate ...txt files, false no files
	GENERATE_TXT_FILES = settings["generate_txt_files"]
	# True=generate ...INCn_.csv and ...INCn.txt files, false, no difference output
	GENERATE_DIFFERENCE_OUTPUT = settings["generate_difference_output"]
	# True=generate ...squares.csv & txt, false no squares output
	GENERATE_SQUARES_OUTPUT = settings["generate_squares_output"]

	# number of DIFF_... files to write (one each of .csv and .txt)
	MAX_DIFFERENCE_FILES = settings["max_difference_files"]

	SQUARES_PAGES_PER_FILE = settings["squares_pages_per_file"]
	SQUARES_LINES_PER_PAGE = settings["squares_lines_per_page"]
	DIFFERENCES_LINES_PER_PAGE = settings["differences_lines_per_page"]
	
	# set addThousandsSeparator to False to cause large numbers to be written without
	# a thousands, millions, ... ',' separator.
	ADD_THOUSANDS_SEPARATOR = settings["add_thousands_separator"]

	DELETE_OLD_OUTPUT = settings["delete_old_output"]
	ALL_SEQUENCES_PAGES_PER_FILE = settings["all_sequences_pages_per_file"]
	ALL_SEQUENCES_LINES_PER_PAGE = settings["all_sequences_lines_per_page"]

"""
	Delete a file cross-platform
	Args: file_path (str): The path to the file to be deleted
"""
def delete_file(file_path):
	try:
		if os.path.exists(file_path):
			if os.path.isfile(file_path):
				os.remove(file_path)
			else:
				pass
	except OSError as e:
		print(f"Error deleting file: {e}")
"""
Delete files matching a wildcard pattern
args: pattern (str): the wildcard pattern to match
"""
def delete_files_with_wildcard(pattern):
	files = glob.glob(pattern)
	for file in files:
		delete_file(file)

"""
	Function to format numbers with comma separators. This function only does
	this if ADD_THOUSANDS_SEPARATOR .json file parameter is set to True.
"""
def FormatWithCommas(num:int):
	return f'{num:,}' if ADD_THOUSANDS_SEPARATOR and isinstance(num,(int,float)) else str(num)


if not isinstance(MAX_DIFFERENCE_FILES,(int,float)):
	MAX_DIFFERENCE_FILES = DIFFERENCE_MAX # write all of them

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

if not GENERATE_CSV_FILES and not GENERATE_TXT_FILES:
	print("Check the file ProductOf_Four.json:\n" \
	   "Either of the values generate_sheet and generate_report \n (or both) must be true. Both were 'false'.")
	exit()
if not GENERATE_DIFFERENCE_OUTPUT and not GENERATE_SQUARES_OUTPUT:
	print("Check the file ProductOfFour.json:\n"
	   "Either of the values generate_difference_output and generate_squares_output \n (or both) must be true. Both were 'false'.")
	exit()
# Prime lists, _100KPrimes or _50KPrimes
sys.path.append('.')


"""
	Get sigma[2,n^2]. This is the sum of the squares of the divisors
	of the passed number squared. Example: for num=2, num² = 4. Divisors
	of 4 are 1, 2 and 4. Squares of the divisors: 1, 4, 16. Sum=21.
	Thus sigma_2(4) = 21
"""
def sigma_2(num):
	numSq = num * num
	divisors = [d for d in range(1,numSq+1) if numSq%d == 0]
	return sum(d**2 for d in divisors)

import _100KPrimes				#100,000 prime numbers in a list named "primes"
# maxPrime: in the array of primes, this is the offset of the last
# prime to process.
MAX_PRIME = 100000				#50000

# add the primes as keys to a dictionary "primeDict"
primesDict = {} # add the p

for w in _100KPrimes.primes:
	primesDict[w] = True

squaresDict = {}			# dictionary of lists of the generated squares and square roots. Key = square number
oddsDict = {}
factorsList = []			# list of the prime factors of the square roots
factorsDict = {}			# dictionary of lists of the prime factors of the square roots

"""
Delete older generated files. Only delete if we are creating new versions.
While new versions will overwrite older ones, the MAX_DIFFERENCE_FILES
count may be lower for this run. We want to get rid of the ones that
were written in an older run but won't be written in this one.
"""
if DELETE_OLD_OUTPUT:
	if GENERATE_CSV_FILES:
		if GENERATE_DIFFERENCE_OUTPUT:
			delete_files_with_wildcard(DIR_CSV + TEST_NODE + "Diff*.csv")
		if GENERATE_SQUARES_OUTPUT:
			delete_files_with_wildcard(DIR_CSV + TEST_NODE + "squares*.csv")
	if GENERATE_TXT_FILES:
		if GENERATE_DIFFERENCE_OUTPUT:
			delete_files_with_wildcard(DIR_TXT + TEST_NODE + "Diff*.txt")
		if GENERATE_SQUARES_OUTPUT:
			delete_files_with_wildcard(DIR_TXT + TEST_NODE + "squares*.txt")

"""
 the difference between successive integers in the product of four integers is represented by the
 variable 'difference'. These differences will be iterated from 1 through DIFFERENCE_MAX. The program will 
 calculate a(n) for each difference iterated up to START_OF_PROGRESSION_MAX calculations per difference.
 """
for difference in range(1,DIFFERENCE_MAX):
	""" 
	 to the product of four integers separated by 'difference' will be added difference to the 4th power
	 this will make the product + the 4th power of difference a perfect square integer.
	"""
	difference_4 = difference ** 4
	sqrtModList = []	# list of the first <difference> values of <difference> mod(square-root-of calculated integer)
	numModList = []		# list of the first <difference> values of <difference> mod(calculated integer)

	if GENERATE_CSV_FILES and GENERATE_DIFFERENCE_OUTPUT and difference <= MAX_DIFFERENCE_FILES:

		# open the report for output
		fCSV = open(DIR_CSV + TEST_NODE+'Diff_'+str(difference)+'.csv', 'w',newline='')
		writer = csv.writer(fCSV)
		writer.writerow(["n","a(n)","(a(n))^.5","S[n]^2","S[n]","(S[n]+(a(n))^.5)/2","(S[n]+(a(n))^.5)/2)^.5"] + \
			["factor"] * 13 + \
			[f"  difference=={difference:.0f}  S[n]=(a(n)+a(n-{difference:.0f})+a(n-{2*difference:.0f})/3)^.5"])

	if GENERATE_TXT_FILES:
		primeRoots = 0
		maxRootFactor = 0
		maxNum = 0

		if GENERATE_DIFFERENCE_OUTPUT and difference <= MAX_DIFFERENCE_FILES:
			fTXT = open(DIR_TXT + TEST_NODE+'Diff_'+str(difference)+'.txt', 'w') # for running on laptop machine
	""" 
		loop through the first "startOfSequenceMax" integers, calculating the product of four integers that are
		in an arithmetic progression, separated by the current "difference" value.
		Note that analysis has shown that the square root of the product for the current index (== n) can
		be calculated as the sum: (n + (i+difference)**2). This is probably faster than doing the product and then 
		taking the square root.
	"""
	for startInteger in range(1,START_OF_PROGRESSION_MAX):
		factorsList = []
		# the text file output header is printed every 45 lines.
		if GENERATE_TXT_FILES and GENERATE_DIFFERENCE_OUTPUT and difference <= MAX_DIFFERENCE_FILES:
			if startInteger % DIFFERENCES_LINES_PER_PAGE == 1:
					if startInteger > 1:
						print("", file=fTXT)
					print("-"*72, file=fTXT)
					print("difference == {0:d}".format(difference), file=fTXT)
					print("a(n) == (n x (n+{0:d}) x (n+{1:d}) x (n+{2:d}) + {3:d})".format(difference,2*difference,3*difference,difference_4) + \
		   				" -or- a(n) == (n x {0:d} + (n + {0:d})²)²".format(difference), file=fTXT)
					print("{0:<8}{1:^30}a(n)^0.5(factors)".format("n","a(n)"), file=fTXT)
					print("-"*72, file=fTXT)

		"""
	 		squareNum = n * (n + difference) * (n + 2*difference) * (n + 3*difference) + difference**4
			factorizationTestNum = sqrtNum = a(n) ** 0.5
			alternative, equivalent values
		 """
		i1Sum = startInteger + difference
		factorizationTestNum = sqrtNum = startInteger*difference + i1Sum * i1Sum  #factorizationTestNum = sqrtNum = i*difference + (i+difference)²
		# squareNum = (iProd + i1Sum**2)**2
		squareNum = sqrtNum * sqrtNum

		# calculate the modulo values starting with difference = 2.
		if startInteger <= difference and difference > 1:
			sqrtModList.append(sqrtNum % difference)
			numModList.append(squareNum % difference)
		""" 
			when n (startInteger) and k (difference) are equal, then this is the middle pair of a
			sequence of pairs that generate the same a(n). THis is therefore part of an odd number
			such pairs.
		"""
		if startInteger == difference:
			oddsDict[squareNum] = [startInteger]

		if squareNum in squaresDict:	  # have we already seen this number when processing a previous arithmetic sequence?
			# yes, append the current value of n and the difference to the list entry for this number
			sqList = squaresDict[squareNum]	 # get the list
			sqList.append(startInteger)		 # add current '1st of the four arithmetic sequence' value (n)
			sqList.append(difference)		 # add the current difference value
		else:
			# no, add a new dictionary entry with key = 'a(n)' (a list)
			squaresDict[squareNum] = [squareNum, sqrtNum, startInteger, difference]

		# get prime factors of the square root of the calculated number
		if squareNum in factorsDict:		#have we already found the factors of this number?
			# yes, just retrieve the previously determined factors
			factorsList = factorsDict[squareNum]
		else:
			# no, this is a number we have not yet factored
			if sqrtNum in primesDict:	# is the current square root one of the first 50K primes in the primes list
				# yes, no need to factor further
				factorsList.append(sqrtNum)
				if GENERATE_TXT_FILES and sqrtNum > maxRootFactor:
					maxNum = squareNum
					maxRootFactor = sqrtNum
			else:
				# no, this is the first time factoring the sqrtNum
				breakJ = 0	# controls whether to leave the "while j <...." loop below
				j = 0		# loop index for the list[] of the first 50000 primes
				sqrtFactorizationTestNum = sqrtNum ** 0.5  # max value to test
				while j < MAX_PRIME and breakJ == 0:
					p = _100KPrimes.primes[j]
					""" 
						There is no need to continue trying to find factors of the current
						test number if we have not found one yet and the next prime > square
						root of the test number or if the test number is in the table of
						primes.
					 """
					if p > sqrtFactorizationTestNum or factorizationTestNum in primesDict:
						factorsList.append(factorizationTestNum)
						if GENERATE_TXT_FILES and factorizationTestNum >= maxRootFactor:
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

		if GENERATE_CSV_FILES and GENERATE_DIFFERENCE_OUTPUT and difference <= MAX_DIFFERENCE_FILES:
			if startInteger >= 2*difference + 1:
				sheetRow = startInteger + 1
				csvRow = [startInteger, squareNum, sqrtNum,f"=(B{sheetRow}+B{sheetRow-difference}+B{sheetRow-2*difference})/3",f"=SQRT(D{sheetRow})", \
			   f"=(C{sheetRow}+E{startInteger+1})/2",f"=SQRT(F{startInteger+1})"] + factorsList
			else:
				csvRow = [startInteger, squareNum, sqrtNum,"_","_","_","_"] + factorsList
			writer.writerow([FormatWithCommas(number) for number in csvRow])

		if GENERATE_TXT_FILES:
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

			
			if GENERATE_DIFFERENCE_OUTPUT and difference <= MAX_DIFFERENCE_FILES:
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

	if GENERATE_TXT_FILES:
		if GENERATE_DIFFERENCE_OUTPUT and difference <= MAX_DIFFERENCE_FILES:
			print(f"There are {primeRoots:d} prime square roots out of {START_OF_PROGRESSION_MAX - 1:d} calculations.", file=fTXT)
			print(f"Maximum prime factor: {maxRootFactor:.0f} (at test for {maxNum:.0f})", file=fTXT)

			if difference % 2 == 1:
				moduloMidpoint = (difference - 1) / 2
				differenceIsOdd = True
			else:
				moduloMidpoint = difference / 2
				differenceIsOdd = False

			moduloPrint = ""
			moduloPrintHeader = "Calculated number modulo " + str(difference) + " cycle: "
			moduloPrintHeaderLen = len(moduloPrintHeader)
			rightAst = ""
			for offset, m in enumerate(numModList, start=1):
				if offset == moduloMidpoint:
					if differenceIsOdd:
						strM = ('* ' + str(m)).rjust(11)
						rightAst = " *"
					else:
						strM = ("* " + str(m) + " *").rjust(11)
				else:
					strM = (str(m) + rightAst).rjust(11)
					rightAst = ""

				moduloPrint = moduloPrint + strM
				if len(moduloPrint) >= 110 and difference != 1:
					print(moduloPrintHeader + moduloPrint, file=fTXT)
					moduloPrintHeader = " " * moduloPrintHeaderLen
					moduloPrint = ""

			if moduloPrint != "" and difference != 1:
				print(moduloPrintHeader + moduloPrint, file=fTXT)
			
			rightAst = ""
			moduloPrint = ""
			# pad print header to be as long as the prior header
			moduloPrintHeader = ("Square root modulo " + str(difference) + " cycle: ").ljust(moduloPrintHeaderLen)

			rightAst = ""
			for offset, m in enumerate(sqrtModList, start=1):
				if offset == moduloMidpoint:
					if differenceIsOdd:
						strM = ('* ' + str(m)).rjust(11)
						rightAst = " *"
					else:
						strM = ("* " + str(m) + " *").rjust(11)
				else:
					strM = (str(m) + rightAst).rjust(11)
					rightAst = ""

				moduloPrint = moduloPrint + strM
				if len(moduloPrint) >= 110 and difference != 1:
					print(moduloPrintHeader + moduloPrint, file=fTXT)
					moduloPrintHeader = " " * moduloPrintHeaderLen
					moduloPrint = ""

			if moduloPrint != "" and difference != 1:
				print(moduloPrintHeader + moduloPrint, file=fTXT)


	if GENERATE_CSV_FILES and GENERATE_DIFFERENCE_OUTPUT and difference <= MAX_DIFFERENCE_FILES:
		fCSV.close()
	if GENERATE_TXT_FILES and GENERATE_DIFFERENCE_OUTPUT and difference <= MAX_DIFFERENCE_FILES:
		fTXT.close()

	ct = len(splits)
	splits[ct] = time.time()
	print(f"Processing complete for difference {difference:d}, duration {(splits[ct] - splits[ct-1]):4.3f}")
#end 'for difference in range(1,...'

if GENERATE_SQUARES_OUTPUT:
	"""
		Each calculated square number was added as a key to a dictionary (squaresDict). That dictionary keeps track of all the
		four number arithmetic sequences and the difference between consecutive numbers in that sequence.
		So, for instance, the number 43681 (209 * 209) is generated by:
			13 * 14 * 15 * 16 + 1	(start = 13,diff = 1: 1**4)
			8 * 13 * 18 * 23 + 625	(start = 8, diff = 5: 5**4)
			5 * 13 * 21 * 29 + 4096 (start = 5, diff = 8: 8**4)
			1 * 14 * 27 * 40 + 28561 (start = 1, diff = 13: 13 ** 4)
		Thus the dictionary entry for 43681 is: 43681,209,13,1,8,5,5,8,1,13
	"""

	print("Multiple starting integer/difference pairs generate the same square number. Iterate over the")
	print("squaresDict collection to find these sequences/difference pairs.")
	"""
	e.g.: 43861 == 209*209 
		== 13*14*15*16+1 
		== 8*13*18*23+625 (5^4) 
		== 5*13*21*29+512 (8^4) 
		== 1 * 14 * 27 * 40 + 28561 (13^4)")
	"""
osq = collections.OrderedDict(sorted(squaresDict.items())) #osq: o_rdered sq_uares dictionary
osqCt = 0
lMax = -1

oddSequences = {}

allSeqFiles = 1
allSeqPages = 1
allSeqHdr1 = "a(n)(sq.rt)"+" "*29 + "Odd    [n1,k1,n2,k2,...,k1,n1]" + " " * 34 + "Factors" + " " * 54 + "sigma[2,n²]"
allSeqHdr0 = "-" * 192

allSeq = open(DIR_TXT+TEST_NODE+"allSequences"+str(allSeqFiles)+".txt","w")

print(f'{allSeqHdr0}\n{allSeqHdr1}\n{allSeqHdr0}',file=allSeq)
allSeqLines = 3

try:
	with open(DIR_TXT+TEST_NODE+"bigdictionary.txt","w") as bdo:
		for o in osq:
			listLen = int((len(osq[o]) - 2))
			print(listLen, ":", osq[o][:2], osq[o][2:], file=bdo)
			squareNum = osq[o][0]
			sequence = osq[o][2:]
			inOddSeq = squareNum in oddsDict
			factorsKey = osq[o][0]
			factorsStr = "(" + ", ".join(f'{num:.0f}' for num in factorsDict[factorsKey]) + ")"

			if inOddSeq:
				middlePairNum = oddsDict[squareNum][0]
				s2 = sigma_2(middlePairNum)
				s2s = str(s2)
				spaces = " " * (26 - len(s2s) - len(str(middlePairNum)))
				pr = f'sigma[2,{middlePairNum}²]: {s2s}{spaces}({s2s[-1:]})'
				dot = "."
			else:
				pr = ""
				dot = " "
			R =FormatWithCommas(osq[o][0])+"("+FormatWithCommas(osq[o][1])+")"
			print(f'{R:<40}{str(inOddSeq):<6} ',end="",file=allSeq)
			
			if sequence[0] == sequence[-1]: # do we have a full sequence?
				list_str = str(sequence)
			else:
				list_str = str(sequence)+" (partial)"

			padding = int(56-len(list_str))
			sequencePadded = list_str + dot * padding
			print(f'{sequencePadded} {factorsStr:60} {pr}',file=allSeq)
			allSeqLines += 1
			if allSeqLines % ALL_SEQUENCES_LINES_PER_PAGE == 1:
				allSeqPages += 1
				if allSeqPages >= ALL_SEQUENCES_PAGES_PER_FILE:
					allSeqLines = 0
					allSeq.close()
					allSeqFiles += 1
					allSeq = open(DIR_TXT+TEST_NODE+"allSequences"+str(allSeqFiles)+".txt","w")
					allSeqPages = 1
				print(f'\n{allSeqHdr0}\n{allSeqHdr1}\n{allSeqHdr0}',file=allSeq)
				allSeqLines += 5

			if inOddSeq:
				"""
				 this is a sequence with an odd number of n/k pairs. We have the a(n), diff=k,
				 result: use this to pull out the value of middle pair where n==k. Use this 
				 number to generate a sigma[2,n] value.
				"""
				middlePairNum = oddsDict[squareNum][0]
				n = FormatWithCommas(squareNum)+"("+FormatWithCommas(osq[o][1])+")"
				oddSeqKey = f'{n:>40}) ==> {middlePairNum:<6}'
				oddSequences[oddSeqKey] = ["[" + ", ".join(str(num) for num in sequence) + "]", \
						   				factorsStr, \
										f'sigma[2,{middlePairNum}²]: {s2s}{spaces}({s2s[-1:]})']

			osqCt += 1
			if listLen > lMax:
				lMax = listLen
		print(f"\nMax length of dictionary entries: {lMax:d}", file=bdo)
finally:
	# close allSeq
	try:
		allSeq.close()
	except:
		pass

with open(DIR_TXT+TEST_NODE+"OddSequences.txt","w") as odd:
	print(f'Report of resultant square numbers with an odd number of n/k pairs:\n', file=odd)
	for k,v in oddSequences.items():
		kv = f'{k}: {v[0]}'
		print(f'{kv:<150}', end="", file=odd)
		factStr = f'{v[1]}'
		print(f'{factStr:40}', end="",file=odd)
		print(f'{v[2]}',file=odd)
	if osqCt == 0:
		print("No data", file=bdo)

if GENERATE_CSV_FILES and GENERATE_SQUARES_OUTPUT:
	print("Squares analysis .csv sheets")
	ct = len(splits)
	splits[ct] = time.time()		 
	header = ["Number","Root"]
	header2 = ["1st of four","diff"]
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

if GENERATE_TXT_FILES and GENERATE_SQUARES_OUTPUT:
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
	header = f"{'a(n) (sq.root)':^30}"
	header2 = f"{'1st of four':^15}{'diff':^10}"
	header = header + header2 * 4 + " Prime Factors"
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
				difference_4 = vTXT2[idx+7]

				if idx == 0:
					numSqrt = ast+"{0:^30}".format("{0}({1})".format(squareNum, sqrt))+"{0:^15}{1:^10}{2:^15}{3:^10}{4:^15}{5:^10}{6:^15}{7:^10}".format(i1Sum, inc1, i2,inc2, i3, inc3, i4, difference_4)
					print("{0:s}{1:s}".format(numSqrt,factors),file=fsqTXT)
				else:
					numSqrt = " {: <30}".format(" ")+"{0:^15}{1:^10}{2:^15}{3:^10}{4:^15}{5:^10}{6:^15}{7:^10}".format(i1Sum, inc1, i2, inc2, i3, inc3, i4,difference_4)
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

"""
Three different ways to calculate a(n) for difference k:
1:
n * (n+k) * (n + 2*k) * (n+3*k) + k^4
 = n* (n+2*k) * (n+k)*(n+3*k) + k^4
 = (n^2+2*k*n) * (n^2 + 4*k*n + 3*k^2) + k^4
 = (n^2*n^2 + 2*k*n*n^2) + (4*k*n*n^2 + 4*k*n*2*k*n) + (3*k^2 * n^2 + 3*k^2 * 2*k*n) +k^4
 = n^4		+ 2*k*n^3	 + 4*k*n^3	  + 8*k^2*n^2	 +	3*k^2*n^2	+ 6*k^3*n		 + k^4
 = n^4		+ 6*k*n^3				  + 11*k^2n^2					+ 6*k^3*n		 + k^4

2:
 (n*k + (n+k)^2)^2
 = (n*k + n^2 + 2*k*n + k^2)^2
 = (n*k + n^2 + 2*k*n + k^2) * (n*k + n^2 + 2*k*n + k^2)
 = (n*k*n*k + n^2*n*k + 2*k*n*n*k + k^2*n*k) + (n*k*n^2 + n^2*n^2 + 2*k*n*n^2 + k^2*n^2) + (n*k*2*k*n + n^2*2*k*n + 2*k*n*2*k*n + k^2*2*k*n) + (n*k*k^2 + n^2*k^2 + 2*k*n*k^2) + (k^2*k^2)
 = (k^2*n^2 + k*n^3 + 2*k^2*n^2 + k^3*n) + (k*n^3 + n^4 + 2*k*n^3 + k^2*n^2) + (2*k^2*n^2 + 2*k*n^3 + 4*k^2*n^2 + 2*k^3*n) + (k^3*n + k^2*n^2 + 2*k^3*n + k^4)
 = n^4 + (k*n^3 + k*n^3 + 2*k*n^3 + 2*k*n^3) + (k^2n^2 + 2*k^2*n^2 + k^2*n^2 + 2*k^2*n^2 + 4*k^2*n^2 + k^2*n^2) + (k^3*n + 2*k^3*n + k^*n + 2*k^3*n) + k^4
 = n^4     + 6*k*n^3                 + 11*k^2n^2                   + 6*k^3*n         + k^4

3:
 (n^2 + 3*k*n + k^2)^2
 = (n^2 + 3*k*n + k^2) * (n^2 + 3*k*n + k^2)
 = n^4 + 3*k*n^3 + n^2*k^2 + 3*k*n^3 + 9*k^2*n^2 + 3*k^3*n + k^2+n^2 + 3*k^3*n + k^4
 = n^4 + (3*k*n^3 + 3*k*n^3) + (n^2*k^2+9*k^2*n^2) + (3*k^3*n + 3*k^3*n) + k^4
 = n^4    + 6*k*n^3                 + 11*k^2*n^2                  + 6*k^3*n          + k^4

"""