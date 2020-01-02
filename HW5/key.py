# -*- coding: utf-8 -*
from method import *

def keyGeneration():
	
	print("Computing key values, please wait...")
	loop = True
	while loop:
		p = 4	# make it not prime to go into the loop
		# Find Q firt then find P
		while not ( Miller_Robin_test(p) ):		# if p is not a prime, then loop umtil it is prime
			
			k = random.getrandbits(1024-160-1) + pow(2,1024-160-1)	# random (1024-160)bits number
			q = Generate_Probably_Prime(160)	# generate large prime
			p = (k * q) + 1

		L = p.bit_length()

		h = random.randint(1, p-1)
		a = mod_Square_and_Multiply(h, (p-1)//q, p)		# 𝛼 = h ^(p-1/q) (mod p)

		# make sure p is 1024 bits, p-1 and q is not relatively prime, a^q mod p == 1
		if(L == 1024 and (GCD(p-1, q)) > 1 and mod_Square_and_Multiply(a, q, p) == 1):
			loop = False
			
			d = random.randint(1, q-1)
			b = mod_Square_and_Multiply(a, d, p)
			
			file1 = open("public_key.txt","w")
			out_txt = str(p) + "\n" + str(q) + "\n" + str(a) + "\n" + str(b) + "\n"
			file1.write(out_txt)
			file1.close()

			file2 = open("private_key.txt","w")
			file2.write(str(d))
			file2.close()
			
			print("Public key stored at public_key.txt and private key stored at private_key.txt")
            
keyGeneration()