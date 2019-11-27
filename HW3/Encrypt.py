#!/usr/bin/python3
from Crypto.Cipher import AES
from Crypto import Random
from PIL import Image
import numpy as np
import io

# ECB Mode
def ECB_Mode(key, plaintext):

    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = bytes()
    
    for i in range(0,len(plaintext),AES.block_size):
        # take one block size
        temp = plaintext[i:i+AES.block_size]
        ciphertext += cipher.encrypt(temp)
        # print(temp, end=' ')
    
    print(ciphertext)
    return ciphertext

# CBC Mode
def CBC_Mode():
    pass

# Cool Mode
def Cool_Mode():
    pass

# JPG to PPM
def JPG_to_PPM():
    ppmPic = "./linux.ppm"
    im = Image.open("./linux-penguin.jpg")
    im.save(ppmPic)
    return im

# PPM to Byte array
def PPM_to_ByteArr():
    imgByteArr = io.BytesIO()
    im.save(imgByteArr, format='PPM')
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

if __name__ == '__main__':

    # Read ppm
    im = JPG_to_PPM()   # JPG to PPM
    imgByteArr = PPM_to_ByteArr()   # PPM to Byte array
    
    Header = imgByteArr[0:15]   # 3 header information
    Plaintext = imgByteArr[15:] # plaintest not include header
    Key = b'Sixteen byte key'   # Key

    print(imgByteArr[0:15])
    print(Plaintext[:19])

    # Call Mode
    Ciphertext = ECB_Mode(Key,Plaintext)

    # Cipher to image
    Ciphertext = Header + Ciphertext
    img = Image.open(io.BytesIO(Ciphertext))
    img.save("./after.ppm")

    # ECB
    print(AES.block_size)
    IV = Random.new().read(AES.block_size)
    key = b'Sixteen byte key'
    cipher = AES.new(key, AES.MODE_ECB)
    msg = IV + cipher.encrypt(b'Attack at dawn..')
    print(msg)