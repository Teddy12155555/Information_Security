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
                temp.append(k)

        for c in alpha:
            if c not in temp and c != 'J':
                temp.append(c)

        key_Matrix = np.reshape(temp,(5,5))
        # print(key_Matrix)

        # Encrypt 
        i = 0
        while i < len(Plaintext):
            w1 = Plaintext[i].upper()
            w2 = Plaintext[i+1].upper()
            
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
        
        a = 2
    elif sys.argv[1] == 'row':
        Cols = len(Key)
        Rows = math.ceil(len(Plaintext)/len(Key))

        # Do Matrix,but only Matrix
        Matrix = np.zeros(shape = (Rows,Cols),dtype=str)
        # print(len(Matrix))
        k = 0
        for i in range(len(Matrix)):
            for j in range(len(Key)):
                if k < len(Plaintext):
                    Matrix[i][j] = Plaintext[k].upper()
                    k = k + 1
                else:
                    break

        # Add Column number on Matrix
        Row_Trans = {}
        # Transpose Matrix
        Matrix = np.transpose(Matrix)
        k = 0
        for i in range(len(Matrix)):
            Row_Trans[Key[k]] = Matrix[i]
            k = k + 1
        
        # print(Row_Trans)
        for i in sorted(Row_Trans.keys()):
            for j in range(Rows):
                Ciphertext += Row_Trans[i][j]
    elif sys.argv[1] == 'rail_fence':
        # text = np.zeros(shape=(int(Key),int(len(Ciphertext)/int(Key))))
        a = 3
    
    print(Ciphertext)
