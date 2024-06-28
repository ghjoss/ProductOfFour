For all integers 'n', n * (n+1) * (n+2) * (n+3) + 1 is always a perfect square. This is in the OEIS as
sequence A062938. The comments note the general theory for this equation is: 
	n * (n+k) * (n+2k) * (n+3k) + k^4 is a perfect square.

ProductOfFour.py is a python program to calculate these squares for all starting integers from 1 to 5550
and all progressive differences from 1 to 1200. It runs for about 10 minutes on a PC with a core i7 CPU
running at 2.4Ghz. The program generates 2400 files, two for each difference. One of these files is a .csv
file and one is a simple text file. The file names start with "Inc_" and denote the difference. Thus for a
difference (increment) of 1, the files are Inc_1.csv and Inc_1.txt
Sample text report (first few lines). In this snippet, i is the first number in the four integers
sequence and the increment is 1. The report shows the number generated by the sequence product plus 1, 
the square root of that number and the prime factors of that square root.:

			------------------------------------------------------------------------
			increment == 1
			num == (i x (i+1) x (i+2) x (i+3) + 1) -or-  num == (i x 1 + (i + 1)²)²
				   i             num              num**0.5(factors)
			------------------------------------------------------------------------
				   1              25              5(5)
				   2             121              11(11)
				   3             361              19(19)
				   4             841              29(29)
				   5             1681             41(41)
				   6             3025             55(5 x 11)

For all increments > 1, each generated number, and its square root, the end of the .txt report shows the 
cycle of taking those numbers modulo the increment. Here is an example using the increment 9:

		There are 872 prime square roots out of 5550 calculations.
		Maximum prime factor: 30796849 (at test for 948445908328801)
		Calculated number modulo 9 cycle:           1          7          0        * 4        4 *          0          7          1          0
		Square root modulo 9 cycle:                 1          4          0        * 7        7 *          0          4          1          0


In addition to the above pairs of files ProductOfFour.py creates three text files related to the prime
factors of the square roots:
	o	PrimesInFiles.txt: this is summarized by the files Inc_1.txt - Inc_1200.txt. Whenever a prime factor is noted in a file, if it is the
		first time that prime factor has been seen, then it is associated with that file along with the line number where it occured.
		
			d:\Source\PythonApps\ProductOfFourSheet\Output\Inc_1.txt
			  5(@6)          11(@7)         19(@8)         29(@9)         41(@10)        71(@12)        89(@13)        
			  109(@14)       131(@15)       31(@16)        181(@17)       239(@19)       271(@20)       61(@21)        
			  379(@23)       419(@24)       461(@25)       101(@26)       599(@28)       59(@29)        701(@30)

		In the above sample, 5 was seen for the first time as a prime factor of a square root on line 6 of the file. Note that the line 
		numbers include the five header lines (see above) which are repeated every 45 lines. Note that this is ordered by the line number.
	o 	PrimesInFilesSorted.txt: this is similar to the PrimesInFiles.txt file, but is sorted by the prime factors.
	
			d:\Source\PythonApps\ProductOfFourSheet\Output\Inc_1.txt
			  5(@6)          11(@7)         19(@8)         29(@9)         31(@16)        41(@10)        59(@29)        
			  61(@21)        71(@12)        79(@33)        89(@13)        101(@26)       109(@14)       131(@15)       
			  139(@73)       149(@44)       151(@31)       179(@84)       181(@17)       191(@98)       199(@71)       
			  211(@36)       229(@91)       239(@19)       241(@61)       251(@133)      269(@81)       271(@20)
		  
	o	PrimesByInitialFile.txt: Sorted by prime factor, across all files. This denotes each prime factor found and the first file in which
		that factor was found. Note: this file is generated by the Check.py program which reads Inc_1.txt through Inc_1200.txt and parses for
		the prime factors listed on the lines.
		
			2(2) 3(3) 5(1) 7(7) 11(1) 13(13) 17(17) 19(1) 
			23(23) 29(1) 31(1) 37(37) 41(1) 43(43) 47(47) 53(53) 
			59(1) 61(1) 67(67) 71(1) 73(73) 79(1) 83(83) 89(1) 
			97(97) 101(1) 103(103) 107(107) 109(1) 113(113) 127(127) 131(1) 
			137(137) 139(1) 149(1) 151(1) 157(157) 163(163) 167(167) 173(173) 
			179(1) 181(1) 191(1) 193(193) 197(197) 199(1) 211(1) 223(223) 


There are additional files that track how many ways a square number can be calculated with the formula. The files 
are Squares.txt and Squares_x.csv (x=1,2,...). The .csv files each contain 250,000 lines. 
For instance, the number 43681 (209 * 209) is generated by:
			13 * 14 * 15 * 16 + 1   (start = 13,diff = 1: 1^4)
			8 * 13 * 18 * 23 + 625  (start = 8, diff = 5: 5^4)
			5 * 13 * 21 * 29 + 4096 (start = 5, diff = 8: 8^4)
			1 * 14 * 27 * 40 + 28561 (start = 1, diff = 13: 13 ^ 4)

This is on line 42 in Squares_1.csv and line 44 in Squares.txt