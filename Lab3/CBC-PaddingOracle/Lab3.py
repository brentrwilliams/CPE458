
import urllib
import urllib2
import re
import time
import subprocess
from CryptoUtils import xor 

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

def findPlain(ciphertext):

   plainText = ''
   cipherLen = len(ciphertext)
   numBytes = cipherLen / 2
   numBlocks = numBytes / 16

   for blockInd in xrange(numBlocks - 1, -1, -1):
      c2Ind = blockInd * 32 
      c2 = ciphertext[c1Ind : c1Ind + 32]
      c1 = c2Ind - 32
      c1 = ciphertext[c1Ind: c2Ind]
      i2 = ''

      for bytInd in xrange(15, -1, -1):
         c1Tail = ''
         numTrailingBytes = 15 - bytInd

         for l in xrange(0, numTrailingBytes):
            c1Tail += hex(numTrailingBytes + 1)

         c1Tail = xor(c1Tail, i2)

         for k in xrange(0, 256):
            
            c1Prime = c1[0:byteInd*2] + hex(k) + c1Tail
            newCipher = c1Prime + c2
            
            if check_ciphertext(newCipher):
               nextInterByte = k ^ (numTrailingBytes + 1)
               i2 = nextInterByte + i2

      newPlain = xor(c1, i2)

      plainText = newPlain + plainText


def check_ciphertext(ciphertext):
   result = False

   try:
      resp = urllib2.urlopen("http://0.0.0.0:8080/?enc=" + ciphertext)
   except Exception, e:
      
      if str(e) == 'HTTP Error 404: Not Found':
         result = True
      elif str(e) == 'HTTP Error 403: Forbidden':
         result = False
      else:
         raise e

   return result


def main():
   server = start_server()

   ciphertext = get_ciphertext()
   print ciphertext

   print check_ciphertext(ciphertext)

   raw_input() # Wait to stop the server
   stop_server(server)


if __name__ == '__main__':
   main()