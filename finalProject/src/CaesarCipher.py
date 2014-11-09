from CryptoUtils import LetterFrequencies, index_to_char, char_to_index

def encrypt(plaintext, key):
   '''
   plaintext is the plaintext in ASCII
   key is a number 1-25 that shifts the letters
   '''
   ciphertext = ''
   for char in plaintext.lower():
      if char.isalpha():
         char_num = ord(char) - ord('a')
         new_char_num = (char_num + key) % 26
         ciphertext += chr(new_char_num + ord('a'))
      else:
         ciphertext += char

   return ciphertext
   

def decrypt(ciphertext, key):
   '''
   ciphertext is the ciphertext in ASCII
   key is a number 1-25 that shifts the letters
   '''
   plaintext = ''
   for char in ciphertext.lower():
      if char.isalpha():
         char_num = ord(char) - ord('a')
         new_char_num = (char_num - key) % 26
         plaintext += chr(new_char_num + ord('a'))
      else:
         plaintext += char

   return plaintext


def get_best_key(ciphertext):
   letter_frequencies = LetterFrequencies(ciphertext)
   best_chi_squared = letter_frequencies.chi_squared()
   best_key = 1
   
   for key in xrange(1,26):
      possible_plaintext = decrypt(ciphertext, key)
      letter_frequencies = LetterFrequencies(possible_plaintext)
      chi_squared = letter_frequencies.chi_squared()
      #print str(index_to_char(key)) + ': ' + str(chi_squared)
      
      if chi_squared < best_chi_squared:
         best_chi_squared = chi_squared
         best_key = key

   return best_key


def crack(ciphertext):
   '''
   decrypt a ciphertext encrypted with a caesar cipher and an unknown key
   ciphertext is the ciphertext in ASCII
   '''
   letter_frequencies = LetterFrequencies(ciphertext)
   best_chi_squared = letter_frequencies.chi_squared()
   best_plaintext = ciphertext
   
   for key in xrange(0,26):
      possible_plaintext = decrypt(ciphertext, key)
      letter_frequencies = LetterFrequencies(possible_plaintext)
      chi_squared = letter_frequencies.chi_squared()
      #print str(key) + ':\t' + str(chi_squared)
      
      if chi_squared < best_chi_squared:
         best_chi_squared = chi_squared
         best_plaintext = possible_plaintext

   return best_plaintext


def main():
   text = '''Most of the production will take place in Montreal, where the studio is currently ramping up its feature animation team to work on Charming and subsequent productions. These first films will allow us to build infrastructure, a team, pipeline and so on, says Butler. It will help us make the feature animation studio we want to be. At the same time, were also going to start to go out and develop our own scripts for our movies. And theyll be ones we own more of going forward.
In terms of animation style, Butler plans to maintain a visual effects quality to the work. Were very ambitious about the quality, he says. I want to capitalize on the high production values we instituted on Beans and then keep it in the box. In VFX you typically have to be a lot more agile, but I learnt my craft at Disney and I feel like we can manage them in a similar way. We want to be successful  make good looking films and make more than one.
Cinesite will continue to work in visual effects  upcoming projects include The Man From U.N.C.L.E. and San Andreas, for example  but this work will run alongside animated features. Id love to do a feature length version of Beans, admits Butler when asked about future plans, who also notes that the studio also plans on accepting scripts and developing ideas for films.'''


   #ciphertext = encrypt(text, 10)
   ciphertext = 'aoljhlzhyjpwolypzvulvmaollhysplzaruvduhukzptwslzajpwolyzpapzhafwlvmzbizapabapvujpwolypudopjolhjoslaalypuaolwshpualeapzzopmalkhjlyahpuubtilyvmwshjlzkvduaolhswohila'

   print 'ciphertext: '
   print ciphertext
   print ''
   print 'cracked plaintext:'
   print crack(ciphertext)



if __name__ == '__main__':
   main()
