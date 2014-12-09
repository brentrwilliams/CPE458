import RailFenceCipher
import SimpleSubCipher
import PlayfairCipher
import CaesarCipher
import VigenereCipher
from CryptoUtils import LetterFrequencies, index_of_coincidence, NGramScorer
import random
import time

class Cipher(object):
   RAIL_FENCE = 0
   SIMPLE_SUB = 3
   PLAYFAIR = 4
   VIGENERE = 1
   CAESAR = 2
      


def preprocessText(text):
   alphabet = 'abcdefghijklmnopqrstuvwxyz'
   text = text.lower()
   newText = ''
   for char in text:
      if char in alphabet:
         newText += char
   return newText


def isPlayfair(ciphertext):
   letters = 'abcdefghijklmnopqrstuvwxyz'
   letterCounts = {}
   for letter in letters:
      letterCounts[letter] = 0

   for letter in ciphertext:
      letterCounts[letter] += 1

   numNonZero = 0
   for letter in letters:
      if letterCounts[letter] > 0:
         numNonZero += 1

   return (letterCounts['j'] == 0 and numNonZero == 25)

def isRail(ciphertext):
   epsilon = 1
   letter_freqs = LetterFrequencies(ciphertext)
   chi = letter_freqs.chi_squared()

   #print chi
   #print ciphertext

   return chi < 0 + epsilon and chi > 0 - epsilon
      

def isSubstitution(ciphertext):
   epsilon = 0.005

   ioc = index_of_coincidence(ciphertext)
   #print ioc

   return ioc < 0.067 + epsilon and ioc > 0.067 - epsilon


def randomEncrypt(plaintext):
   cipher = random.randint(0, 4)
   ciphertext = ""
   decryptedtext = ""

   if cipher == Cipher.RAIL_FENCE:
      #print "Encrypting with RailFence"
      railFenceKey = random.randint(2, len(plaintext)/2)
      ciphertext = RailFenceCipher.encrypt(plaintext, railFenceKey)
      decryptedtext = RailFenceCipher.decrypt(ciphertext, railFenceKey)
   elif cipher == Cipher.SIMPLE_SUB:
      #print "Encrypting with SimpleSubCipher"
      alph = list("abcdefghijklmnopqrstuvwxyz")
      random.shuffle(alph)
      subKey = "".join(alph)
      ciphertext = SimpleSubCipher.encrypt(plaintext, subKey)
      decryptedtext = SimpleSubCipher.decrypt(ciphertext, subKey)
   elif cipher == Cipher.PLAYFAIR:
      #print "Encrypting with PlayfairCipher"
      playFairkKey = 'ZMDCFQRNOEGHIKLWXBYAUVPST'
      ciphertext = PlayfairCipher.encrypt(plaintext, playFairkKey)
      decryptedtext = PlayfairCipher.decrypt(ciphertext, playFairkKey)
   elif cipher == Cipher.VIGENERE:
      #print "Encrypting with VigenereCipher"
      vigenereKey = "fjdklafjdklghjak"
      ciphertext = VigenereCipher.encrypt(plaintext, vigenereKey)
      decryptedtext = VigenereCipher.decrypt(ciphertext, vigenereKey)
   else:
      #print "Encrypting with CaesarCipher"
      caesarKey = random.randint(1, 25)
      ciphertext = CaesarCipher.encrypt(plaintext, caesarKey)
      decryptedtext = CaesarCipher.decrypt(ciphertext, caesarKey)

   return (ciphertext, cipher, decryptedtext)

def getRandText(text, length):
   index = random.randint(0, len(text) - length - 1)
   return text[index:index+length]

def crackCipherText(ciphertext):
   ciphertext = preprocessText(ciphertext)
   #print "ciphertext: " + ciphertext

   if isRail(ciphertext):
      #print "Predicting it is RailFence"
      newplain = RailFenceCipher.crack(ciphertext)
      return (newplain, Cipher.RAIL_FENCE)

   elif isSubstitution(ciphertext):
      #print "Predicting it is a Substitution cipher"

      digram = NGramScorer(2)
      trigram = NGramScorer(3)
      quadgram = NGramScorer(4)

      simpleSubPlain = SimpleSubCipher.crack(ciphertext)
      caesarPlain = CaesarCipher.crack(ciphertext)

      simpleScore = digram.score(simpleSubPlain) + trigram.score(simpleSubPlain) + quadgram.score(simpleSubPlain)
      caesarScore = digram.score(caesarPlain) + trigram.score(caesarPlain) + quadgram.score(caesarPlain)

      if simpleScore > caesarScore:
         #print "Predicting it is simple substitution"
         return (simpleSubPlain, Cipher.SIMPLE_SUB)
      else:
         #print "Predicting it is caesar"
         return (caesarPlain, Cipher.CAESAR)

   elif isPlayfair(ciphertext):
      #print "Predicting it is the PlayFair"
      newplain = PlayfairCipher.crack(ciphertext)
      return (newplain, Cipher.PLAYFAIR)
   else:
      #print "Predicting it is Vigenere"
      newplain = VigenereCipher.crack(ciphertext)
      return (newplain, Cipher.VIGENERE)


