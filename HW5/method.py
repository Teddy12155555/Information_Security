import random

TEST_ROUND = 40

def Miller_Robin_test(N, Times=TEST_ROUND):

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
def Generate_Probably_Prime(bits):

    p = random.getrandbits(bits-1) + pow(2, bits-1)
    while Miller_Robin_test(p, TEST_ROUND) == False:
        p = random.getrandbits(bits-1) + pow(2,bits-1)
    
    return p


# Square_and_Multiply with mod
def mod_Square_and_Multiply(base, exp, modulus):
    result = 1
    while exp:
        exp, d = exp // 2, exp % 2    # shift right
        if d:   # last bit is '1': do square and multiply, '0': square
            result = result * base % modulus    # multiply
        base = base * base % modulus    # square
    return result

def Square_and_Multiply(base, exp):
    exponent = bin(exp)
    value = base    # Always start with '1', so initial be base

    for i in exponent[3:]:  # skip the starting '0b', and the first '1'
        if i == '1': # square and multiply
            value = value * value * base
        elif i == '0':  # square
            value = value * value
    return value

# Return the greatest common divisor of n and m.
def GCD(n,m):
    # m: mod number
    # n: beeing mod
    while  m > 0:
        temp = m
        m = n % m
        n = temp
    return n     