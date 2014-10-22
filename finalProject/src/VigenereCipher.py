from CryptoUtils import LetterFrequencies, index_of_coincidence

def char_to_index(char):
   return ord(char.lower()) - ord('a')

def index_to_char(index):
   alphabet = "abcdefghijklmnopqrstuvwxyz"
   return alphabet[index % 26]

def create_tableau():
   alphabet = "abcdefghijklmnopqrstuvwxyz"
   tableau = []
   for y in range(0,26):
      row = []
      for x in range(0,26):
         row.append(alphabet[(x + y) % 26])
      tableau.append(row)
   return tableau
         

def encrypt(plaintext, key):
   '''
   plaintext is the plaintext in ASCII
   key is a set of alphabetic letters in ASCII
   '''
   ciphertext = ''
   tableau = create_tableau()
   key_index = 0

   for char in plaintext.lower():
      if char.isalpha():
         row_index = char_to_index(char)
         col_index = char_to_index(key[key_index])
         ciphertext += tableau[row_index][col_index]
         key_index = (key_index + 1) % len(key)

      else:
         ciphertext += char

   return ciphertext
   

def decrypt(ciphertext, key):
   '''
   ciphertext is the ciphertext in ASCII
   key is a set of alphabetic letters in ASCII
   '''
   plaintext = ''
   tableau = create_tableau()
   key_index = 0

   for char in ciphertext.lower():
      if char.isalpha():
         row_index = char_to_index(key[key_index])
         char_index = tableau[row_index].index(char)
         plaintext += index_to_char(char_index)

         key_index = (key_index + 1) % len(key)
      else:
         plaintext += char

   return plaintext


def crack(ciphertext):
   '''
   decrypt a ciphertext encrypted with a caesar cipher and an unknown key
   ciphertext is the ciphertext in ASCII
   '''
   best_plaintext = ''
   stripped_ciphertext = [char.lower() for char in ciphertext if char.isalpha()]
   for period in range(2,27):
      sum_ioc = 0.0
      for index in range(0,period):
         text = ''.join([stripped_ciphertext[i] for i in range(0+index, len(stripped_ciphertext), period)])
         #print text
         ioc = index_of_coincidence(text)
         #print ioc
         sum_ioc += ioc

      average_ioc = sum_ioc / period
      print str(period) + ': ' + str(average_ioc)


   return best_plaintext


def main():
   text = '''Most of the production will take place in Montreal, where the studio is currently ramping up its feature animation team to work on Charming and subsequent productions. These first films will allow us to build infrastructure, a team, pipeline and so on, says Butler. It will help us make the feature animation studio we want to be. At the same time, were also going to start to go out and develop our own scripts for our movies. And theyll be ones we own more of going forward.
In terms of animation style, Butler plans to maintain a visual effects quality to the work. Were very ambitious about the quality, he says. I want to capitalize on the high production values we instituted on Beans and then keep it in the box. In VFX you typically have to be a lot more agile, but I learnt my craft at Disney and I feel like we can manage them in a similar way. We want to be successful  make good looking films and make more than one.
Cinesite will continue to work in visual effects  upcoming projects include The Man From U.N.C.L.E. and San Andreas, for example  but this work will run alongside animated features. Id love to do a feature length version of Beans, admits Butler when asked about future plans, who also notes that the studio also plans on accepting scripts and developing ideas for films.'''

   key = 'FORTIFICATION'
   ciphertext = encrypt(text, key)
   #ciphertext = 'vptnvffuntshtarptymjwzirappljmhhqvsubwlzzygvtyitarptyiougxiuydtgzhhvvmumshwkzgstfmekvmpkswdgbilvjljmglmjfqwioiivknulvvfemioiemojtywdsajtwmtcgluysdsumfbieugmvalvxkjduetukatymvkqzhvqvgvptytjwwldyeevquhlulwpkt'

   print 'ciphertext: '
   print ciphertext
   print ''
   print 'cracked plaintext:'
   print crack(ciphertext)


if __name__ == '__main__':
   main()