def getPercentCorrect(plain, expected):

   count = 0

   for x in range(0, len(plain)):
      if plain[x].lower() == expected[x].lower():
         count += 1

   return float(count) / len(plain) * 100.0


def generateStats(text, numTests, length):
   numCorrect = 0
   totPercentCorrect = 0
   totPercentCorrectWithCorrectCipher = 0
   numReadable = 0
   totVig = 0; totSS = 0; totRail = 0; totCaesar = 0; totPlay = 0
   numVig = 0; numSS = 0; numRail = 0; numCaesar = 0; numPlay = 0


   statsFile = open(str(length) + ".txt", "w+")

   for x in range(0, numTests):
      plain = getRandText(text, length)
      ciphertext, cipher, decryptedtext = randomEncrypt(plain)
      newplain, crackcipher = crackCipherText(ciphertext)

      print newplain
      print decryptedtext
      print cipher
      print crackcipher

      percentCorrect = getPercentCorrect(newplain.lower(), decryptedtext)
      totPercentCorrect += percentCorrect


      statsFile.write("checking string " + str(x) + " of " + str(numTests) + "\n")
      statsFile.write("    Correct Cipher: " + str(cipher == crackcipher) + "\n")
      statsFile.write("    Percent Plaintext Correct: " + str(percentCorrect) + "\n\n")

      if cipher == crackcipher:
         numCorrect += 1

         if cipher == Cipher.VIGENERE:
            totVig += percentCorrect
            numVig += 1
         elif cipher == Cipher.SIMPLE_SUB:
            totSS += percentCorrect
            numSS += 1
         elif cipher == Cipher.PLAYFAIR:
            totPlay += percentCorrect
            numPlay += 1
         elif cipher == Cipher.CAESAR:
            totCaesar += percentCorrect
            numCaesar += 1
         else:
            totRail += percentCorrect
            numRail += 1

         totPercentCorrectWithCorrectCipher += percentCorrect
      if percentCorrect > 75.0:
         numReadable += 1


      print "Done with test " + str(x) + " of 100 for length" + str(length)

   statsFile.write("==========================\nTOTAL BREAKDOWN\n==========================\n")
   statsFile.write("Percent Correct Chosen Cipher: " + str(float(numCorrect) / numTests * 100.0) + "\n")
   statsFile.write("Average Accuracy (Percent): " + str(float(totPercentCorrect) / numTests) + "\n")
   statsFile.write("Average Accuracy When Choosing Correct Cipher: " + str(float(totPercentCorrectWithCorrectCipher) / numCorrect) + "\n")
   statsFile.write("Percent Readable (75% Accurate): " + str(float(numReadable) / numTests * 100.0) + "\n\n")
   
   statsFile.write("Average Accuracy of RailFence: " + str(float(totRail) / numRail) + "\n")
   statsFile.write("Average Accuracy of SimpleSub: " + str(float(totSS) / numSS) + "\n")
   statsFile.write("Average Accuracy of Caesar: " + str(float(totCaesar) / numCaesar) + "\n")
   statsFile.write("Average Accuracy of Vigenere: " + str(float(totVig) / numVig) + "\n")
   statsFile.write("Average Accuracy of PlayFair: " + str(float(totPlay) / numPlay) + "\n")

   statsFile.close()

def getResponseToMenu():
   print '       MENU       '
   print '=================='
   print 'Encrypt:        1'
   print 'Decrypt:        2'
   print 'Crack:          3'
   print 'Run Statistics: 4'
   print 'Quit:           Q'
   print ''
   
   answer = raw_input('What would you like to do: ')
   answer = answer.strip()
   print ''
   return answer


