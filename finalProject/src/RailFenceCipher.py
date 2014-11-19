from CryptoUtils import NGramScorer

def encrypt(plaintext, key):
   ciphertext = []

   plaintext = "".join(plaintext.splitlines())
   plaintext = "".join(plaintext.split(" "))

   for x in range(0, key):
      ciphertext.append("")


   modOp = key*2 - 2

   for i in xrange(0, len(plaintext)):
      
      if i % modOp > modOp/2:
         ciphertext[modOp % (i % modOp)] += plaintext[i]
      else:
         ciphertext[i % modOp] += plaintext[i]


   return "".join(ciphertext)


#modified 
def decrypt(ciphertext, key):
   plaintext = [''] * len(ciphertext)
   cipherTextInd = 0



   for line in xrange(0, key):
      if line == key - 1:
         skip = 2 *(key - 1)
      else:
         skip = 2 * (key - (line + 1))
      
      j = 0
      ptInd = line
      while ptInd < len(ciphertext):
         plaintext[ptInd] = ciphertext[cipherTextInd]
         cipherTextInd += 1

         if line == 0 or line == key - 1 or j % 2 == 0:
            ptInd += skip
         else:
            ptInd += 2 * (key - 1) - skip

         j+= 1

   return "".join(plaintext)

def crack(ciphertext):
   ciphLen = len(ciphertext)

   maxScore = -1000000000000000000
   bestKey = 0
   score = 0

   quadgramScorer = NGramScorer(4)
   bigramScorer = NGramScorer(2)
   trigramScorer = NGramScorer(3)

   for key in xrange(2, len(ciphertext)/2):
      #print key
      possplain = decrypt(ciphertext, key)
      #print possplain
      score = quadgramScorer.score(possplain) + bigramScorer.score(possplain) + trigramScorer.score(possplain)
      print "score for key " + str(key) + " is: " + str(score)
      if score > maxScore:
         maxScore = score
         bestKey = key

   print bestKey
   return decrypt(ciphertext, bestKey)


def main():
   text = '''Most of the production will take place in Montreal, where the studio is currently ramping up its feature animation team to work on Charming and subsequent
   productions. These first films will allow us to build infrastructure, a team, pipeline and so on, says Butler. It will help us make the feature animation studio we want to be. At the same time, were also going to start to go out and develop our own scripts for our movies. And theyll be ones we own more of going forward.In terms of animation style, Butler plans to maintain a visual effects quality to the work. Were very ambitious about the quality, he says. I want to capitalize on the high production values we instituted on Beans and then keep it in the box. In VFX you typically have to be a lot more agile, but I learnt my craft at Disney and I feel like we can manage them in a similar way. We want to be successful  make good looking films and make more than one.
   Cinesite will continue to work in visual effects  upcoming projects include The Man From U.N.C.L.E. and San Andreas, for example  but this work will run alongside animated features. Id love to do a feature length version of Beans, admits Butler when asked about future plans, who also notes that the studio also plans on accepting scripts and developing ideas for films.'''

   smallText = "hi my name is drew and I am trying to make a semi small message to encrypt lets see if this works"

   #text = "".join(text.splitlines())  
   cipher = encrypt(text, 5)
   print cipher

   print decrypt(cipher, 5)

   print "\n\n\n"
   print crack(cipher)

if __name__ == '__main__':
   main()