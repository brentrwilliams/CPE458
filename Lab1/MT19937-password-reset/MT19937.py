
#Mersenne Twister MT 19937
class MT19937:
   def __init__(self, seed):
      self.index = 0
      self.MT = [0] * 624
      
      # Initialize the generator from a seed
      self.MT[0] = seed
      for i in range(1,624):
         self.MT[i] = 0xFFFFFFFF & (1812433253 * (self.MT[i-1] ^ (self.MT[i-1] >> 30)) + i) 

   def extract_number(self):
      # Extract a tempered pseudorandom number based on the index-th value,
      # calling generate_numbers() every 624 numbers
      if self.index == 0:
         self.generate_number()

      y = self.MT[self.index]
      y = y ^ (y >> 11)
      y = y ^ ((y << 7) & 2636928640)
      y = y ^ ((y << 15) & 4022730752)
      y = y ^ (y >> 18)

      self.index = (self.index + 1) % 624
      return y

   def unmix(self):
      y = self.MT[self.index]
      y = y ^ (y >> 18)
      y = y ^ ((y << 15) & 4022730752)
      y = y ^ ((y << 7) & 2636928640)
      y = y ^ (y >> 11)

      return y


   def generate_numbers(self):
      for i in range(1,624):
         y = (self.MT[i] & 0x80000000) + (self.MT[(i+1) % 624] & 0x7fffffff)

         self.MT[i] = self.MT[(i + 397) % 624] ^ (y >> 1)

         if (y % 2) != 0: # y is odd
            self.MT[i] = self.MT[i] ^ 2567483615

