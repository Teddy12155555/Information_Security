import sys
from method import *
from hashlib import sha1
import random

def sign(OutputName):
	
	if(len(sys.argv) == 3):	
		print("Signing the file...")
		fileName = sys.argv[1]
		file0 = open(fileName,"r")
		file1 = open("public_key.txt","r")
		file2 = open("private_key.txt","r")
		p = int(file1.readline().rstrip())
		q = int(file1.readline().rstrip())
		a = int(file1.readline().rstrip())
		b = int(file1.readline().rstrip())
		d = int(file2.readline().rstrip())
		string = file0.read()

		Ke = random.randint(1,q)
		KeInv = Inverse(Ke,q)
		SHA = sha1(string.encode('utf-8')).hexdigest()
		hex = "0x"+SHA

		r = mod_Square_and_Multiply(a,Ke,p)
		r = r % q
		s = ((int(hex,0) + (d * r)) * KeInv) % q
		SignFile = open(OutputName,"w")
		SignFile.write(str(r)+"\n"+str(s)+"\n")
		SignFile.close()
		print ('sign complete')
	else:
		print("Format: python sign.py filename")


if __name__ == '__main__':
	if(len(sys.argv) != 3):
		print("Format: python sign.py {input filename" + "} {output filename" + "}")
	elif(len(sys.argv) == 3):
		OutputName = sys.argv[2]
		sign(OutputName)
