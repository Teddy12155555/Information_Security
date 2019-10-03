import sys
import numpy as np
import math

alpha = 'abcdefghijklmnopqrstuvwxyz'

# Meet the format
if len(sys.argv) == 4:
    Key = sys.argv[2]
    Ciphertext = sys.argv[3]
    Plaintext = ""

    if sys.argv[1] == 'caesar':
        
        for c in Ciphertext:
            if c.isalpha():
                Plaintext += alpha[(alpha.index(c.lower()) - int(Key)) % 26]
            else:
                Plaintext += c
        
    elif sys.argv[1] == 'playfair':
        Key = Key.lower()
        # Create Key Matrix j not involved
        temp = []
        for k in Key:
            if k not in temp:
                if k == 'j':
                    temp.append('i')
                else:
                    temp.append(k)

        for c in alpha:
            if c not in temp and c != 'j':
                temp.append(c)

        key_Matrix = np.reshape(temp,(5,5))
        # print(key_Matrix)

        # Decrypt 
        i = 0
        while i < len(Ciphertext):
            # Keep it even
            try:
                w1 = Ciphertext[i].lower()
                w2 = Ciphertext[i+1].lower()
            except:
                w2 = 'x'
            
            # Dealing ij
            if w1 == 'j':
                w1 = 'i'
            if w2 == 'j':
                w2 = 'i'
            
            # Find position
            row1, col1 = np.where(key_Matrix == w1)
            row2, col2 = np.where(key_Matrix == w2)
            # print(w1, ': ',int(row1), int(col1))
            # print(w2, ': ',int(row2), int(col2))

            # Same Word
            if row1 == row2 and col1 == col2:
                w2 = 'x'
                row2,col2 = np.where(key_Matrix == w2)
                # Dealing duplicate word
                i = i - 1
            
            # Numpy to int
            row1,col1,row2,col2 = int(row1),int(col1),int(row2),int(col2)

            # Same Row
            if row1 == row2:
                Plaintext += key_Matrix[row1][(col1-1)%5]
                Plaintext += key_Matrix[row2][(col2-1)%5]
            # Same Col
            elif col1 == col2:
                Plaintext += key_Matrix[(row1-1)%5][col1]
                Plaintext += key_Matrix[(row2-1)%5][col2]
            # Others
            else:
                Plaintext += key_Matrix[row1][col2]
                Plaintext += key_Matrix[row2][col1]
            i = i + 2

    elif sys.argv[1] == 'vernam':
        # Making Real Key
        Real_key = ''
        for c in Key:
            Real_key += c.lower()

        i = 0
        while i < len(Ciphertext) - len(Key):
            Real_key += chr(( (ord(Real_key[i])-ord('a')) ^ (ord(Ciphertext[i].lower())-ord('a')) ) + ord('a'))
            i = i + 1
        # print(Real_key)

        # Decrypt
        for i in range(len(Ciphertext)):
            Plaintext += chr( ((ord(Real_key[i])-ord('a')) ^ (ord(Ciphertext[i].lower())-ord('a'))) + ord('a'))

        # To Lower
        Plaintext = Plaintext.lower()

    elif sys.argv[1] == 'row':
        Cols = len(Key)
        Rows = math.ceil(len(Ciphertext)/len(Key))

        ## Create Matrix
        # Check the position of Matrix
        Matrix = np.ones(shape = (Rows,Cols),dtype=str)
        k = 0
        for i in range(Rows):
            for j in range(Cols):
                if k < len(Ciphertext):
                    Matrix[i][j] = '0'
                    k = k + 1
                else:
                    break
        
        # Transpose Matrix
        Matrix = np.transpose(Matrix)
        # Add Columns index
        Row_Trans = {}
        for i in range(len(Key)):
            Row_Trans[Key[i]] = Matrix[i]
            # Row_Trans[Key[i]] = Matrix[i].copy()

        # Fill the Row_Trans Matrix
        k = 0
        for i in range(1,Cols+1):
            for j in range(Rows):
                if Row_Trans[str(i)][j] == '0':
                    Row_Trans[str(i)][j] = Ciphertext[k].lower()
                    k = k + 1
                else:
                    break
        # print(Row_Trans)
        # print(Matrix)

        # Decrypt
        for i in range(Rows):
            for j in range(Cols):
                if Matrix[j][i] != '1':
                    Plaintext += Matrix[j][i]
                else:
                    break


    elif sys.argv[1] == 'rail_fence':
        # Cycle of fence (-2 because top and down not repeated)
        cycle = int(Key) * 2 - 2

        # print(len(Ciphertext))
        # Make Rail Matrix
        matrix = np.ones(shape=(int(Key),len(Ciphertext)),dtype=str)        
        Down = True
        row = col = 0
        for j in range(len(Ciphertext)):
            matrix[row][col] = '*'

            # Change direction
            if row == 0:
                Down = True
            elif row == (int(Key) - 1):
                Down = False

            # Make it Rail fence
            if Down:
                row = row + 1
            else:
                row = row - 1
            col = col + 1
        
        # print(matrix)

        # Stuff Ciphertext into Matrix
        count = 0
        for i in range(int(Key)):
            for j in range(len(Ciphertext)):
                if matrix[i][j] == '*':
                    matrix[i][j] = Ciphertext[count]
                    count = count + 1
        # print(matrix)

        # Get Ciphertext by using Rail Matrix
        row = col = 0
        Down = True
        for i in range(len(Ciphertext)):
            Plaintext += matrix[row][col]
            if Down:
                row = row + 1
            else:
                row = row - 1
            
            if row == 0:
                Down = True
            elif row == (int(Key) - 1):
                Down = False
            col = col + 1
    print(Plaintext)