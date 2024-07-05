The product of four integers in a consecutive aritmetic sequence (difference = "increment")
added to the increment integer value raised to the fourth power is always a squared integer
value. As an example:
sequence 2 4 6 8  (increment = 2): 2 * 4 * 6 * 8 + 2^4 = 384 + 16 = 400

This program computes and reports these integer sequences up to a maximum user specified increment.
This is done across a range of sequence values, also user specified.

See INCREMENT_MAX and START_OF_SEQUENCE_MAX below.

See the on-line encyclopedia of integer sequences #A062938 (https://oeis.org/A062938)
This sequence, generalized for all increments (not only inc=1), is used in the
code to evaluate the square roots without having to use the sqrt() function. 
The comments in A062938 note the general formula for this equation: 
	n * (n+k) * (n+2k) * (n+3k) + k^4 is a perfect square.

For increment=1: The square roots of the generated numbers are the values in sequence #A028387. 
For increment=2: The square roots of the generated numbers are the positive values in sequence #A028875
For increment=3: The square roots of the generated numbers are the positive values in sequence #A190576
For increment=4: The square roots of the generated numbers are the positive values in sequence #A134594
For increment=5 through increment=25, no sequences were found referencing the
square roots.

ProductOfFour.py is a python program to calculate these squares for all starting integers from 1 to 5550
and all progressive differences from 1 to 2000. It runs for about 17 minutes on a PC with a core i7 CPU
running at 2.4Ghz. The program generates over 5000 files. For each of the 2000 differences there are
two files generated. One of these files is a .csv file and one is a simple text file. The file names start 
with "Inc_" and denote the difference. Thus for a difference (increment) of 1, the files are Inc_1.csv and 
Inc_1.txt.

Here is a snippet of a sample text report (first few lines). In this snippet, i is the first number in the 
four integers sequence and the increment is 1. The report shows the number generated by the sequence product plus 1, 
the square root of that number and the prime factors of that square root.:

			------------------------------------------------------------------------
			increment == 1
			num == (n x (n+1) x (n+2) x (n+3) + 1) -or-  num == (n x 1 + (n + 1)²)²
				   i             num              num^0.5(factors)
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

			----------------------------------------------------------------------------------------------------------------------------------------------
					Number(Root)           1st of four     incr     1st of four     incr     1st of four     incr     1st of four     incr   Prime Factors
			-----------------------------------------------------------------------------------------------------------------------------------------------
				 	 25(5)                    1           1            -           -            -           -            -           -     5
					121(11)                   2           1            1           2            -           -            -           -     11
					361(19)                   3           1            1           3            -           -            -           -     19
					400(20)                   2           2            -           -            -           -            -           -     2 x 2 x 5

This is on line 42 in Squares_1.csv and line 44 in Squares.txt

Lastly: the file bigdictionary.txt lists all generated numbers (and their square roots) which can be generated by
more than one starting integer:difference. This is an unformatted report of the data in the Squares_x... files. 
The prime factors of the square roots are not listed.
				...
				8 : [43681, 209] [13, 1, 8, 5, 5, 8, 1, 13]
				4 : [44521, 211] [7, 6, 6, 7]
				4 : [48400, 220] [12, 2, 2, 12]
				4 : [52441, 229] [11, 3, 3, 11]
				4 : [55696, 236] [10, 4, 4, 10]
				4 : [57121, 239] [14, 1, 1, 14]
				4 : [58081, 241] [9, 5, 5, 9]
				4 : [59536, 244] [8, 6, 6, 8]
				2 : [60025, 245] [7, 7]
				...
The first number (before the colon) is the number of files that contain a sequence that generates the 
number. The group following the colon (e.g. [43681, 209]) is the generated number and its square
root. The groups (e.g. [13,1,8,5,5,8,1,13]) are a list of starting number:difference pairs.

The second part of bigdictionary.txt lists all of the numbers with an odd number of number/difference
sequences:
				Report of sequences with an odd number of n/k pairs:

				25(5): [1, 1]
				400(20): [2, 2]
				2025(45): [3, 3]
				6400(80): [4, 4]
				15625(125): [5, 5]
				32400(180): [6, 6]
				60025(245): [7, 7]
				102400(320): [8, 8]
				164025(405): [9, 9]
				250000(500): [10, 10]
				366025(605): [19, 4, 11, 11, 4, 19]
				...

