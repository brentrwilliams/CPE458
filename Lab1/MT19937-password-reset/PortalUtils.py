import urllib
import urllib2
import re
import time
import subprocess
from CryptoUtils import base64ToAscii


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


def main():
   p = start_server()
   register()
   randomNumbers = get_random_numbers()
   print 'randomNumbers: ' + str(randomNumbers)
   print 'len(randomNumbers): ' + str(len(randomNumbers))
   p.terminate()


if __name__ == '__main__':
   main()