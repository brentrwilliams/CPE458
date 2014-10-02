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

frequencyMap = {'a': 0.08167,
                'b': 0.01492,
                'c': 0.02782,
                'd': 0.04253,
                'e': 0.12072,
                'f': 0.02228,
                'g': 0.02015,
                'h': 0.06094,
                'i': 0.06966,
                'j': 0.00153,
                'k': 0.00772,
                'l': 0.04025,
                'm': 0.02406,
                'n': 0.06749,
                'o': 0.07507,
                'p': 0.01929,
                'q': 0.00095,
                'r': 0.05987,
                's': 0.06327,
                't': 0.09056,
                'u': 0.02758,
                'v': 0.00978,
                'w': 0.02630,
                'x': 0.00150,
                'y': 0.01974,
                'z': 0.00074 
               }

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
   columnText = ""
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

def frequencyAnalysis(text):
   total = 0
   frequencyArray = [0] * 26
   #if all(c in string.printable for c in text):
   for i in xrange(0, len(text)):
      char = text[i]
      if(char.isalpha()):
         lowerChar = char.lower()
         chIndex = ord(lowerChar) - 97
         frequencyArray[chIndex] += 1

   for letter in xrange(0, 26):
      asciiLetter = chr(letter + 97)
      total += frequencyArray[letter] * frequencyMap[asciiLetter]

   return total

def testByte(keyIndex, cypherText, keyLength):
   iocArray = 256 * [0.0]
   keyList = []
   bestKey = 0
   maxCorellation = 0 
   for key in xrange(0, 256):
      columnText = getColumnText(keyIndex, cypherText, keyLength)
      xoredText = xor(columnText, chr(key))
      corolation = frequencyAnalysis(xoredText)
      if corolation > maxCorellation:
         maxCorellation = corolation
         bestKey = key
      #call indexOf Coincidence on testString
      #ioc = indexOfCoincidence26(xoredText)
      #if ioc > 0.6 && ioc < 0.7:
       #  keyList.append(key)
        # print key
      #iocArray[key] = ioc
   
   return bestKey
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
   listOfKeys = []
   theKey = ""
   for i in xrange(0, 5):
      theKey += chr(testByte(i, cypherText, 5))

   
   print xor(cypherText, str(theKey))

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



























