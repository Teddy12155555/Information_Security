import sys
from hashlib import sha1
import math
from method import *

def verification(SignFileName):
	if(len(sys.argv) == 3):	
		print("Checking the signature...")
		fileName = sys.argv[1]
		# Open text file, public key and Signature file
		file0 = open(fileName,"r")
		file1 = open("public_key.txt","r")
		file2 = open(SignFileName,"r")

		# Read the public key (p,q,a,b)
		p = int(file1.readline().rstrip())
		q = int(file1.readline().rstrip())
		a = int(file1.readline().rstrip())
		b = int(file1.readline().rstrip())
		# Read text file
		string = file0.read()

		# Read Signature file
		r = int(file2.readline().rstrip())
		s = int(file2.readline().rstrip())
        
		# Do the verifcation
		SHA = sha1(string.encode('utf-8')).hexdigest()	# SHA1(string)
		hex = "0x"+SHA
		w = Inverse(s,q)	# w = S^-1 mod q
		u1 = (w * int(hex,0)) % q	# u1 = (w * SHA1(string)) mod q
		u2 = (w * r) % q	# u2 = (w * r) mod q
		v = ((pow(a,u1,p) * pow(b,u2,p))%p) % q		# v = (a^u1 * b^u2 mod p) mod q

		if (v == (r % q)):	# V = R mod q -> signature is valid
			print("signature is valid!!!")
		else:
			print("signature is invalid!!!")
	else:
		print("Format: python verification.py filename")

if __name__ == '__main__':
	if(len(sys.argv) != 3):
		print("Format: python verification.py {input filename" + "} {output filename" + "}")
	elif(len(sys.argv) == 3):
		SignFileName = sys.argv[2]
		try:
			verification(SignFileName)
		except:
			print("File Name Error")