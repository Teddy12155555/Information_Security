#!/usr/bin/python3
from Crypto.Cipher import AES
from Crypto import Random
from PIL import Image

# JPG to PPM
ppmPic = "./linux.ppm"
im = Image.open("./linux-penguin.jpg")
im.save(ppmPic)

# ECB
IV = Random.new().read(AES.block_size)
key = b'Sixteen byte key'
cipher = AES.new(key, AES.MODE_ECB)
msg = IV + cipher.encrypt(b'Attack at dawn')

