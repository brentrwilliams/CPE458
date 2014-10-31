import struct
import re

def circular_shift_left(x, shift):
  return ((x << shift) | (x >> (32 - shift))) & 0xffffffff


def SHA1_orig(message):
   '''
   Note 1: All variables are unsigned 32 bits and wrap modulo 2^32 when calculating, except
        ml the message length which is 64 bits, and
        hh the message digest which is 160 bits.
   Note 2: All constants in this pseudo code are in big endian.
           Within each word, the most significant byte is stored in the leftmost byte position
   '''

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
   
   #print ('%08x %08x %08x %08x %08x' % (h0, h1, h2, h3, h4))
   #return ('%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4))
   return  int( ('0x' + ('%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4))), 16 )

def SHA1(message, h0, h1, h2, h3, h4):
   '''
   Note 1: All variables are unsigned 32 bits and wrap modulo 2^32 when calculating, except
        ml the message length which is 64 bits, and
        hh the message digest which is 160 bits.
   Note 2: All constants in this pseudo code are in big endian.
           Within each word, the most significant byte is stored in the leftmost byte position
   '''

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
   
   #print ('%08x %08x %08x %08x %08x' % (h0, h1, h2, h3, h4))
   return ('%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4))

def find_collision():
   sha1_dict = {}

   not_found = True

   i = 0
   while not_found:
      text = integer_to_char_list(i)

      sha1val = SHA1(text) & 0x3ffffffffffff
      if sha1val in sha1_dict:
         return (sha1val, text, sha1_dict[sha1val]) 

      sha1_dict[sha1val] = text

      if (i % 10000) == 0:
         print "{:,}".format(i)

      i += 1


def integer_to_char_list(num):
   text = ''
   while num > 0:
      text += chr(num & 255)
      num = num >> 8
   return text

def test_SHA1():
   print 'Testing SHA1...'

   tests = [('abc', 'a9993e364706816aba3e25717850c26c9cd0d89d'), 
            ('', 'da39a3ee5e6b4b0d3255bfef95601890afd80709'),
            ('abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq', '84983e441c3bd26ebaae4aa1f95129e5e54670f1'),
            ('abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnhijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu', 'a49b2446a02c645bf419f995b67091253a04a259'),
            ('a'*1000000, '34aa973cd4c4daa4f61eeb2bdbad27316534016f')
           ]
   i = 1
   for input_val, output_val in tests:
      out = SHA1(input_val)
      expected_out_int = int(('0x' + output_val), 16)
      if out == expected_out_int:
         print 'Passed test ' + str(i)
      else:
         print 'Failed test ' + str(i)

      i += 1

def taskIIB():
   # Collision at (28992493371179L, ';^\x94\x02', '\x98\x05e\x02')
   a = ''.join(list(bin(SHA1(';^\x94\x02')))[-50:])
   b = ''.join(list(bin(SHA1('\x98\x05e\x02')))[-50:])
   print str(list(';^\x94\x02')) + ':   ' + a
   print str(list('\x98\x05e\x02')) + ':' + b


def taskIIIA():
   input_val = raw_input('Enter url of last post: ')
   #print input_val
   # http://0.0.0.0:8080/?who=Costello&what=You%20know%20the%20fellows%27%20names?&mac=44f8b9fdca9343c6c94e0a26ca5e2192d9e5bf05
   match = re.match(r'http://0.0.0.0:8080/\?who=(.*)&what=(.*)&mac=(.*)', input_val)
   who = match.group(1)
   what = match.group(2)
   mac = match.group(3)

   # print who
   print 'what: ' + what
   # print mac
   print 'new what: ' + what.replace('%', '\\x')

   message = what
   orig_message_bit_len = (len(message) + 16) * 8
   message += b'\x80'

   while ((len(message) + 16) * 8) % 512 != 448:
      message += b'\x00'

   size_chars = struct.pack('>Q', orig_message_bit_len)
   message += size_chars

   print 'orig_message_bit_len:' + str(orig_message_bit_len)
   print 'size_chars: ' + size_chars 

   print len(message) + 16

   ourMsg = 'Dealwithit'
   #newWhat = message + r'&what=' + ourMsg
   newWhat = message + ourMsg

   #print list(message)
   print size_chars.encode('string-escape')
   print newWhat

   h0 = int(('0x' + mac[:8]), 16)
   h1 = int(('0x' + mac[8:16]), 16)
   h2 = int(('0x' + mac[16:24]), 16)
   h3 = int(('0x' + mac[24:32]), 16)
   h4 = int(('0x' + mac[32:]), 16)

   newMac = SHA1(ourMsg,h0,h1,h2,h3,h4)
   #print newMac
   newWhat = convertPercents(newWhat)
   # newWhat = newWhat.replace('\x00', r'\x00')
   # newWhat = newWhat.replace('\x80', r'\x80')
   # newWhat = newWhat.replace('\x00', r'%00')
   # newWhat = newWhat.replace('\x80', r'%80')
   newWhat = str(newWhat).replace('\x00', r'%00')



   newUrl = 'http://0.0.0.0:8080/?who=' + who + '&what=' + newWhat + '&mac=' + newMac
   print ''
   print newUrl


def hexToChars(hexStr):
   hexStr = hexStr[2:-1]
   charStr = ''
   for i in range(0,len(hexStr),2):
      ordNum = int('0x' + hexStr[i:i+2], 16)
      charStr += chr(ordNum)
   return charStr


def convertPercents(oldStr):
   newStr = ''
   i = 0
   while i < len(oldStr) - 3:
      if oldStr[i] == '%':
         ordNum = int('0x' + oldStr[i+1:i+3], 16)
         newStr += chr(ordNum)
         print '%: ' + oldStr[i:i+3] + ' => newStr: ' + newStr
         i += 3
      else:
         newStr += oldStr[i]
         print oldStr[i] + ' => newStr: ' + newStr
         i += 1
   
   print ''
   return newStr

def main():
   #taskIIB()
   #taskIIIA()
   print convertPercents('http://0.0.0.0:8080/?who=Costello&what=Funny%20names?&mac=14405ccf50915fe87bbb8f04bfbcdd5119980a06')


if __name__ == '__main__':
   main()