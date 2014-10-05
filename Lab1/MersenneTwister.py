# MersenneTwister.py


class MersenneTwister:
   """docstring for MersenneTwister"""
   def __init__(self, seed):
      self.index = 0
      self.MT = [0] * 624
      self.initialize_generator(seed)


   # // Initialize the generator from a seed
   # function initialize_generator(int seed) {
   #     index := 0
   #     MT[0] := seed
   #     for i from 1 to 623 { // loop over each other element
   #         MT[i] := lowest 32 bits of(1812433253 * (MT[i-1] xor (right shift by 30 bits(MT[i-1]))) + i) // 0x6c078965
   #     }
   # }

   def initialize_generator(self, seed):
      # Initialize the generator from a seed
      self.index = 0
      self.MT[0] = seed
      for i in range(1,624):
         self.MT[i] = 0xFFFFFFFF & (1812433253 * (self.MT[i-1] ^ (self.MT[i-1] >> 30)) + i) 


   #  // Extract a tempered pseudorandom number based on the index-th value,
   #  // calling generate_numbers() every 624 numbers
   #  function extract_number() {
   #      if index == 0 {
   #          generate_numbers()
   #      }
    
   #      int y := MT[index]
   #      y := y xor (right shift by 11 bits(y))
   #      y := y xor (left shift by 7 bits(y) and (2636928640)) // 0x9d2c5680
   #      y := y xor (left shift by 15 bits(y) and (4022730752)) // 0xefc60000
   #      y := y xor (right shift by 18 bits(y))

   #      index := (index + 1) mod 624
   #      return y
   #  }

   def extract_number(self):
      # Extract a tempered pseudorandom number based on the index-th value,
      # calling generate_numbers() every 624 numbers
      if self.index == 0:
         self.generate_numbers()

      y = self.MT[self.index]
      y = y ^ (y >> 11)
      y = y ^ ((y << 7) & 2636928640)
      y = y ^ ((y << 15) & 4022730752)
      y = y ^ (y >> 18)

      self.index = (self.index + 1) % 624
      return y


   # // Generate an array of 624 untempered numbers
   #  function generate_numbers() {
   #      for i from 0 to 623 {
   #          int y := (MT[i] and 0x80000000)                       // bit 31 (32nd bit) of MT[i]
   #                         + (MT[(i+1) mod 624] and 0x7fffffff)   // bits 0-30 (first 31 bits) of MT[...]
   #          MT[i] := MT[(i + 397) mod 624] xor (right shift by 1 bit(y))
   #          if (y mod 2) != 0 { // y is odd
   #              MT[i] := MT[i] xor (2567483615) // 0x9908b0df
   #          }
   #      }
   #  }

   def generate_numbers(self):
      for i in range(1,624):
         y = (self.MT[i] & 0x80000000) + (self.MT[(i+1) % 624] & 0x7fffffff)

         self.MT[i] = self.MT[(i + 397) % 624] ^ (y >> 1)

         if (y % 2) != 0: # y is odd
            self.MT[i] = self.MT[i] ^ 2567483615

def main():
   myMT = MersenneTwister(0)
   for i in range(0,5):
      print myMT.extract_number()

if __name__ == '__main__':
   main()
















