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
   print bin(y)
   y = y ^ (y >> 18)
   print bin(y)
   y = y ^ ((y >> 15 << 15) & 4022730752)
   print bin(y)
   y = y ^ (y  >> 7 << 7) & 2636928640)
   print bin(y)
   y = y ^ (y >> 11)
   print bin(y)
   return y

def main():
   print unmix(extract_number(456))

if __name__ == '__main__':
   main()
