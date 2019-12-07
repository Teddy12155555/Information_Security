import sys
import random
import numpy as np
import os

test_round = 40
FOLDER = './MsgAndKey/'
PRIVATE_KEY = FOLDER + 'private_key.txt'
PUBLIC_KEY = FOLDER + 'public_key.txt'
ENC_MESSAGE = FOLDER + 'enc_message.txt'
DEC_MESSAGE = FOLDER + 'dec_message.txt'

# ================ Miller Robin Test ========================
# It returns false if n is composite 
# It returns True if n is probably prime.  
#
# If n is a prime and n > 2 then:
# n-1 is an even and such that d*2^s = n-1 for d is odd and s,d are positive int
# a in range[2, n-1], 0 <= r <= s-1
# 1. If a^d mod n != 1 and 
# 2. a^((2^r)*d) mod n != n-1 
# Then n is not prime
# ===========================================================
def Miller_Robin_test(N, Times=test_round):

    if N == 2 or N==3:
        return True

    if N % 2 == 0: # even number is not prime
        return False
    
    d = N - 1
    s = 0
    while d % 2 == 0:
        d = d // 2  # Int division, will be d = (n-1)/2^s in final
        s = s + 1

    for _ in range(Times):
        a = random.randrange(2, N-1)
        x = pow(a, d, N)    # x = a^d mod N

        if x == 1 or x == N-1: continue # probably prime

        for r in range(1, s): # r=0, been check by previous if
            x = pow(x, 2, N)    # x = a^((2^r)*d) mod N
            if x == N-1: break  # probably prime
            if x == 1: return False # composite, because won't match x == N-1
        else:
            return False    # composite
        
    return True  # probably prime

# Random number with bits to get probably prime by using Miller Robin test
def Probably_Prime(bits):

    p = random.getrandbits(bits-1) + Square_and_Multiply(2, bits-1)
    while Miller_Robin_test(p, test_round) == False:
        p = random.getrandbits(bits-1) + Square_and_Multiply(2,bits-1)
    
    return p

# ============== Square and Miltiply Algorithm=================
# Efficient way to do base ^ exp
# 1. Get the binary representation of the exponent.
# 2. Bits are read from left to right (MSB first) and it should start with '1'.
# 3. Starting value = n^0, but always start with '1', so init will be n (square and mulitply)
# 4. If scanned bit is 1 then, square the value and then multiply by n
# 5. If scanneed bit is 0 then, square the value.
# ============================================================
def Square_and_Multiply(base, exp):
    exponent = bin(exp)
    value = base    # Always start with '1', so initial be base

    for i in exponent[3:]:  # skip the starting '0b', and the first '1'
        if i == '1': # square and multiply
            value = value * value * base
        elif i == '0':  # square
            value = value * value
    return value

# Square_and_Multiply with mod
def SM_mod(base, exp, modulus):
    result = 1
    while exp:
        exp, d = exp // 2, exp % 2    # shift right
        if d:   # last bit is '1': do square and multiply, '0': square
            result = result * base % modulus    # multiply
        base = base * base % modulus    # square
    return result

# ================= modPow====================
# Equals base ^ exp % modulus. 
# Only call in Chinese_Remainder(), so modulus will always
# be prime. And exp can be reduced using Euler theorem.
# Uses Euler theorem and Square_and_Multiply.
#=============================================
def modPow(base, exp, modulus):
    # do Euler
    exp = exp % (modulus-1) # exp mod phi(modulu)
    return SM_mod(base,exp,modulus)

# ================= Chinese_Remainder ==============
# Used when Decrypt. base ^ exp % M is too big to compute.
# result = Sum (ai * Mi * yi) % M
# mi: pairwise relatively prime
# Mi: M // mi
# yi: multi inverse of Mi (mod mi)
# ai: x mod mi
# ==================================================
def Chinese_Remainder(base, exp, M, m):
    # m: prime number , M: m1*m2*...*mn
    result = 0

    for i in range(len(m)):
        mi = m[i]
        ai = modPow(base, exp, mi)  # base ^ exp = x
        
        Mi = M // mi
        r, yi, _ = Extended_GCD(Mi, mi)
        yi = yi % mi

        result = (result + ai * Mi * yi)%M
    
    return result % M

