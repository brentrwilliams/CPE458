#!/usr/bin/python

import urllib
import urllib2
import re
import time
import subprocess
from CryptoUtils import base64ToAscii, asciiToBase64
from MT19937 import MT19937


def start_server():
   print 'Starting Server...'
   p = subprocess.Popen(['python', 'server.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   time.sleep(2)
   print 'Server Started...'
   print ''
   return p


def register():
   print 'Registering...'
   data = {
           'user' : 'brent',
           'password' : 'brent',
           'Reset' : '',
          }
   
   encoded_data = urllib.urlencode(data)
   content = urllib2.urlopen("http://localhost:8080/register", encoded_data)
   print 'Done registering...'
   print ''

def reset_admin_token():
   data = {
           'user' : 'admin',
           'Reset' : '',
          }

   encoded_data = urllib.urlencode(data)
   content = urllib2.urlopen("http://localhost:8080/forgot",
           encoded_data)

   print "done resetting admin token"

def get_token():
   data = {
           'user' : 'brent',
           'Reset' : '',
          }

   encoded_data = urllib.urlencode(data)
   content = urllib2.urlopen("http://localhost:8080/forgot",
           encoded_data)

   lines = content.readlines()
   webPageText = ''.join(lines)

   found = re.search(r'<!--open_token-->localhost:8080/reset\?token=(.*)<!--close_token-->', webPageText)

   if not found:
      print 'Error: Could not find token!'
   
   token = found.group(1)
   return token


def get_random_numbers():
   randomNumbers = []
   for i in xrange(0,78):
      token = get_token()
      ascii = base64ToAscii(token)
      asciiNumbers = ascii.split(':')

      for asciiNumber in asciiNumbers:
         randomNumbers.append(int(asciiNumber))

   return randomNumbers

def unmix(y):
   magicNumA = 2636928640
   #print bin(y)
   y = y ^ (y >> 18)
   #print bin(y)
   y = y ^ ((y << 15) & 4022730752)
   #print bin(y)

   a = y << 7;
   b = y ^ (a & magicNumA)
   c = b << 7
   d = y ^ (c & magicNumA) # now we have 14 of the original
   e = d << 7
   f = y ^ (e & magicNumA) # now we have 21 of the original
   g = f << 7
   h = y ^ (g & magicNumA) # now we have 28 of the original
   i = h << 7
   y = y ^ (i & magicNumA)
   #print bin(y)
   a = y ^ (y >> 11)
   b = y ^ (a >> 11)
   y = y ^ (b >> 11) 
   #print bin(y)
   return y

def main():
   p = start_server()
   register()
   randomNumbers = get_random_numbers()
   state = []
   for num in randomNumbers:
      state.append(unmix(num))
   
   mt = MT19937(0)
   mt.MT = state
   tokenArray = []
   for i in xrange(0, 8):
      tokenArray.append(str(mt.extract_number()))

   newToken = ":".join(tokenArray)
   newToken = asciiToBase64(newToken)
   reset_admin_token()
   print "http://localhost:8080/reset?token=" + newToken
   #print get_token() 

   while True:
      time.sleep(2)
   #print 'randomNumbers: ' + str(randomNumbers)
   #print 'len(randomNumbers): ' + str(len(randomNumbers))
   #p.terminate()


if __name__ == '__main__':
   main()