# -*- coding: utf-8 -*-
"""
Created on Wed Apr 01 15:35:12 2015

@author: Ray
http://en.wikipedia.org/wiki/Steganography
"""

from PIL import Image

def stringToBits(theString):
    result = []
    for aChar in theString:
        bits = bin(ord(aChar))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def bitsToString(bits):
    chars = []
    for b in range(len(bits) / 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)
    
def getPixelsFromImage(filename):
    img = Image.open(filename)
    pixels = list(img.getdata())
    width, height = img.size
    return width, height, pixels
    
def encodeMessageInPixels(message, pixels):
    new_pixels = []
    for bit in stringToBits(message):
        oldB = bin(pixels[bit][2])
        newB = (int(oldB, 2) & ~1) | bit
        newPix = (pixels[bit][0], pixels[bit][1], newB)
        new_pixels.append(newPix)  
    for i in range(len(stringToBits(message)), len(pixels)):
        new_pixels.append(pixels[i])
    return new_pixels
        
def decodeMessageInPixels(pixels):
    secMessageBits = []
    secMessage = ""
    i = 0
    while not secMessage.endswith("\0"):
        secMessageBits.append(bin(pixels[i][2])[-1:])
        if (i + 1) % 8 == 0:
            secMessage = bitsToString(secMessageBits)
        i += 1
    return secMessage

width, height, pixels = getPixelsFromImage("python.jpg")
message = "This is a test\0"

img2 = Image.new("RGB", (width, height))
img2.putdata(encodeMessageInPixels(message, pixels))
img2.save("python2.png")

width2, height2, pixels2 = getPixelsFromImage("python2.png")

print "THE SECRET MESSAGE: " + str(decodeMessageInPixels(pixels2))