# TaskI.py

import random
import time
from MersenneTwister import MersenneTwister
from CryptoUtils import asciiToBase64

def oracle(randNum):
   print 'Searching for seed...'

   maxSeed = 2**32
   twoMinutes = 120
   startingPoint = int(time.time() - twoMinutes)

   for i in xrange(startingPoint, maxSeed):
      mt = MersenneTwister(i)
      retVal = mt.extract_number()

      if retVal == randNum:
         return asciiToBase64(str(i))

   print 'Error: Could not find seed'
   return ''


def main():
   timeToSleep = random.randint(5,60)
   print 'Sleeping for ' + str(timeToSleep) + ' seconds...'
   print ''
   time.sleep(timeToSleep)
 
   print 'Seeding MersenneTwister...'
   print ''
   seed = int(time.time()) 
   mt = MersenneTwister(seed)

   timeToSleep = random.randint(5,60)
   print 'Sleeping for ' + str(timeToSleep) + ' seconds...'
   print ''
   time.sleep(timeToSleep)

   randNum = mt.extract_number()

   print '\tFound Seed:\t' + oracle(randNum)
   print '\tActual Seed:\t' + asciiToBase64(str(seed))


if __name__ == '__main__':
   main()






