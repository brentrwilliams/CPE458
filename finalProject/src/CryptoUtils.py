

class IOC(object):
   '''docstring for IOC'''
   def __init__(self, text):
      super(IOC, self).__init__()

      self.expected_letter_frequencies = {'a':0.08167, 'b':0.01492, 'c':0.02782, 'd':0.04253, 'e':0.12702, 'f':0.02228, 'g':0.02015, 'h':0.06094, 'i':0.06966, 'j':0.00153, 'k':0.00772, 'l':0.04025, 'm':0.02406, 'n':0.06749, 'o':0.07507, 'p':0.01929, 'q':0.00095, 'r':0.05987, 's':0.06327, 't':0.09056, 'u':0.02758, 'v':0.00978, 'w':0.02360, 'x':0.00150, 'y':0.01974, 'z':0.00074,} # taken from wikipedia
      self.letter_frequencies = {}
      self.num_letters = 0
      
      self.update(text)


   def update(self, text):
      letter_sums = {'a':0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0, 'g':0, 'h':0, 'i':0, 'j':0, 'k':0, 'l':0, 'm':0, 'n':0, 'o':0, 'p':0, 'q':0, 'r':0, 's':0, 't':0, 'u':0, 'v':0, 'w':0, 'x':0, 'y':0, 'z':0,}

      self.num_letters = 0
      for char in text.lower():
         if char.isalpha():
            letter_sums[char] += 1
            self.num_letters += 1

      for char in letter_sums.keys():
         self.letter_frequencies[char] = float(letter_sums[char]) / self.num_letters

   def __getitem__(self, index):
      return self.letter_frequencies[index]

   def __repr__(self):
      return str(self.letter_frequencies)

   def within_percent(self,percent):
      '''
      Returns the percentage of the letter frequencies that are within a given percentage (percent) of what is expected of english's letter frequencies
      '''
      within = 0
      for char in self.expected_letter_frequencies.keys():
         expected = self.expected_letter_frequencies[char]
         given = self.letter_frequencies[char]
         if (given < expected + expected * percent) and (given > expected - expected * percent):
            within += 1

      return within / 26.0

def main():
   text = '''Most of the production will take place in Montreal, where the studio is currently ramping up its feature animation team to work on Charming and subsequent productions. These first films will allow us to build infrastructure, a team, pipeline and so on, says Butler. It will help us make the feature animation studio we want to be. At the same time, were also going to start to go out and develop our own scripts for our movies. And theyll be ones we own more of going forward.
          In terms of animation style, Butler plans to maintain a visual effects quality to the work. Were very ambitious about the quality, he says. I want to capitalize on the high production values we instituted on Beans and then keep it in the box. In VFX you typically have to be a lot more agile, but I learnt my craft at Disney and I feel like we can manage them in a similar way. We want to be successful  make good looking films and make more than one.
          Cinesite will continue to work in visual effects  upcoming projects include The Man From U.N.C.L.E. and San Andreas, for example  but this work will run alongside animated features. Id love to do a feature length version of Beans, admits Butler when asked about future plans, who also notes that the studio also plans on accepting scripts and developing ideas for films.'''

   print len(text)
   ioc = IOC(text)
   print ioc
   print ioc.within_percent(0.333) > .5

if __name__ == '__main__':
   main()
      