import sys
import random

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
def Miller_Robin_test(N, Times):

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

# ============== Square and Miltiply Algorithm=================
# Following steps needs to be carried out :
#
# 1. Get the binary representation of the exponent.
# 2. Bits are read from left to right (MSB first) and it should start with '1'.
# 3. Starting value = n^0, but always start with '1', so init will be n (square and mulitply)
# 4. If scanned bit is 1 then, square the value and then multiply by n
# 5. If scanneed bit is 0 then, square the value.
# 8. Repeat 4. 5. for all the bits.
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

def Decrypt():
    pass

def Encrypt():
    pass

# Get probably prime by using Miller Robin test
def Probably_Prime(bits):
    p = random.getrandbits(bits)
    while Miller_Robin_test(p, 40) == False:
        p = random.getrandbits(bits)
    print('Probably prime:', p)
    
    return p

def Init():

    bits = int(sys.argv[2])
    # Get Probably prime
    p = Probably_Prime(bits)
    q = Probably_Prime(bits)
    N = p * q
    phi_N = (p-1)*(q-1)
    

# TEST
    
    print(bits)
    print('N: ', N)
    # if Miller_Robin_test(1049,40):
    #     print('yeee')
    # print(Square_and_Multiply(5, 256))
    # print(pow(5,256))


if __name__ == "__main__":

    try:
        # Input processing
        if sys.argv[1] == 'init':   # return p,q,n,e,d
            Init()
            
        elif sys.argv[1] == '-e':   # encrypt
            Encrypt()

        elif sys.argv[1] == '-d':   # decrypt
            Decrypt()

        else:
            raise

    except:
        print('Error: Input Format')
        pass