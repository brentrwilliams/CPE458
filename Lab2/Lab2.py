
from Crypto.Cipher import AES
from CryptoUtils import base64ToAscii, asciiToBase64, hexToAscii, asciiToHex, xor, base64ToHex, hexToBase64
import struct
import crypto

class InvalidTextOrKeyLengthException(Exception):
   def __init__(self, details):
      self.details = details
   def __str__(self):
      return str(self.details)

# PKCS#7 padding
def pad(keyLength, plaintext):
   paddedtext = plaintext
   padNum = keyLength - (len(plaintext) % keyLength)

   paddedtext += chr(padNum) * padNum 
   return paddedtext


# PKCS#7 unpadding
def unpad(keyLength, plaintext):
   if len(plaintext) % keyLength != 0:
      raise InvalidTextOrKeyLengthException('The length of the text is not a multiple of the key length')

   lastChar = plaintext[-1]
   padNum = ord(lastChar)

   if padNum > keyLength:
      raise InvalidTextOrKeyLengthException('Padding number greater than key length')

   padding = plaintext[-padNum:]
   expectedPadding = lastChar * padNum

   if padding != expectedPadding:
      raise InvalidTextOrKeyLengthException('Unexpected padding: ' + padding + '\nExpected: ' +expectedPadding)

   return plaintext[:-padNum]


def ecb_encrypt(key, plaintext):
   padded_plaintext = pad(len(key),  plaintext)
   cipher = AES.new(key)
   ciphertext = cipher.encrypt(padded_plaintext)
   return asciiToBase64(ciphertext)


def ecb_decrypt(key, ciphertext):
   ascii_ciphertext = base64ToAscii(ciphertext)
   cipher = AES.new(key)
   padded_plaintext = cipher.decrypt(ascii_ciphertext)
   return unpad(len(key), padded_plaintext)

def cbc_encrypt(plaintext, key, iv):
   #padded_plaintext = pad(len(key), plaintext)
   padded_plaintext = crypto.ansix923_pad(plaintext,len(key))
   cipher = AES.new(key)
   blockSize = len(key)

   #firstBlock = padded_plaintext[0:blockSize]
   totalCtext = ""
   #ctext = cipher.encrypt(xor(firstBlock, iv))
   ctext = iv
   totalCtext += ctext


   for i in xrange(0, len(padded_plaintext), blockSize):
      block = padded_plaintext[i:i+blockSize]
      ctext = cipher.encrypt(xor(block, ctext))
      totalCtext += ctext

   print len(totalCtext)

   return asciiToBase64(totalCtext)

def cbc_decrypt(ciphertext, key, iv):
   ascii_ciphertext = base64ToAscii(ciphertext)
   cipher = AES.new(key)

   blockSize = len(key)

   ctext = ascii_ciphertext[0:blockSize]
   totalPtext = ""
   #ptext = xor(cipher.decrypt(ctext), iv)
   #totalPtext += ptext

   print blockSize
   print len(ascii_ciphertext)

   for i in xrange(blockSize, len(ascii_ciphertext), blockSize):
      block = ascii_ciphertext[i:i+blockSize]
      print len(block)
      ptext = xor(cipher.decrypt(block), ctext)
      totalPtext += ptext
      ctext = block

   #return unpad(len(key), totalPtext)
   #return crypto.ansix923_strip(totalPtext,len(key))
   return totalPtext

def read_ciphertext_file(filename):
   ciphertext = ''
   with open(filename) as f:
      for line in f:
         ciphertext += line.strip()
   return ciphertext


def taskIIA():
   print 'TaskIIA: \n'
   filename = 'Lab2.TaskII.A.txt'
   ciphertext = ''
   with open(filename) as f:
      for line in f:
         ciphertext += line.strip()
   
   plaintext = ecb_decrypt('CALIFORNIA LOVE!', ciphertext)
   print plaintext

