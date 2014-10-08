def extract_number(y):
   # Extract a tempered pseudorandom number based on the index-th value,
   # calling generate_numbers() every 624 numbers
   print bin(y)
   y = y ^ (y >> 11)
   print bin(y)
   y = y ^ ((y << 7) & 2636928640)
   print bin(y)
   y = y ^ ((y << 15) & 4022730752)
   print bin(y)
   y = y ^ (y >> 18)
   print bin(y)
   print "==========="
   return y

def unmix(y):
   magicNumA = 2636928640
   print bin(y)
   y = y ^ (y >> 18)
   print bin(y)
   y = y ^ ((y << 15) & 4022730752)
   print bin(y)

   a = y << 7;
   b = y ^ (a & magicNumA)
   c = b << 7
   d = y ^ (c & magicNumA) # now we have 14 of the original
   e = d << 7
   f = y ^ (e & magicNumA) # now we have 21 of the original
   g = f << 7
   h = y ^ (g & magicNumA) # now we have 28 of the original
   i = h << 7
   y = y ^ (i & magicNumA)
   print bin(y)
   a = y ^ (y >> 11)
   b = y ^ (a >> 11)
   y = y ^ (b >> 11) 
   print bin(y)
   return y

def main():
   print unmix(extract_number(2636928640))

if __name__ == '__main__':
   main()