# Return (g, x, y) such that a*x + b*y = g = gcd(a, b)
def Extended_GCD(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = Extended_GCD(b % a, a)
        return (g, y - (b // a) * x, x)

# Return the greatest common divisor of n and m.
def GCD(n,m):
    # m: mod number
    # n: beeing mod
    while  m > 0:
        temp = m
        m = n % m
        n = temp
    return n         

# Algorithm to turn text into blocks, used in Encrypt
def textToBlocks(infileName, N):
    
    block_size = (len(bin(N)[2:]) // 7)-1  # make sure message bits is less then N bits

    # Read Message file
    infile = open(infileName, 'r')
    fileString = ""
    line = infile.readline()
    while line != "":
        fileString += line
        line = infile.readline()
    
    blockList = []
    while len(fileString) != 0:
        s = ""
        s = fileString[0:block_size]    # takes a block size a time
        fileString = fileString[block_size:]    # shift the filestring

        block = 0
        for ch in s:
            block = block * 128 + ord(ch)   # 固定每個字為7個bit，陸續接在尾巴

        blockList.append(str(block)+"\n")   # A block is a row

    blockList[-1] = blockList[-1][:-1]  # '\n' not needed in last message block

    # Output file
    outfile = open(ENC_MESSAGE, 'w')
    for item in blockList:
        outfile.write("%s" % item)
    outfile.close()

# Algorithm to turn blocks into text, used in Decrypt
def blocksToText(infile):
    # Open file
    intList = open(infile).readlines()

    s = ""
    for i in intList:
        block = ""
        while int(i) > 0:
            ch = chr(int(i) % 128)    # take the last block
            block = ch + block  # from back to head
            i = int(i)//128     # delete the last block
        s += block
    
    # Output file
    outfile = open(infile, 'w')
    outfile.write(s)
    outfile.close()
    return s

# Generate public/private key file
# private mode =1, when generate private key file
def gen_keyfile(privateMode,n, key,filename, p=0, q=0):
    outfile1 = open(filename, 'w')
    outfile1.write("N:"+str(n)+"\nK:"+str(key))
    if privateMode: # generate private key file
        outfile1.write("\np:"+str(p)+"\nq:"+str(q))
    
# Unpack the keyfile and get the key
def take_key(filename):
    keylist = open(filename).readlines()
    n = int((keylist[0])[2:])
    k = int((keylist[1])[2:])
    if len(keylist) == 2:
        return n,k
    else:   # private key got p q as well
        p = int((keylist[2])[2:])
        q = int((keylist[3])[2:])
        return n,k,p,q

# cmd: python3 RSA.py -d
def Decrypt():
    ## Decrypt the file we Encrypt previous
    n,d,p,q = take_key(PRIVATE_KEY)

    dec = []
    enc_msg = open(ENC_MESSAGE).readlines() # Read the file we Encrypt previous
    for C in enc_msg:
        M = Chinese_Remainder(int(C),d,n,(p,q)) # Decrypt
        # M = pow(int(C),d,n)
        # M = modPow(int(C),d,n)
        dec.append(M)
    
    # Output file
    temp = open(DEC_MESSAGE, 'w')
    for i in dec:
        temp.write("%s\n" % str(i))
    temp.close()
    print(blocksToText(DEC_MESSAGE))

# cmd: python3 RSA.py -e input_file
def Encrypt():
    # Take message file and public key
    message_file = sys.argv[2]
    n,e = take_key(PUBLIC_KEY)
    
    # Encrypt
    textToBlocks(message_file, n)   # Make message to block
    txtblk = open(ENC_MESSAGE).readlines()  # Read output file made in testToBlocks()
    enc = []
    for M in txtblk:
        C = pow(int(M),e,n) # Encrypt
        enc.append(C)

    # Output file
    outfile = open(ENC_MESSAGE,'w')
    for i in enc:
        print(i)
        outfile.write("%s\n" % str(i))
    outfile.close()

def Init():

    bits = int(sys.argv[2])
    # Get Probably prime
    p = Probably_Prime(bits)
    q = Probably_Prime(bits)

    # Get N and phi N
    N = p * q
    phi_N = (p-1)*(q-1)
    
    # Get e
    while True:
        e = random.randrange(2, bits*100)
        if GCD(e, phi_N) == 1:
            break

    # Get d
    r,d,y = Extended_GCD(e, phi_N)
    d = d % phi_N
    
    print('private key(\nN:\n{},\nd:\n{})\n\npublic key(\nN:\n{},\ne:\n{})\n'.format(N, d, N, e))
    print('N: \n{}'.format(N))
    print('p: \n{}\nq: \n{}'.format(p,q))

    # Generate public key file
    gen_keyfile(0, N, e, PUBLIC_KEY)
    # Generate private key file
    gen_keyfile(1, N, d, PRIVATE_KEY, p, q)

if __name__ == "__main__":

    # Create folders to save key files
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)
    
    try:
        # Input processing
        if sys.argv[1] == '-init':   # return p,q,n,e,d
            Init()
            
        elif sys.argv[1] == '-e':   # encrypt
            Encrypt()

        elif sys.argv[1] == '-d':   # decrypt
            Decrypt()
        else:
            raise
    except:
        print('<Error>: Input Format')
        print('[Initial]: python3 RSA.py -init {bits}')
        print('[Encrypt]: python3 RSA.py -e {input_file}')
        print('[Decrypt]: python3 RSA.py -d')
        print('<Info>: Initial -> Encrypt -> Decrypt')