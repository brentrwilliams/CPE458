
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


def crack(ciphertext):
   '''
   decrypt a ciphertext encrypted with a playfair cipher and an unknown key
   ciphertext is the ciphertext in ASCII
   '''
   pass


def main():
   plaintext = 'we are discovered, save yourself'
   key = 'monarchy'
   ciphertext = encrypt(plaintext, key)
   crackedPlaintext = decrypt(ciphertext, key)
   print 'plaintext: ' + plaintext
   print 'ciphertext: ' + ciphertext
   print 'cracked plaintex: ' + crackedPlaintext


if __name__ == '__main__':
   main()