Notes:
	o	The math involved:

		For number n, difference (increment) k:

		----
		Formula 1:
		----
		  n * (n+k) * (n + 2*k) * (n+3*k) + k^4
		= n* (n+2*k) * (n+k)*(n+3*k) + k^4
		= (n^2+2*k*n) * (n^2 + 4*k*n + 3*k^2) + k^4
		= (n^2*n^2 + 2*k*n*n^2) + (4*k*n*n^2 + 4*k*n*2*k*n) + (3*k^2 * n^2 + 3*k^2 * 2*k*n) +k^4
		= n^4		+ 2*k*n^3	 + 4*k*n^3	  + 8*k^2*n^2	 +	3*k^2*n^2	+ 6*k^3*n		 + k^4
		= n^4		+ 6*k*n^3				  + 11*k^2n^2					+ 6*k^3*n		 + k^4
		
		----
		Formula 2:
		----
		  (n*k + (n+k)^2)^2
		= (n*k + n^2 + 2*k*n + k^2)^2
		= (n*k + n^2 + 2*k*n + k^2) * (n*k + n^2 + 2*k*n + k^2)
		= (n*k*n*k + n^2*n*k + 2*k*n*n*k + k^2*n*k) + (n*k*n^2 + n^2*n^2 + 2*k*n*n^2 + k^2*n^2) + (n*k*2*k*n + n^2*2*k*n + 2*k*n*2*k*n + k^2*2*k*n) + (n*k*k^2 + n^2*k^2 + 2*k*n*k^2) + (k^2*k^2)
		= (k^2*n^2 + k*n^3 + 2*k^2*n^2 + k^3*n) + (k*n^3 + n^4 + 2*k*n^3 + k^2*n^2) + (2*k^2*n^2 + 2*k*n^3 + 4*k^2*n^2 + 2*k^3*n) + (k^3*n + k^2*n^2 + 2*k^3*n + k^4)
		= n^4 + (k*n^3 + k*n^3 + 2*k*n^3 + 2*k*n^3) + (k^2n^2 + 2*k^2*n^2 + k^2*n^2 + 2*k^2*n^2 + 4*k^2*n^2 + k^2*n^2) + (k^3*n + 2*k^3*n + k^*n + 2*k^3*n) + k^4
		= n^4 + 6*k*n^3 + 11*k^2n^2 + 6*k^3*n + k^4
		
		----
		Formula 3:
		----
		 (n^2 + 3*k*n + k^2)^2
		 = (n^2 + 3*k*n + k^2) * (n^2 + 3*k*n + k^2)
		 = n^4 + 3*k*n^3 + n^2*k^2 + 3*k*n^3 + 9*k^2*n^2 + 3*k^3*n + k^2+n^2 + 3*k^3*n + k^4
		 = n^4 + (3*k*n^3 + 3*k*n^3) + (n^2*k^2+9*k^2*n^2) + (3*k^3*n + 3*k^3*n) + k^4
		 = n^4 + 6*k*n^3 + 11*k^2*n^2 + 6*k^3*n + k^4


	o	As noted: the series with difference 1, as well as the series comprised of the square roots of the diff 1, diff 2, diff3 and diff 4 series, 
		are in the Online Encyclopedia of Integer Sequences (oeis.org)
	o	When looking in squaresX.txt (X=1,2,3,...), the products formed by starting integer(n)=1, difference(k)=1 is not formed by any other 
		n:k combination. The same is true for n=2:k=2, n=3:k=3, ... n=10,k=10.  But n=11:k=11 is also formed by n=4:k=19 and n=19:k=4. The n:k 
		pairs continue 	as uniquely formed products until n=19:k=19, whose product 3,258,025 is also generated by n=41:k=1 and n=1:k=41. A quick 
		check shows that n=41:k=41 has a product also formed by n=11:k=76 and n=76:k=11. 

		Any number formed by an odd number of combinations will contain one instance of starting integer:difference being equal. Conversely: every starting 
		integer:difference of equal value (n=k) will generate a number that has an odd number of n:k combinations. The lines containing the n=k
		in the squaresX.txt files are denoted with an asterisk(*). In the files where the number in the file name approaches the number of
		files geneerated, lines will be marked with an asterisk simply because the first number in the sequence (n) is greater than the highest
		difference (k) in all calculations. Thus this sample line:
		-----------------------------------------------------------------------------------------------------------------------------------------------
		 Number(Root)           1st of four     incr     1st of four     incr     1st of four     incr     1st of four     incr   Prime Factors
		-----------------------------------------------------------------------------------------------------------------------------------------------
		*4,318,925,053,923,841(65,718,529)     5,477       1,944          -           -            -           -            -           -     409 x 160,681

		should not have an odd number of n:k pairs. However ProductOfFour.py did not do calculations for n=1944 k=5477 because the maximum k value 
		was 2000.

	o	Question: is there any way to predetermine which generated numbers have an odd number of n:k,k:n combinations greater than 1?
	
	o	for n=k the product's square root is 5 n^2.  For n-1:k+1 and n+1:k-1 the product's square root is 5*n^2 - 1.  Proof: for k=n, n-1:k+1 = n-1:n+1. Again using Formula 2,
		the square root of the product is (n-1)*(n+1) + (n-1 + n + 1)^2 = n^2 - 1 + (2*n)^2 = 5*n^2 - 1 
	
	o	for n=k, the square root of generated product (s) is 5 * n^2. Proof: By formula 2, s=n*k + (n+k)^2). For k=n this becomes n^2 + (2*n)^2 = n^2 + 4*n^2 = 5 * n^2

	o	For every n=x,k=y pair that generates a number, there exists an n=y,k=x pair that generates the same number. Proof: Using Formula 2 (n*k + (n+k)^2)^2 for the sequence 
		it is easy to see that swapping n and k does not change the result. This shows that whenever a set of n:k combinations has an odd number of entries, then one of those entries must 
		be where n=k.

