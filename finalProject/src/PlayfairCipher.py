from CryptoUtils import NGramScorer
from math import exp
import random
from subprocess import Popen, PIPE

def getKeySquare(key):
   keySquare = [
         ['*','*','*','*','*'], 
         ['*','*','*','*','*'],
         ['*','*','*','*','*'],
         ['*','*','*','*','*'],
         ['*','*','*','*','*']
      ]
   key = key.lower()
   key = key.replace('j', 'i')

   truncatedKey = ''
   usedChars = set()
   for char in key:
      if not char in usedChars:
         usedChars.add(char)
         truncatedKey += char

   alphabet = list('abcdefghiklmnopqrstuvwxyz')

   index = 0
   for char in truncatedKey:
      keySquare[index//5][index%5] = char
      alphabet.remove(char)
      index += 1

   for char in alphabet:
      keySquare[index//5][index%5] = char
      index += 1

   return keySquare


def printKeySquare(keySquare):
   for keySquareLine in keySquare:
      for char in keySquareLine:
         print(char + ' '),
      print ''


def processPlaintext(plaintext):
   '''
   Process the plaintext to return a list of the plaintext broken into letter pairs
   '''
   print plaintext

   # Remove non-alphabetic characters
   updatedPlaintext = ''
   for char in plaintext.lower():
      if char.isalpha():
         updatedPlaintext += char
   plaintext = updatedPlaintext

   # Replace characters not in the key square
   plaintext = plaintext.replace('j', 'i')

   # Identify any double letters in the plaintext and replace the second occurence with an 'x' e.g. 'hammer' -> 'hamxer'
   for i in xrange(0,len(plaintext)-1):
      char1 = plaintext[i]
      char2 = plaintext[i+1]
      if char1 == char2:
         plaintext = plaintext[:i+1] + 'x' + plaintext[i+2:]

   # If the plaintext has an odd number of characters, append an 'x' to the end to make it even.
   if len(plaintext) % 2 == 1 :
      plaintext += 'x'

   # Break the plaintext into pairs of letters, e.g. 'hamxer' -> 'ha mx er
   letterPairs = []
   for i in xrange(0,len(plaintext), 2):
      letterPairs.append(plaintext[i:i+2])

   return letterPairs


def getRowCol(letter, keySquare):
   for row in range(0,5):
      for col in range(0,5):
         if keySquare[row][col] == letter:
            return (row,col)
      


def encodeLetterPair(letterPair, keySquare):
   row0, col0 = getRowCol(letterPair[0], keySquare)
   row1, col1 = getRowCol(letterPair[1], keySquare)

   if row0 != row1 and col0 != col1:
      return keySquare[row0][col1] + keySquare[row1][col0]
   elif row0 == row1:
      return keySquare[row0][(col0+1)%5] + keySquare[row1][(col1+1)%5]
   return keySquare[(row0+1)%5][col0] + keySquare[(row1+1)%5][col1]


def decodeLetterPair(letterPair, keySquare):
   row0, col0 = getRowCol(letterPair[0], keySquare)
   row1, col1 = getRowCol(letterPair[1], keySquare)

   if row0 != row1 and col0 != col1:
      return keySquare[row0][col1] + keySquare[row1][col0]
   elif row0 == row1:
      return keySquare[row0][(col0-1)%5] + keySquare[row1][(col1-1)%5]
   return keySquare[(row0-1)%5][col0] + keySquare[(row1-1)%5][col1]


def encrypt(plaintext, key):
   '''
   plaintext is the plaintext in ASCII
   key is a set of alphabetic letters in ASCII
   '''
   keySquare = getKeySquare(key)
   letterPairs = processPlaintext(plaintext)

   encryptedLetterPairs = []
   for letterPair in letterPairs:
      encryptedLetterPairs.append(encodeLetterPair(letterPair, keySquare))

   return ''.join(encryptedLetterPairs)


def decrypt(ciphertext, key):
   '''
   ciphertext is the ciphertext in ASCII
   key is a set of alphabetic letters in ASCII
   '''
   keySquare = getKeySquare(key)
   letterPairs = []
   for i in range(0, len(ciphertext), 2):
      letterPairs.append(ciphertext[i:i+2])
   
   decryptedLetterPairs = []
   for letterPair in letterPairs:
      decryptedLetterPairs.append(decodeLetterPair(letterPair,keySquare))

   return ''.join(decryptedLetterPairs)


def decryptWithKeySquare(ciphertext, keySquare):
   '''
   ciphertext is the ciphertext in ASCII
   '''
   letterPairs = []
   for i in range(0, len(ciphertext), 2):
      letterPairs.append(ciphertext[i:i+2])
   
   decryptedLetterPairs = []
   for letterPair in letterPairs:
      decryptedLetterPairs.append(decodeLetterPair(letterPair,keySquare))

   return ''.join(decryptedLetterPairs)


def swap2Rows(key):
   i = random.randint(0,4)
   j = random.randint(0,4)

   while i == j:
      j = random.randint(0,4)

   row1 = key[i]
   row2 = key[j]

   key[i] = row2
   key[j] = row1

   return key


def swap2Cols(key):
   i = random.randint(0,4)
   j = random.randint(0,4)

   while i == j:
      j = random.randint(0,4)
   
   for x in xrange(0,len(key)):
      temp = key[x][i]
      key[x][i] = key[x][j]
      key[x][j] = temp

   return key


def swapRows(key):
   key.reverse()
   return key


def swapCols(key):
   for x in xrange(0,len(key)):
      temp = key[x][0]
      key[x][0] = key[x][4]
      key[x][4] = temp

      temp = key[x][1]
      key[x][1] = key[x][3]
      key[x][3] = temp

   return key


def reverseKey(key):
   newKey = [
         ['*','*','*','*','*'], 
         ['*','*','*','*','*'],
         ['*','*','*','*','*'],
         ['*','*','*','*','*'],
         ['*','*','*','*','*']
      ]
   for i in range(0,25):
      newI = 24 - i
      newKey[i//5][i%5] = key[newI//5][newI%5]

   return newKey


def swapLetters(key):
   randNum1 = random.randint(0,24)
   randNum2 = random.randint(0,24)

   while randNum1 == randNum2:
      randNum2 = random.randint(0,24)

   i1 = randNum1 // 5
   j1 = randNum1 % 5

   i2 = randNum2 // 5
   j2 = randNum2 % 5

   temp = key[i1][j1]
   key[i1][j1] = key[i2][j2]
   key[i2][j2] = temp

   return key


def modifyKey(key):
   newKey = []
   i = random.randint(0,49)
   if i == 0:
      newKey = swap2Rows(key)
   elif i == 1:
      newKey = swap2Cols(key)
   elif i == 2:
      newKey = swapRows(key)
   elif i == 3:
      newKey = swapCols(key)
   elif i == 4:
      newKey = reverseKey(key)
   else:
      newKey = swapLetters(key)
   
   return newKey


def crack(ciphertext):
   '''
   decrypt a ciphertext encrypted with a playfair cipher and an unknown key
   ciphertext is the ciphertext in ASCII
   '''
   print '\nCracking ciphertext...'
   maxRounds = 100 
   plaintext = Popen(["./a.out", ciphertext, str(maxRounds), 'v'], stdout=PIPE).communicate()[0]

   return plaintext


def main():
   plaintext = '''Carsten Egeberg Borchgrevink was an Anglo Norwegian polar explorer and a pioneer of modern Antarctic travel. He was the precursor of Robert Falcon Scott, Ernest Shackleton, Roald Amundsen and other more famous names associated with the Heroic Age of Antarctic Exploration. In some year, he led the British financed Southern Cross Expedition, which established a new Farthest South record'''
   key = 'ZMDCFQRNOEGHIKLWXBYAUVPST'
   ciphertext = encrypt(plaintext, key)
   
   crackedPlaintext = crack(ciphertext)
   print 'plaintext: ' + plaintext
   print 'ciphertext: ' + ciphertext
   print 'cracked plaintex: ' + crackedPlaintext



if __name__ == '__main__':
   main()