import struct

def circular_shift_left(x, shift):
  return ((x << shift) | (x >> (32 - shift))) & 0xffffffff


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

   # append 0 <= k < 512 bits '0', thus the resulting message length (in bits)
   #    is congruent to 448 (mod 512)
   while (len(message) * 8) % 512 != 448:
      message += b'\x00'

   # append ml, in a 64-bit big-endian integer. So now the message length is a multiple of 512 bits.
   size_chars = struct.pack('>Q', orig_message_bit_len)
   message += size_chars
   
   # Process the message in successive 512-bit chunks:
   for chunkInd in xrange(0, len(message), 64):
      # break chunk into sixteen 32-bit big-endian words w[i], 0 <= i <= 15
      chunk = message[chunkInd:chunkInd+64]
      words = []

      for i in xrange(0, len(chunk), 4):
         words.append(struct.unpack(b'>I', chunk[i:i+4])[0])

      print len(words)
      # Extend the sixteen 32-bit words into eighty 32-bit words:
      for i in xrange(16, 80):
         words.append(circular_shift_left( words[i - 3] ^ words[i - 8] ^ words[i - 14] ^ words[i - 16], 1 ))

      # Initialize hash value for this chunk:
      a = h0
      b = h1
      c = h2
      d = h3
      e = h4
      f = 0
      g = 0
      h = 0
      k = 0

      for i in range(0, 80):
         if i >= 0 and i <= 19:
            f = (b & c) | ((~ b) & d)
            k = 0x5A827999
         elif i >= 20 and i <= 39:
            f = b ^ c ^ d
            k = 0x6ED9EBA1
         elif i >= 40 and i <= 59:
            f = (b & c) | (b & d) | (c & d) 
            k = 0x8F1BBCDC
         elif i >= 60 and i <= 79:
            f = b ^ c ^ d
            k = 0xCA62C1D6

         temp = (circular_shift_left(a, 5) + f + e + k + words[i]) & 0xffffffff
         e = d
         d = c
         c = circular_shift_left(b, 30)
         b = a
         a = temp

      h0 = (h0 + a) & 0xffffffff
      h1 = (h1 + b) & 0xffffffff 
      h2 = (h2 + c) & 0xffffffff
      h3 = (h3 + d) & 0xffffffff
      h4 = (h4 + e) & 0xffffffff
    
   # Produce the final hash value (big-endian):
   return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)


def main():
   print SHA1('abc')

if __name__ == '__main__':
   main()