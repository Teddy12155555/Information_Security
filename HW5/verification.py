import sys
from hashlib import sha1
import math
from method import *

def verification():
	if(len(sys.argv) < 2):
		print("Format: python verification.py filename")
	elif(len(sys.argv) == 2):	
		print("Checking the signature...")
		fileName = sys.argv[1]
		file0 = open(fileName,"r")
		file1 = open("public_key.txt","r")
		file2 = open("signature.txt","r")
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
        print(int(hex,0))
        if (v == (r % q)):
            print("signature is valid")
        else:
            print("signature is invalid")

verification()