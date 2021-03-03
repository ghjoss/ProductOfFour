#!/usr/bin/python3
import sys
import time

def f1(n,i):
	return (n * (n+i) * (n+2*i) * (n+3*i)) + i ** 4
def f2(n,i):
	return (n * (n+i) * (n+2*i) * (n+3*i)) + i * i * i * i
def f3(n,i):
	return (n ** 2 + 3 * n * i + i ** 2) ** 2
def f4(n,i):
	return (n * n + 3 *n * i + i  * i) ** 2
def f5(n,i):
	k = n * n + 3 *n * i + i  * i
	return k * k
def f6(n,i):
	return (n * i + (n+i)**2) ** 2
def f7(n,i):
	k = n * i + (n+i) * (n+i)
	return k * k
functionsStr = ["n * (n+i) * (n+2*i) * (n+3*i)) + i ** 4",
		"(n ** 2 + 3 * n * i + i ** 2) ** 2",
		"(n * n + 3 * n * i  + i * i) ** 2",
		"k=(n * n + 3 * n * i  + i * i), then k * k",
		"(n * i + (n+i) ** 2) ** 2",
	        "(n * (n+i) * (n+2*i) * (n+3*i)) + i * i * i * i",
		"k=n * i + (n+i) * (n+i), then k * k",
]
functions = [f1,f2,f3,f4,f5,f6,f7]
funcCount = len(functions)
avgs = []
minVals = []
maxVals = []

for i in range (0,funcCount):
	avgs.append(0.0)
	minVals.append(99.9)
	maxVals.append(0.0)

iterations = 100
f = open("./test.txt","w")
for test in range (0,funcCount):
	print("Testing {0:d}: {1:s}".format(test,functionsStr[test]),file=f)
	print("Testing {0:d}: {1:s}".format(test,functionsStr[test]))

	for count in range (0,iterations):
		testStart = time.time()
		for n in range (1,5001):
			for i in range (1,31):
				num = functions[test](n,i)
		duration = time.time() - testStart
		maxVals[test] = max(maxVals[test],duration)
		minVals[test] = min(minVals[test],duration)
		avgs[test] = avgs[test] + duration
#	print("For test {test:d} the duration was {duration:4.3f}".format(test=test,duration=duration))
print("\n ---",file=f)
print("\n ---")
for test in range (0,funcCount):
	print("{str:s} (test {test:d}):".format(str=functionsStr[test],test=test),file=f)
	print("         Average duration: {avg:4.3f}".format(avg=avgs[test] / iterations),file=f)
	print("         Minimum duration: {min:4.3f}".format(min=minVals[test]),file=f)
	print("         Maximum duration: {max:4.3f}".format(max=maxVals[test]),file=f)
	print(" ---",file=f)
print("\n ---")
for test in range (0,funcCount):
	print("{str:s} (test {test:d}):".format(str=functionsStr[test],test=test))
	print("         Average duration: {avg:4.3f}".format(avg=avgs[test] / iterations))
	print("         Minimum duration: {min:4.3f}".format(min=minVals[test]))
	print("         Maximum duration: {max:4.3f}".format(max=maxVals[test]))
	print(" ---")
f.close()
exit()
