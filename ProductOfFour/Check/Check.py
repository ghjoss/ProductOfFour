import sys
import collections
import time
import re

#Controls:
# bash:
#	True - Linux file system paths
#	False - Windows file system paths
#
bash = True
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
	multSign = "x"
else:
	path = "F:\\Source\\PythonApps\\ProductOfFourSheet"
	filePath = "F:\\Source\\PythonApps\\ProductOfFourSheet\\Output\\"
	multSign = "\xD7"

sys.path.append(path)
import _50KPrimes


foundDict = {}
byFile = [dict() for x in range(fileCount+1)]

r = re.compile(".+\((?P<Factors>(?:\d+\s*[\u00D7]?\s*)+)\)")
for w in _50KPrimes.primes:
	foundDict[str(w)] = False

fOut = open(filePath + "PrimesInFiles.txt", "w")

for fileNo in range(1,fileCount + 1):
	f = filePath + "ProductOfFour_Increment_" + str(fileNo) + ".txt"
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
			wordList = re.sub("[^\w]"," ",factors).split()
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

				
	if skip < 0:
		fIn.close()
		if primeLineCt > 0:
			primeLineCt = 0
			print("  " + primeLine,file=fOut)
			primeLine = ""
fOut.close()


fOut = open(filePath + "PrimesInFilesSorted.txt)","w")
for fileNo in range(1, fileCount + 1):
	if fileNo > 1:
		print("\n",file=fOut)
	print(filePath + "ProductOfFour_Increment_" + str(fileNo) + ".txt",file=fOut)
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