def encryptUserInput():
   cipherName = {
      '1':'Rail Fence',
      '2':'Simple Substitution',
      '3':'Caesar',
      '4':'Vigenere',
      '5':'PlayFair',
   }

   keyInstructions = {
      '1':'Keys for the Rail Fence Cipher can be integers from 2 to half the length of the plaintext.',
      '2':'Keys for the Simple Substitution Cipher are a jumbled alphabet.',
      '3':'Keys for the Caesar Cipher can be an integer in the range [1,25].',
      '4':'Keys for the Vigenere Cipher can be any alphabetic text.',
      '5':'Keys for the Playfair Cipher are a jumbled alphabet without the letter \'J\'',
   }

   cipherEncryptMap = {
      '1':RailFenceCipher.encrypt,
      '2':SimpleSubCipher.encrypt,
      '3':CaesarCipher.encrypt,
      '4':VigenereCipher.encrypt,
      '5':PlayfairCipher.encrypt,
   }

   print '        CIPHERS'
   print '======================'
   print 'Rail Fence:          1'
   print 'Simple Substitution: 2'
   print 'Caesar:              3'
   print 'Vigenere:            4'
   print 'PlayFair:            5'

   answer = raw_input('What cipher would you like to encrypt with? ')
   answer = answer.strip()
   
   if answer in cipherName:
      encrypt = cipherEncryptMap[answer]
      print ''
      print 'Thank you for choosing the ' + cipherName[answer] + ' cipher'
      print ''
      print keyInstructions[answer]
      key = raw_input('Please enter a key: ')

      if answer == '1' or answer == '3':
         key = int(key)
      else:
         key = preprocessText(key)

      plaintext = raw_input('Please enter the plaintext you would like to encrypt: ')
      plaintext = preprocessText(plaintext)
      print ''
      print 'Your encrypted plaintext is the following:'
      print encrypt(plaintext, key)

   else:
      print 'Invalid input'
   
   print ''
   return


def decryptUserInput():
   cipherName = {
      '1':'Rail Fence',
      '2':'Simple Substitution',
      '3':'Caesar',
      '4':'Vigenere',
      '5':'PlayFair',
   }

   cipherDecryptMap = {
      '1':RailFenceCipher.decrypt,
      '2':SimpleSubCipher.decrypt,
      '3':CaesarCipher.decrypt,
      '4':VigenereCipher.decrypt,
      '5':PlayfairCipher.decrypt,
   }

   print '        CIPHERS'
   print '======================'
   print 'Rail Fence:          1'
   print 'Simple Substitution: 2'
   print 'Caesar:              3'
   print 'Vigenere:            4'
   print 'PlayFair:            5'

   answer = raw_input('What cipher would you like to decrypt with? ')
   answer = answer.strip()

   if answer in cipherName:
      decrypt = cipherDecryptMap[answer]
      print ''
      print 'Thank you for choosing the ' + cipherName[answer] + ' cipher'
      print ''
      ciphertext = raw_input('Please enter the ciphertext you would like to decrypt: ')
      ciphertext = preprocessText(ciphertext)

      key = raw_input('Please enter a key: ')
      if answer == '1' or answer == '3':
         key = int(key)
      else:
         key = preprocessText(key)

      print ''
      print 'Your decrypted ciphertext is the following:'
      print decrypt(ciphertext, key)
   else:
      print 'Invalid input'

   print ''
   return


def crackUserInput():
   ciphertext = raw_input('Please enter the ciphertext you would like to crack: ')
   ciphertext = preprocessText(ciphertext)
   plaintext = crackCipherText(ciphertext)

   print plaintext[0]


def runStatistics():
   with open("InputText.txt", "r") as myFile:
      textOfFile = myFile.read()

   plaintext = preprocessText(textOfFile)

   tests = [100, 150, 250, 500]
   for x in tests:
      print "NOTE:"
      print "- FOR ALL STATS TO BE RUN IT WILL TAKE A FEW HOURS"
      print "- EACH RESULT WILL NOT BE WRITTEN TO A FILE UNTIL ITS WHOLE TEST HAS COMPLETED"
      print 'YOU HAVE BEEN WARNED'

      time.sleep(10)

      print ''
      print "Working on stats for length " + str(x)
      print "Writing statistical output for this test to " + str(x) + ".txt"
      print ''
      print ''
      
      percentCorrect = generateStats(plaintext, 100, x)
      print "Stats for message length " + str(x) + ": " + str(percentCorrect) + " accuracy"


def main():
   answer = getResponseToMenu()

   while answer.upper() != 'Q':

      if answer == '1':
         encryptUserInput()
      elif answer == '2':
         decryptUserInput()
      elif answer == '3':
         crackUserInput()
      elif answer == '4':
         runStatistics()
      else:
         print 'Did not understand input...'
      
      answer = getResponseToMenu()


   



if __name__ == '__main__':
   main()