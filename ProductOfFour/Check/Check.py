import sys
import collections
import time
import re

#Controls:
# bash:
#	True - Linux file system paths
#	False - Windows file system paths
#
bash = False
# fileCount:
#   Number of files that were output by ProductOfFour.py.
#	File names are in the format <path>ProductOfFour_Increment_n, 
#	where n ranges from 1 to fileCount.
fileCount = 1200

# path:
# if bash == False:
#	F:\Source\PythonApps\ProductOfFourSheet\_50KPrimes.py
# if bash == True:
#	/mnt/f/Source/PythonApps/ProductofFourSheet"
if bash:
	path = "/mnt/f/source/PythonApps/ProductOfFourSheet"
	filePath = "/mnt/f/source/PythonApps/ProductOfFourSheet/Output/"
else:
	path = "F:\\Source\\PythonApps\\ProductOfFourSheet"
	filePath = "F:\\Source\\PythonApps\\ProductOfFourSheet\\Output\\"

sys.path.append(path)
import _50KPrimes


foundDict = {}
r = re.compile(".+\((?P<Factors>(?:\d+\s*[\u00D7]?\s*)+)\)")

for w in _50KPrimes.primes:
	foundDict[str(w)] = False

fOut = open(filePath + "PrimesInFiles(py).txt", "w")

for fileNo in range(1,fileCount + 1):
	f = filePath + "ProductOfFour_Increment_" + str(fileNo) + ".txt"
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
		m = r.search(line)
		if m != None:
			factors = m.group("Factors")
			factors = factors.replace("\xD7"," ")
			wordList = re.sub("[^\w]"," ",factors).split()
			for pr in wordList:
				if pr in foundDict:
					if not foundDict[pr]:
						foundDict[pr] = True
						primeLineCt += 1
						primeLine = primeLine + (str(pr) + "(@" + str(currentLine) + ")").ljust(15)
						if primeLineCt == 7:
							primeLineCt = 0
							print("  " + primeLine,file=fOut)
							primeLine = ""

				
	if skip < 0:
		fIn.close()
		if primeLineCt > 0:
			primeLineCt = 0
			print("  " + primeLine,file=fOut)
			primeLine = ""
fOut.close()







