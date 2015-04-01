# -*- coding: utf-8 -*-
"""
Created on Wed Apr 01 15:35:12 2015

@author: Ray
"""

from PIL import Image

def toBits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def fromBits(bits):
    chars = []
    for b in range(len(bits) / 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

img = Image.open("python.jpg")

pixels = list(img.getdata())
width, height = img.size


#pixels = [pixels[i * width:(i + 1) * width] for i in xrange(height)]

message = "This is a test"

print bin(pixels[0][0])[2:]