import RailFenceCipher
import SimpleSubCipher
from CryptoUtils import LetterFrequencies, index_of_coincidence

def checkIfRail(ciphertext):
   epsilon = 1
   letter_freqs = LetterFrequencies(ciphertext)
   chi = letter_freqs.chi_squared()

   #print chi
   #print ciphertext

   if chi < 0 + epsilon and chi > 0 - epsilon:
      return True

   return False

def checkIfSubstitution(ciphertext):
   epsilon = 0.005

   ioc = index_of_coincidence(ciphertext)
   print ioc

   if ioc < 0.06 + epsilon and ioc > 0.06 - epsilon:
      return True

   return False



def main():
   text = "hello my name is drew aNd i Am going to decrypt this message i hope it works because this is getting really annoying and i want this to work very badly please program do this for me the world depends on it and i want it to work hello my name is drew aNd i Am going to decrypt this message i hope it works because this is getting really annoying and i want this to work very badly please program do this for me the world depends on it and i want it to work"
   #text = '''Most of the production will take place in Montreal, where the studio is currently ramping up its feature animation team to work on Charming and subsequent productions. These first films will allow us to build infrastructure, a team, pipeline and so on, says Butler. It will help us make the feature animation studio we want to be. At the same time, were also going to start to go out and develop our own scripts for our movies. And theyll be ones we own more of going forward.
#In terms of animation style, Butler plans to maintain a visual effects quality to the work. Were very ambitious about the quality, he says. I want to capitalize on the high production values we instituted on Beans and then keep it in the box. In VFX you typically have to be a lot more agile, but I learnt my craft at Disney and I feel like we can manage them in a similar way. We want to be successful  make good looking films and make more than one.
#Cinesite will continue to work in visual effects  upcoming projects include The Man From U.N.C.L.E. and San Andreas, for example  but this work will run alongside animated features. Id love to do a feature length version of Beans, admits Butler when asked about future plans, who also notes that the studio also plans on accepting scripts and developing ideas for films.'''

   #cipher = RailFenceCipher.encrypt(text, 3)
   cipher = SimpleSubCipher.encrypt(text, "qwertyuiopasdfghjklzxcvbnm")
   print checkIfRail(cipher)
   print checkIfSubstitution(cipher)

   pass

if __name__ == '__main__':
   main()