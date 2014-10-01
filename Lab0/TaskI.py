# Things that are good to know
# ord()
# chr()
# string.encode.hex

import sys
import string

def main():
   '''with open(sys.argv[1]) as f:
      for line in f:
         print line
   '''
   #taskIIB('Lab0.TaskII.B.txt')
   taskIIC('Lab0.TaskII.C.txt')


def asciiToHex(text):
   return text.encode(encoding='hex', errors='strict')

def hexToAscii(text):
   return text.decode(encoding='hex', errors='strict')

def asciiToBase64(text):
   return text.encode(encoding='base64',errors='strict') 

def base64ToAscii(text):
   return text.decode(encoding='base64',errors='strict')

def base64ToHex(text):
   return asciiToHex(base64ToAscii(text))

def hexToBase64(text):
   return asciiToBase64(hexToAscii(text))

def xor(plaintext, key):
   textLen = len(plaintext);
   keyLen = len(key);
   newString = "";

   for i in range(0, textLen):
      keyChar = key[i % keyLen];
      textChar = plaintext[i];
      
      keyInt = ord(keyChar);
      textInt = ord(textChar);
      
      newInt = keyInt ^ textInt;
      newChar = chr(newInt);

      newString += newChar;


   return newString

# 26
def indexOfCoincidence26(text):
   # Make the text be lowercase and strip all non-alphabetic characters so we 
   # only have 26 possible characters
   iocTextNums = [0] * 26
   iocTextLen = 0
   for ch in text:
      if ch.isalpha():
         chIndex = ord(ch.lower()) - 97
         iocTextNums[chIndex] += 1
         iocTextLen += 1

   if iocTextLen <= 1:
      return 0.0

   iocSum = 0.0
   for count in iocTextNums:
      iocSum += count * (count - 1)

   ioc = iocSum / (iocTextLen * (iocTextLen - 1))

   return ioc


# 256
def indexOfCoincidence256(text):
   iocTextNums = [0] * 256
   iocTextLen = 0
   for ch in text:
      chIndex = ord(ch)
      iocTextNums[chIndex] += 1
      iocTextLen += 1

   iocSum = 0.0
   for count in iocTextNums:
      iocSum += count * (count - 1)

   ioc = iocSum / (iocTextLen * (iocTextLen - 1))

   return ioc * 26

def getColumnText(keyIndex, cypherText, keyLen):
   columnText = ''
   for i in xrange(keyIndex, len(cypherText), keyLen):
      columnText += cypherText[i]
   return columnText

def getOccurence(text, letter):
   numLetters = 0
   for i in xrange(0, len(text)):
      textletter = text[i]
      if (textletter.isalpha()):
         if textletter.lower() == letter:
            numLetters += 1

   return numLetters

def getMostCommonChar(plaintext):
   text = plaintext.lower()
   charArray = [0] * 256
   maxChar = 0
   mostCommon = ''
   for i in xrange(0, len(text)):
      charArray[ord(text[i])] += 1
      num = charArray[ord(text[i])]
      if num > maxChar:
         maxChar = num
         mostCommon = text[i]

   return mostCommon 

def testByte(keyIndex, cypherText, keyLength):
   iocArray = 256 * [0.0]
   maxEOccurence = 0
   maxTOccurence = 0
   maxAOccurence = 0
   for key in xrange(0, 256):
      columnText = getColumnText(keyIndex, cypherText, keyLength)
      xoredText = xor(columnText, chr(key))
      if(getMostCommonChar(xoredText) == 'e'):
         newEOccurence = getOccurence(xoredText, 'e')
         if(newEOccurence > maxEOccurence):
            bestKey = key
            print "text(E): " + xoredText
            maxEOccurence = newEOccurence
      if(getMostCommonChar(xoredText) == 't'):
         #if maxEOccurence == 0:
         newTOccurence = getOccurence(xoredText, 't')
         if(newTOccurence > maxTOccurence):
            bestKey = key
            print "text(T): " + xoredText
            maxTOccurence = newTOccurence 

      if(getMostCommonChar(xoredText) == 'a'):
         #if maxEOccurence == 0:
         newAOccurence = getOccurence(xoredText, 'a')
         if(newAOccurence > maxAOccurence):
            bestKey = key
            print "text(A): " + xoredText
            maxAOccurence = newAOccurence 
   return bestKey
      #call indexOf Coincidence on testString
      #ioc = indexOfCoincidence26(xoredText)
      #iocArray[key] = ioc
      #print (str(key) + ': ' + str(ioc))

   #find best key
   #return byte key

def taskIIB(fileName):

   for key in xrange(0,256):
      #print chr(key)
      with open(fileName) as f:
         for line in f:
            xoredLine = xor(hexToAscii(line.strip()), chr(key))
            if all(c in string.printable for c in xoredLine):
               val = indexOfCoincidence26(xoredLine)
               if val < 0.068 and val > 0.062:
                  print xoredLine
                  print ("Key: " + str(key))
                  print ("IOC: " + str(val))

def taskIIC(fileName):
   maxLineLen = 10
   with open(fileName) as f:
      cypherText = ''
      for line in f:
         cypherTextLine = base64ToAscii(line.strip())
         cypherText += cypherTextLine

         #if len(cypherTextLine) > maxLineLen:
         #   maxLineLen = len(cypherTextLine)

   print ("maxLineLen: " + str(maxLineLen))
   columnIoc = []

   for keyLen in xrange(1, maxLineLen+1):
      iocSum = 0.0
      for keyIndex in xrange(0,keyLen):
         columnText = getColumnText(keyIndex, cypherText, keyLen)
         # columnText = ''
         # for i in xrange(keyIndex, len(cypherText), keyLen):
         #    columnText += cypherText[i]

         ioc = indexOfCoincidence256(columnText)
         iocSum += ioc

      columnIoc.append(iocSum / keyLen)

   print 'IOC of Key Length:'
   for i in xrange(0,maxLineLen):
      print(str(i+1) + ": " + str(columnIoc[i]))

   print 'IOC of key:'
   #testByte(keyIndex, cypherText, keyLength):
   theKey = ""
   for i in xrange(0, 5):
      theKey += str(testByte(i, cypherText, 5))

   print str(theKey)
   print xor(cypherText, theKey)

   ###FOUND KEY LEN AS 5
   # key = ''
   # for key1 in xrange(0,256):
   #    for key2 in xrange(0,256):
   #       for key3 in xrange(0,256):
   #          for key4 in xrange(0,256):
   #             for key5 in xrange(0,256):
   #                key = str(key1) + str(key2) + str(key3) + str(key4) + str(key5)
   #                xoredLine = xor(cypherText, key)
   #                if all(c in string.printable for c in xoredLine):
   #                   val = indexOfCoincidence26(xoredLine)
   #                   if val < 0.068 and val > 0.062:
   #                      print xoredLine
   #                      print ("Key: " + str(key))
   
if __name__ == '__main__':
   main()



























