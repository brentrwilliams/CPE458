import PlayfairCipher

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


def main():
   plaintext = 'Carsten Egeberg Borchgrevink was an Anglo Norwegian polar explorer and a pioneer of modern Antarctic travel. He was the precursor of Robert Falcon Scott, Ernest Shackleton, Roald Amundsen and other more famous names associated with the Heroic Age of Antarctic Exploration. In some year, he led the British financed Southern Cross Expedition, which established a new Farthest South record'
   key = 'ZMDCFQRNOEGHIKLWXBYAUVPST'
   plaintext = preprocessText(plaintext)
   ciphertext = PlayfairCipher.encrypt(plaintext, key)
   ciphertext = preprocessText(ciphertext)
   print isPlayfair(plaintext)

if __name__ == '__main__':
   main()