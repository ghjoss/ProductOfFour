import sys
if len(sys.argv) == 2:
	maxk = int(sys.argv[1]) + 1
	maxn = int(sys.argv[2]) + 1
else:
	maxk = 11
	maxn = 11	
f=open("test.txt","w")
for k in range(1,maxk):
	for n in range(1,maxn):
		fkn1 = n**4 + 6*k*n**3 + 11*k**2*n**2 +6*k**3*n + k**4
		fkn2 = ((n*k) + (n+k)**2)**2
		print("n(%3d):k(%3d) ==> %8d / %8d" % (n,k,fkn1,fkn2),file=f)
