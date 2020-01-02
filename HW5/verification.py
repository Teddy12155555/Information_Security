import sys
from hashlib import sha1
import math
from method import *

def verification(OutputName):
	if(len(sys.argv) == 3):	
		print("Checking the signature...")
		fileName = sys.argv[1]
		file0 = open(fileName,"r")
		file1 = open("public_key.txt","r")
		file2 = open(OutputName,"r")
		p = int(file1.readline().rstrip())
		q = int(file1.readline().rstrip())
		a = int(file1.readline().rstrip())
		b = int(file1.readline().rstrip())
		string = file0.read()

		r = int(file2.readline().rstrip())
		s = int(file2.readline().rstrip())
        
		SHA = sha1(string.encode('utf-8')).hexdigest()
		hex = "0x"+SHA
		w = Inverse(s,q)
		u1 = (w * int(hex,0)) % q
		u2 = (w * r) % q
		v = ((pow(a,u1,p) * pow(b,u2,p))%p) % q
		if (v == (r % q)):
			print("signature is valid!!!")
		else:
			print("signature is invalid!!!")
	else:
		print("Format: python verification.py filename")

if __name__ == '__main__':
	if(len(sys.argv) != 3):
		print("Format: python verification.py {input filename" + "} {output filename" + "}")
	elif(len(sys.argv) == 3):
		OutputName = sys.argv[2]
		verification(OutputName)