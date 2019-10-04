import sys
import numpy as np 
import math

alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Meet the format
if len(sys.argv) == 4:
    Key = sys.argv[2]
    Plaintext = sys.argv[3]
    Ciphertext = ""

    if sys.argv[1] == 'caesar':
        
        for c in Plaintext:
            if c.isalpha():
                Ciphertext += alpha[(alpha.index(c.upper()) + int(Key)) % 26]
            else:
                Ciphertext += c
        
    elif sys.argv[1] == 'playfair':
        Key = Key.upper()
        # Create Key Matrix j not involved
        temp = []
        for k in Key:
            if k not in temp:
                if k == 'J':
                    temp.append('I')
                else:
                    temp.append(k)

        for c in alpha:
            if c not in temp and c != 'J':
                temp.append(c)

        key_Matrix = np.reshape(temp,(5,5))
        # print(key_Matrix)

        # Encrypt 
        i = 0
        while i < len(Plaintext):
            # Keep it even
            try:
                w1 = Plaintext[i].upper()
                w2 = Plaintext[i+1].upper()
            except:
                w2 = 'X'
            
            # Dealing ij
            if w1 == 'J':
                w1 = 'I'
            if w2 == 'J':
                w2 = 'I'

            # Find position
            row1, col1 = np.where(key_Matrix == w1)
            row2, col2 = np.where(key_Matrix == w2)
            # print(w1, ': ',int(row1), int(col1))
            # print(w2, ': ',int(row2), int(col2))

            # Same Word
            if row1 == row2 and col1 == col2:
                w2 = 'X'
                row2,col2 = np.where(key_Matrix == w2)
                # Dealing duplicate word
                i = i - 1
            
            # Numpy to int
            row1,col1,row2,col2 = int(row1),int(col1),int(row2),int(col2)

            # Same Row
            if row1 == row2:
                Ciphertext += key_Matrix[row1][(col1+1)%5]
                Ciphertext += key_Matrix[row2][(col2+1)%5]
            # Same Col
            elif col1 == col2:                
                Ciphertext += key_Matrix[(row1+1)%5][col1]
                Ciphertext += key_Matrix[(row2+1)%5][col2]
            # Others
            else:
                Ciphertext += key_Matrix[row1][col2]
                Ciphertext += key_Matrix[row2][col1]
            i = i + 2

    elif sys.argv[1] == 'vernam':
        newkey = Key.lower()+Plaintext
        newkey.upper()
        for i in range(len(Plaintext)):
            key_int = ord(newkey[i]) - 97
            txt_int = ord(Plaintext[i]) - 97
            Ciphertext += chr((key_int ^ txt_int)+65)
    elif sys.argv[1] == 'row':
        lt = [None]*len(Key)
        dic = {}
        for i in range(len(Key)):
            lt[i] = Key[i]
            dic[Key[i]] = ""
        lt.sort()
        for i in range(len(Plaintext)):
            dic[Key[i%len(Key)]] += Plaintext[i].upper()
        for i in range(len(lt)):
            Ciphertext += dic[lt[i]]
    elif sys.argv[1] == 'rail_fence':
        fence = int(Key)
        j=0
        flag = True
        dic={}
        for i in range(fence):
            dic[i] = ''
        for i in range(len(Plaintext)):
            dic[j] += Plaintext[i].upper()
            if flag:
                j+=1
            else:
                j-=1
            if j == fence-1:
                flag = False
            if j == 0:
                flag = True
        for i in dic.values():
            Ciphertext += i
    
    print(Ciphertext)