def analyze_pixel_frequency(pixel_data, bytes_per_pixel):
   colors = {}

   for i in range(0, len(pixel_data), bytes_per_pixel):
      color = pixel_data[i:i+bytes_per_pixel]
      
      if color in colors:
         colors[color] = colors[color] + 1
      else:
         colors[color] = 1

   count = 0
   
   for key in colors.keys():
      if colors[key] > 2:
         count += 1

   return count

def taskIIB():
   print '\nTaskIIB: \n'
   filename = 'Lab2.TaskII.B.txt'
   with open(filename) as f:
      count = 0
      for line in f:
         img = hexToAscii(line.strip())
         if count == 1:
            file_size = struct.unpack( "h",img[2:4] )[0]
            pixel_data_offset = struct.unpack( "i",img[10:14] )[0]
            width = struct.unpack( "i",img[18:22] )[0]
            height = struct.unpack( "i",img[22:26] )[0]
            bits_per_pixel = struct.unpack( "h",img[28:30] )[0]
            pad_number = len(img)-file_size

            print 'File size from header (in bytes): ' + str(file_size)
            print 'Encrypted file size (in bytes): ' + str(len(img))
            print 'Pixel data offset (in bytes): ' + str(pixel_data_offset)
            print 'Bits per pixel: ' + str(bits_per_pixel)
            print 'Each component in RGBA is: 1 byte'
            print 'Width: ' + str(width)
            print 'Height: ' + str(height)
            print 'ECB padded images last bytes: '
            print (str(pad_number) * pad_number)
            print ''

         f = open('images/image' + str(count) + '.bmp', 'w')
         f.write(img)
         f.close()
         count += 1

   print 'Analyzing pixel frequency...'
   pixel_frequencies = [0] * count

   with open(filename) as f:
      index = 0
      for line in f:
         img = hexToAscii(line.strip())
         file_size = struct.unpack( "h",img[2:4] )[0]
         pixel_data_offset = struct.unpack( "i",img[10:14] )[0]
         bits_per_pixel = struct.unpack( "h",img[28:30] )[0]
         bytes_per_pixel = bits_per_pixel / 8
         pixel_data = img[pixel_data_offset:file_size]

         pixel_frequencies[index] = analyze_pixel_frequency(pixel_data, bytes_per_pixel)

         index += 1

   # Get the index with the highest number of repeating pixels
   max_val = pixel_frequencies[0]
   max_index = 0
   for i in range(1, count):
      if pixel_frequencies[i] > max_val:
         max_val = pixel_frequencies[i]
         max_index = i

   print 'ECB Padded image: ' + str(max_index)


def taskIIC():
   print '\nTaskIIC: \n'
   username = 'mmmmmmadmin'
   cookie_hex = '20963c162c912a4479dd5db13f0138a52e2e0bdcc1fd7d5351ed4ebca5948dfe1ad334cefbae0d0953dd4462eef91e81'
   cookie_ascii = hexToAscii(cookie_hex)
   admin_hex = asciiToHex( cookie_ascii[11:16] )
   block3 = asciiToHex( cookie_ascii[32:] )


   print 'username: ' + username
   print 'password: ' + username
   print 'cookie in hex: ' + cookie_hex
   print 'len(cookie_hex): ' + str(len(cookie_hex))

   print 'Cookie Block 1 (in hex):\t' + asciiToHex( cookie_ascii[:16] )
   print 'Cookie Block 1 (in ascii):\t u s e r = m m m m m m a d m i n'
   print 'admin (at the end of the block in hex):\t\t      ' +  admin_hex
   print 'Cookie Block 3 (in hex):\t' + asciiToHex( cookie_ascii[32:] )
   print ''



   old_cookie_hex = cookie_hex
   username = 'brent12345'
   cookie_hex = 'ac75f873cdc275990f6bbd139049189a3f199f3cab998ffdb6a298fc77225364'
   cookie_ascii = hexToAscii(cookie_hex)
   block1 = asciiToHex( cookie_ascii[:16] )
   start_block2 = asciiToHex( cookie_ascii[16:27] )
   new_block2 = start_block2 + admin_hex



   print 'username: ' + username
   print 'password: ' + username
   print 'cookie in hex: ' + cookie_hex
   print 'len(cookie_hex): ' + str(len(cookie_hex))

   print 'Cookie Block 2 (in hex):\t' + asciiToHex( cookie_ascii[16:] )
   print 'Cookie Block 2 (in ascii):\t # # # # # # r o l e = u s e r 0'
   print 'Want Cookie Block 2 (in ascii):  # # # # # # r o l e = a d m i n'
   print 'Start (in hex):\t\t\t'  + start_block2
   print 'admin (at the end of the block in hex):\t\t      ' +  admin_hex
   print 'New Block 2 (in hex):\t\t' + new_block2

   print ''

   print 'New Cookie Block 1 (in hex):    ' + block1
   print 'New Cookie Block 2 (in hex):    ' + new_block2
   print 'New Cookie Block 3 (in hex):    ' + block3

   print ''

   username = 'brent12345'
   print 'username: ' + username
   print 'password: ' + username
   print 'Final Cookie: ' + block1 + new_block2 + block3
   print ''

