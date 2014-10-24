

def SHA1(message):
   '''
   Note 1: All variables are unsigned 32 bits and wrap modulo 2^32 when calculating, except
        ml the message length which is 64 bits, and
        hh the message digest which is 160 bits.
   Note 2: All constants in this pseudo code are in big endian.
           Within each word, the most significant byte is stored in the leftmost byte position
   '''
   sha1val = 0

   h0 = 0x67452301
   h1 = 0xEFCDAB89
   h2 = 0x98BADCFE
   h3 = 0x10325476
   h4 = 0xC3D2E1F0

   # message length in bits (always a multiple of the number of bits in a character).
   orig_message_byte_len = len(message)
   orig_message_bit_len = len(message) * 8

   # Pre-processing:
   # append the bit '1' to the message i.e. by adding 0x80 if characters are 8 bits.
   message += b'\x80'

   # append 0 ≤ k < 512 bits '0', thus the resulting message length (in bits)
   #    is congruent to 448 (mod 512)
   # append ml, in a 64-bit big-endian integer. So now the message length is a multiple of 512 bits.
   while (len(message) * 8) % 512 != 448:
      message += b'\x00'

   message += orig_message_bit_len

   for chunkInd in xrange(0, len(message), 64):
      chunk = message[chunkInd:chunkInd+64]
      words = []
      for i in xrange(0, len(chunk), 4):
         words.append(chunk[i:i+4])

      for i in xrange(16, 79):
         words[i] = xor(xor(xor(words[i - 3], words[i - 8]), words[i - 14]), words[i - 16])



   return sha1val = 0



def main():
   pass

if __name__ == '__main__':
   main()