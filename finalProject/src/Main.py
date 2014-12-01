import RailFenceCipher
import SimpleSubCipher
import PlayfairCipher
import CaesarCipher
import VigenereCipher
from CryptoUtils import LetterFrequencies, index_of_coincidence, NGramScorer
import random

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
   print ioc

   return ioc < 0.067 + epsilon and ioc > 0.067 - epsilon
      

def main():
   plaintext = 'Carsten Egeberg Borchgrevink was an Anglo Norwegian polar explorer and a pioneer of modern Antarctic travel. He was the precursor of Robert Falcon Scott, Ernest Shackleton, Roald Amundsen and other more famous names associated with the Heroic Age of Antarctic Exploration. In some year, he led the British financed Southern Cross Expedition, which established a new Farthest South record'
   
   plaintext = preprocessText(plaintext)

   num = 2#random.randint(0, 4)
   ciphertext = ""

   if num == 0:
      print "Encrypting with RailFence"
      railFenceKey = random.randint(2, len(plaintext)/2)
      ciphertext = RailFenceCipher.encrypt(plaintext, railFenceKey)
   elif num == 1:
      print "Encrypting with SimpleSubCipher"
      alph = list("abcdefghijklmnopqrstuvwxyz")
      random.shuffle(alph)
      subKey = "".join(alph)
      ciphertext = SimpleSubCipher.encrypt(plaintext, subKey)
   elif num == 2:
      print "Encrypting with PlayfairCipher"
      playFairkKey = 'ZMDCFQRNOEGHIKLWXBYAUVPST'
      ciphertext = PlayfairCipher.encrypt(plaintext, playFairkKey)
   elif num == 3:
      print "Encrypting with VigenereCipher"
      vigenereKey = "fjdklafjdklghjak"
      ciphertext = VigenereCipher.encrypt(plaintext, vigenereKey)
   else:
      print "Encrypting with CaesarCipher"
      caesarKey = random.randint(1, 25)
      ciphertext = CaesarCipher.encrypt(plaintext, caesarKey)



   ciphertext = preprocessText(ciphertext)
   print "ciphertext: " + ciphertext

   if isRail(ciphertext):
      print "Predicting it is RailFence"
      newplain = RailFenceCipher.crack(ciphertext)
      print "plaintext: " + newplain
   elif isSubstitution(ciphertext):
      print "Predicting it is a Substitution cipher"

      digram = NGramScorer(2)
      trigram = NGramScorer(3)
      quadgram = NGramScorer(4)

      simpleSubPlain = SimpleSubCipher.crack(ciphertext)
      caesarPlain = CaesarCipher.crack(ciphertext)

      simpleScore = digram.score(simpleSubPlain) + trigram.score(simpleSubPlain) + quadgram.score(simpleSubPlain)
      caesarScore = digram.score(caesarPlain) + trigram.score(caesarPlain) + quadgram.score(caesarPlain)

      if simpleScore > caesarScore:
         print "Predicting it is simple substitution"
         print "plaintext: " + simpleSubPlain
      else:
         print "Predicting it is caesar"
         print "plaintext: " + caesarPlain

   elif isPlayfair(ciphertext):
      print "Predicting it is the PlayFair"
      newplain = PlayfairCipher.crack(ciphertext)
      print "plaintext: " + newplain
   else:
      print "Predicting it is Vigenere"
      newplain = VigenereCipher.crack(ciphertext)
      print "plaintext: " + newplain

if __name__ == '__main__':
   main()