def taskIIIA():
   print 'TaskIIIA: \n'
   filename = 'Lab2.TaskIII.A.txt'
   ciphertext = ''
   with open(filename) as f:
      for line in f:
         ciphertext += line.strip()
   
   plaintext = cbc_decrypt(ciphertext, 'MIND ON MY MONEY', 'MONEY ON MY MIND')
   print plaintext

def get_to_xor():
   user_line = [0,0,0,0,0,0,0,117, 115, 101, 114, 0, 0, 0, 0, 0, 6]
   admin_line = [0,0,0,0,0,0,0,97, 100, 109, 105, 110, 0, 0, 0, 0, 5]
   xor_line_ascii = ''

   for i in xrange(0,len(user_line)):
      xor_line_ascii += (chr(user_line[i] ^ admin_line[i]))



   # xor_line = asciiToHex(xor_line_ascii)

   # print xor_line
   return xor_line_ascii

def getNewBlock(orig, to_xor):

   ascii_orig = hexToAscii(orig)
   ascii_xor = hexToAscii(to_xor)

   xored_ascii = xor(ascii_orig, ascii_xor)

   print asciiToHex(xored_ascii)

def ecbCookie(cookie1, cookie2):

   newCookie = cookie1[:64] + cookie2[32:]

   print newCookie


def taskIIIB(ciphertext):

   string1 = '\0' + '\0' '\0' + '\0' + '\0' + '\0' + '\0' + '\0' + '\0' + '\0' + '\0' + "23456"
   string2 = '\0' + '\0' '\0' + '\0' + '\0' + '\0' + '\0' + '\0' + '\0' + '\0' + '\0' + "&uid="

   iv_xor = xor(string1, string2)
   cipherIv = hexToAscii(ciphertext[:32])
   newCipherIV = asciiToHex(xor(iv_xor, cipherIv))

   string3 = '\0' + '\0' + '\0' + '\0' + '\0' + '\0' + "user" + '\0' + '\0' + '\0' + '\0' + '\0' + chr(0x6)
   string4 = '\0' + '\0' + '\0' + '\0' + '\0' + '\0' + "admin" + '\0' + '\0' + '\0' + '\0' + chr(0x5)

   block_xor = xor(string3, string4)
   cipherBlock = hexToAscii(ciphertext[64:96])
   newCipherBlock = asciiToHex(xor(block_xor, cipherBlock))

   newCipherText = newCipherIV + ciphertext[32:64] + newCipherBlock + ciphertext[96:]

   print newCipherText

def main():
   #taskIIA()
   #taskIIB()
   #taskIIC()
   taskIIIA()


if __name__ == '__main__':
   main()

