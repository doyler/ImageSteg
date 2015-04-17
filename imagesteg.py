# -*- coding: utf-8 -*-
"""
Created on Wed Apr 01 15:35:12 2015

@author: Ray
http://en.wikipedia.org/wiki/Steganography
"""

import base64
import hashlib

from Crypto import Random
from Crypto.Cipher import AES
from PIL import Image

def stringToBits(theString):
    result = []
    for char in theString:
        bits = bin(ord(char))[2:]
        bits = "%08d" % int(bits)
        result.extend([int(b) for b in bits])
    return result

def bitsToString(bits):
    chars = []
    for b in range(len(bits) / 8):
        byte = bits[b*8:(b+1)*8]
        #Clean this up a bit for usability and readability
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)
    
def getPixelsFromImage(filename):
    img = Image.open(filename)
    pixels = list(img.getdata())
    width, height = img.size
    return width, height, pixels
    
def encodeMessageInPixels(message, pixels, location):
    new_pixels = []
    newPix = ()
    for bit in stringToBits(message):
        oldB = bin(pixels[bit][2])
        newB = (int(oldB, 2) & ~1) | bit
        #Consider a slightly different way to determine where to put the info?
        if location == "R":
            new_pixels.append((newB, pixels[bit][1], pixels[bit][2]))
        elif location == "G":
            new_pixels.append((pixels[bit][0], newB, pixels[bit][2]))
        elif location == "B":
            new_pixels.append((pixels[bit][0], pixels[bit][1], newB))
        elif location == "ALL":
            newPix += (newB,)
            if len(newPix) % 3 == 0:
                new_pixels.append(newPix)
                newPix = ()
        else:
            raise ValueError("{loc} is an improper value for location; "
                            "use 'R', 'G', 'B', "
                            "or 'ALL' instead.""".format(loc=repr(location)))
    for i in range (0, 3):
        oldB = bin(pixels[bit][i])
        newB = (int(oldB, 2) & ~1) | 0
        newPix += (newB,)
    new_pixels.append(newPix)
    for i in range(len(new_pixels), len(pixels)):
        new_pixels.append(pixels[i])
    return new_pixels
        
def decodeMessageInPixels(pixels, location):
    secMessageBits = []
    secMessage = ""
    i = 0
    while not secMessage.endswith("\0"):
        if location == "R":
            secMessageBits.append(bin(pixels[i][0])[-1:])
        elif location == "G":
            secMessageBits.append(bin(pixels[i][1])[-1:])
        elif location == "B":
            secMessageBits.append(bin(pixels[i][2])[-1:])
        elif location == "ALL":
            secMessageBits.append(bin(pixels[i / 3][i % 3])[-1:])
        else:
            raise ValueError("{loc} is an improper value for location; "
                            "use 'R', 'G', 'B', "
                            "or 'ALL' instead.""".format(loc=repr(location)))      
        if (i + 1) % 8 == 0:
            """
            This ends up calling the bitsToString method for each character,
            this is unnecessary and the checking or calling should be done
            slightly differently.
            """
            secMessage = bitsToString(secMessageBits)
        i += 1
    return secMessage.rstrip("\0")
    
def aesEncrypt(message, key):
    iv = Random.new().read(AES.block_size)
    keySum = hashlib.md5(key).hexdigest()
    cipher = AES.new(keySum, AES.MODE_CFB, iv)
    return base64.b64encode(iv + cipher.encrypt(message))

def aesDecrypt(cipherText, key):
    cipherText = base64.b64decode(cipherText) 
    iv = cipherText[:16]
    keySum = hashlib.md5(key).hexdigest()
    cipher = AES.new(keySum, AES.MODE_CFB, iv)
    return cipher.decrypt(cipherText[16:])

def main():
    width, height, pixels = getPixelsFromImage("python.jpg")
    message = "This is a test\0"
    messageEnc = aesEncrypt(message, "secretkey")
    
    img2 = Image.new("RGB", (width, height))
    img2.putdata(encodeMessageInPixels(messageEnc, pixels, "ALL"))
    img2.save("python2.png")

    width2, height2, pixels2 = getPixelsFromImage("python2.png")

    outMessage = decodeMessageInPixels(pixels2, "ALL")
    messageDec = aesDecrypt(outMessage, "secretkey")
    print "THE SECRET MESSAGE: " + messageDec
    
if __name__ == "__main__":
    main()