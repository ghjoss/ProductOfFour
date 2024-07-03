import sys
import collections
import time
import re

#Controls:
# bash:
#	True - Linux file system paths
#	False - Windows file system paths
#
if len(sys.argv) > 1:
	arg1 = sys.argv[1].upper()
else:
	arg1 = "W"

if arg1.startswith("B"):
	bash = True
else:
	bash = False

# fileCount:
#   Number of files that were output by ProductOfFour.py.
#	File names are in the format <path>ProductOfFour_Increment_n, 
#	where n ranges from 1 to fileCount.
if len(sys.argv) > 2:
	arg2 = sys.argv[2]
else:
	arg2 = 1200

if str(arg2).isnumeric():
	fileCount = arg2
else:
	fileCount = 1200

# path:
# if bash == False:
#	F:\Source\PythonApps\ProductOfFourSheet
# if bash == True:
#	/mnt/f/Source/PythonApps/ProductofFourSheet"
if bash:
	path = "/mnt/d/source/PythonApps/ProductOfFourSheet"
	filePath = "/mnt/d/source/PythonApps/ProductOfFourSheet/Output/"
	multSign = "x"
else:
	path = "d:\\Source\\PythonApps\\ProductOfFourSheet"
	filePath = "d:\\Source\\PythonApps\\ProductOfFourSheet\\Output\\"
	multSign = "\xD7"

sys.path.append(path)
import _100KPrimes


foundDict = {}
fileDict = {}
byFile = [dict() for x in range(fileCount+1)]

r = re.compile(r".+\((?P<Factors>(?:\d+\s*[x]?\s*)+)\)")

for w in _100KPrimes.primes:
	foundDict[str(w)] = False

fOut = open(filePath + "PrimesInFiles.txt", "w")

for fileNo in range(1,fileCount + 1):
	f = filePath + "Inc_" + str(fileNo) + ".txt"
	byFileCt = 0
	print("processing " + f + "...")

	print(f,file=fOut)
	currentLine = 0
	fIn = open(f,"r")
	skip = 0
	primeLine = ""
	primeLineCt = 0
	for line in fIn:
		currentLine += 1
		#if currentLine % 100 == 0:
		#	print(currentLine)
		if skip > 0:
			skip = skip - 1
			continue
		if line.startswith("---"):
			skip = 4
			continue
		if line.find("There are") >= 0:
			skip = -1
			break # no more relevant lines in fIn
		m = r.match(line)
		if m != None:
			factors = m.group("Factors")
			factors = factors.replace(multSign," ")
			wordList = re.sub(r"[^\w]"," ",factors).split()

			for pr in wordList:
				if pr in foundDict:
					if not foundDict[pr]:
						foundDict[pr] = True
						byFileCt += 1
						byFile[fileNo][byFileCt] = str(pr).rjust(6,"0") + "(@" + str(currentLine) + ")"
						primeLineCt += 1
						primeLine = primeLine + (str(pr) + "(@" + str(currentLine) + ")").ljust(15)
						if primeLineCt == 7:
							primeLineCt = 0
							print("  " + primeLine,file=fOut)
							primeLine = ""
						fileDict[int(pr)] = fileNo

				
	if skip < 0:
		fIn.close()
		if primeLineCt > 0:
			primeLineCt = 0
			print("  " + primeLine,file=fOut)
			primeLine = ""
fOut.close()

fOut = open(filePath + "PrimesByInitialFile.txt","w")
osq = collections.OrderedDict(sorted(fileDict.items()))
s:str = ""
i=0
for key,val in osq.items():
	s = s + "{}({}) ".format(key,val)
	i+=1
	if i == 8:
		print(s,file=fOut)
		i = 0
		s=""

fOut = open(filePath + "PrimesInFilesSorted.txt","w")
for fileNo in range(1, fileCount + 1):
	if fileNo > 1:
		print("\n",file=fOut)
	print(filePath + "Inc_" + str(fileNo) + ".txt",file=fOut)
	byFileKeysS = sorted(byFile[fileNo],key=byFile[fileNo].get)
	byFileS = {}
	byFileSKey = 0
	for w in byFileKeysS:
		byFileSKey += 1
		byFileS[byFileSKey] = (byFile[fileNo])[w]
	primeLineCt = 0
	primeLine = ""
	for w in byFileS:
		prStr = byFileS[w]
		t = prStr.find("(@")
		u = prStr.find(")")
		pr = int(prStr[0:t])
		currentLine = int(prStr[t+2:u])
		primeLine = primeLine + (str(pr) + "(@" + str(currentLine) + ")").ljust(15)
		primeLineCt += 1
		if primeLineCt == 7:
			primeLineCt = 0
			print("  " + primeLine,file=fOut)
			primeLine = ""

if primeLineCt > 0:
	if primeLineCt > 0:
		primeLineCt = 0
		print("  " + primeLine,file=fOut)
		primeLine = ""
fOut.close()








