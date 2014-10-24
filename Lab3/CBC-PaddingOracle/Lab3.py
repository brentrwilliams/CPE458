
import urllib
import urllib2
import re
import time
import subprocess
from CryptoUtils import xor, hexToAscii, asciiToHex 

I2 = []

def start_server():
   print 'Starting Server...'
   p = subprocess.Popen(['python', 'server.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   time.sleep(2)
   print 'Server Started...'
   print ''
   return p


def stop_server(server):
   print 'Stopping Server...'
   server.terminate()
   time.sleep(1) # make sure it doesn't leave the server as a zombie process
   print 'Server Stopped...'


def get_ciphertext():
   resp = urllib2.urlopen('http://0.0.0.0:8080/eavesdrop')
   page = resp.read()

   found = re.search(r'<p><font color="red">(.*)</font></p>', page)

   if not found:
      print 'Error: Could not find token!'
   
   ciphertext = found.group(1).strip()

   return ciphertext

def two_space_hex(hex_str):
   if len(hex_str) == 3:
      return '0' + hex_str[2]
   else:
      return hex_str[2:]


def findPlain(ciphertext):

   plainText = ''
   cipherLen = len(ciphertext)
   numBytes = cipherLen / 2
   numBlocks = numBytes / 16

   for blockInd in xrange(numBlocks - 1, 0, -1):
      c2Ind = blockInd * 32 
      c2 = ciphertext[c2Ind : c2Ind + 32]
      c1Ind = c2Ind - 32
      c1 = ciphertext[c1Ind: c2Ind]
      i2 = ''

      for byteInd in xrange(15, -1, -1):
         plaintextTail = ''
         numTrailingBytes = 15 - byteInd

         for l in xrange(0, numTrailingBytes):
            plaintextTail += two_space_hex( hex(numTrailingBytes + 1) )
            #print 'l:' + str(l)

         c1Tail = asciiToHex(xor(hexToAscii(plaintextTail), hexToAscii(i2)))

         for k in xrange(0, 256):
            #print 'k: ' + str(k)
            c1Prime = c1[0:byteInd*2] + two_space_hex( hex(k) ) + c1Tail
            newCipher = c1Prime + c2
            
            #print 'a'
            ciphertext_good = check_ciphertext(newCipher)
            #print 'b'

            if ciphertext_good:
               #print 'found ' + str(byteInd)
               nextInterByte = two_space_hex(hex(k ^ (numTrailingBytes + 1)))
               i2 = nextInterByte + i2
               break

      newPlain = xor( hexToAscii(c1), hexToAscii(i2))
      print newPlain
      plainText = newPlain + plainText

   print plainText
   return plainText


def check_ciphertext(ciphertext):
   result = False

   try:
      #print len(ciphertext)
      #print ciphertext
      resp = urllib2.urlopen("http://0.0.0.0:8080/?enc=" + ciphertext, timeout=2)
   except Exception, e:
      #print 'after'
      if str(e) == 'HTTP Error 404: Not Found':
         result = True
      elif str(e) == 'HTTP Error 403: Forbidden':
         result = False
      elif str(e) == 'timed out':
         print 'Recursing...'
         result = check_ciphertext(ciphertext)
      else:
         raise e

   return result


def main():
   #server = start_server()

   ciphertext = get_ciphertext()
   print ciphertext

   findPlain(ciphertext)  

   print 'Waiting...'
   raw_input() # Wait to stop the server
   #stop_server(server)


if __name__ == '__main__':
   main()