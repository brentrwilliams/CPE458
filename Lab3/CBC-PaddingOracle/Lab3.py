
import urllib
import urllib2
import re
import time
import subprocess

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

def main():
   server = start_server()

   print get_ciphertext()

   raw_input() # Wait to stop the server
   stop_server(server)


if __name__ == '__main__':
   main()