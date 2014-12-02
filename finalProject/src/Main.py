import RailFenceCipher
import SimpleSubCipher
import PlayfairCipher
import CaesarCipher
import VigenereCipher
from CryptoUtils import LetterFrequencies, index_of_coincidence, NGramScorer
import random

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
   cipher = random.randint(0, 3)
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

def generateStats(text, numTests, length):
   numCorrect = 0

   for x in range(0, numTests):
      plain = getRandText(text, length)
      ciphertext, cipher, decryptedtext = randomEncrypt(plain)
      newplain, crackcipher = crackCipherText(ciphertext)

      if newplain == decryptedtext and cipher == crackcipher:
         numCorrect += 1

      print "Done with test " + str(x) + " of 100 for length" + str(length)

   return numCorrect / numTests * 100.0



def main():
   
   textOfFile = ""

   with open("InputText.txt", "r") as myFile:
      textOfFile = myFile.read()

   plaintext = preprocessText(textOfFile)

   for x in range(1000, 99, -100):
      print "working on stats for length " + str(x)
      percentCorrect = generateStats(plaintext, 100, x)
      print "Stats for message length " + str(x) + ": " + str(percentCorrect) + " accuracy"



   #plaintext = 'Carsten Egeberg Borchgrevink was an Anglo Norwegian polar explorer and a pioneer of modern Antarctic travel. He was the precursor of Robert Falcon Scott, Ernest Shackleton, Roald Amundsen and other more famous names associated with the Heroic Age of Antarctic Exploration. In some year, he led the British financed Southern Cross Expedition, which established a new Farthest South record'
   #plaintext = preprocessText(plaintext)
   #ciphertext, cipher = randomEncrypt(plaintext)
   #ciphertext = preprocessText(ciphertext)
   

if __name__ == '__main__':
   main()