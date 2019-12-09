import sys
import numpy as np
import os
import math
import random
import re

def ExtendedEuclidean(a,b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  b, y0, x0

def SquareAndMultiply(x, k, p=None):
    b = bin(k).lstrip('0b')
    r = 1
    for i in b:
        r = r**2
        if i == '1':
            r = r * x
        if p:
            r %= p
    return r

def MillerRabinTest(p, s=5):
    if p == 2: 
        return True
    if not (p & 1): 
        return False
    p1 = p - 1
    u = 0
    r = p1  
    while r % 2 == 0:
        r >>= 1
        u += 1

    def witness(a):
        z = SquareAndMultiply(a, r, p)
        if z == 1:
            return False
        for i in range(u):
            z = SquareAndMultiply(a, 2**i * r, p)
            if z == p1:
                return False
        return True
    for j in range(s):
        a = random.randrange(2, p-2)
        if witness(a):
            return False
    return True

def GenerateKeys(p,q):
    Phi = (p - 1) * (q - 1)
    while True:
        e = random.randrange(1,Phi - 1)
        if math.gcd(e,Phi) == 1:
            gcd,s,t = ExtendedEuclidean(Phi,e)
            if gcd == (s * Phi + t * e):
                d = t % Phi
                break
    return (e,d)

def RSAEncrypt(plaintext,e,n):
    temp = ''
    for i in plaintext:
        temp += ( str( ord(i)+100 ) )
    ciphertext = SquareAndMultiply(int(temp),e,n)
    
    return str(ciphertext)

def RSADecrypt(ciphertext,d,n):
    plaintext = ''
    temp = str(SquareAndMultiply(int(ciphertext),d,n))
    
    for i in range(0,len(temp),3):
        plaintext += chr(int(temp[i:i+3]) - 100)

    return plaintext

def RSADecryptCRT(ciphertext,d,n,p,q):
    plaintext = ''

def main(): 
    if len(sys.argv) <= 1:
        print("Error")
        print("Please given some parameter !")
        return
    else:
        if (sys.argv[1] == "init") and (len(sys.argv) == 3):
            bits = sys.argv[2]
            print("init RSA with "+bits+" bits...")
            # Do init RSA
            number = GeneratePrimes(int(bits))
            p = number[0]
            print("p : " + str(p))
            q = number[1]
            print("q : " + str(q))
            n = p * q
            print("n : " + str(n))
            e,d = GenerateKeys(p,q)
            print("e : " + str(e))
            print("d : " + str(d))
            print("---------------------------------------")
            print('Public Key (e, n) = {}'.format((e,n)))
            print('Private Key (d) = {}'.format(d))
            print("---------------------------------------")
            return
            
        elif sys.argv[1] == "-e" and len(sys.argv) == 5:
            plaintext = sys.argv[2]
            Encrypt_e = int(sys.argv[3])
            Encrypt_n = int(sys.argv[4])
            ciphertext = RSAEncrypt(plaintext,Encrypt_e,Encrypt_n)
            print("CipherText : " + ciphertext)
            return
        

        elif sys.argv[1] == "-d" and len(sys.argv) == 5:
            ciphertext = sys.argv[2]
            Decrypt_d = int(sys.argv[3])
            Decrypt_n = int(sys.argv[4])
            plaintext = RSADecrypt(ciphertext,Decrypt_d,Decrypt_n)
            print("PlainText : " + plaintext) 
            return
            
        elif sys.argv[1] == "-d" and len(sys.argv) == 7:
            ciphertext = sys.argv[2]
            Decrypt_d = int(sys.argv[3])
            Decrypt_n = int(sys.argv[4])
            Decrypt_p = int(sys.argv[5])
            Decrypt_q = int(sys.argv[6])
            plaintext = RSADecrypt(ciphertext,Decrypt_d,Decrypt_n)
            print("PlainText : " + plaintext)

        elif sys.argv[1] == "debug":
            bitlength = sys.argv[2]
            x = random.getrandbits(int(bitlength))
            
            print('Plaintext x={}'.format(x))    

        else:
            print("Parameters Error !")

def GeneratePrimes(bits):
    PrimeCount = 2
    #temp = random.getrandbits(bits)
    primes = []
    while PrimeCount > 0:
        temp = bin(random.getrandbits(bits - 2))
        temp = temp[0:2] + '1' + temp[2:] + '1'
        if MillerRabinTest(int(temp,2), s=4):
            primes.append(int(temp,2))
            PrimeCount -= 1
    
    return primes

if __name__ == '__main__':
    # main func
    main()