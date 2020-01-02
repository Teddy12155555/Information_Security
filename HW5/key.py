from miller import *
from fractions import gcd

def loopIsPrime(number):
	#looping to reduce probability of rabin miller false +
	isNumberPrime = True
	for i in range(0,20):
		isNumberPrime*=isPrime(number)
		if(isNumberPrime == False):
			return isNumberPrime
	return isNumberPrime	
def modexp( base, exp, modulus ):
        return pow(base, exp, modulus)
def SquareAndMultiply(x,c,n):
	z=1
	#getting value of l by converting c into binary representation and getting its length
	c="{0:b}".format(c)[::-1] #reversing the binary string
	
	l=len(c)
	for i in range(l-1,-1,-1):
		z=pow(z,2)
		z=z%n
		if(c[i] == '1'):
			z=(z*x)%n
	return z	

def keyGeneration():
	
	print("Computing key values, please wait...")
	loop = True
	while loop:
		k = random.getrandbits(1024-160)
		q = generateLargePrime(160)
		p = (k*q)+1
		while not (isPrime(p)):
			k = random.getrandbits(1024-160)
			q=generateLargePrime(160)
			p=(k*q)+1
		L = p.bit_length()
		"""
		g=t^(p-1)/q  %  p
		if(g^q  % p = 1) we found g
		"""

		t = random.randint(1,p-1)
		a = SquareAndMultiply(t, (p-1)//q, p)
		
		if(L == 1024 and (gcd(p-1,q)) > 1 and SquareAndMultiply(a,q,p) == 1):
			loop = False
			#print((p-1)%q)
			
			d = random.randint(2,q-1)
			b = SquareAndMultiply(a,d,p)
			#print("p = ",p)
			#print("q = ",q)
			#print("g = ",g)
			#print("h = ",h)
			#print("a = ",a)
			
			file1 = open("key.txt","w")
			file1.write(str(p))
			file1.write("\n")
			file1.write(str(q))
			file1.write("\n")
			file1.write(str(a))
			file1.write("\n")
			file1.write(str(b))
			file1.close()
			file2 = open("secretkey.txt","w")
			file2.write(str(d))
			file2.close()
			print("Verification key stored at key.txt and secret key stored at secretkey.txt")
            

keyGeneration()