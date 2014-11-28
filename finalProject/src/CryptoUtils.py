from math import log10

def char_to_index(char):
   return ord(char.lower()) - ord('a')

def index_to_char(index):
   alphabet = "abcdefghijklmnopqrstuvwxyz"
   return alphabet[index % 26]

class LetterFrequencies(object):
   '''docstring for LetterFrequencies'''
   def __init__(self, text):
      super(LetterFrequencies, self).__init__()

      self.expected_letter_frequency_percentages = {'a':0.08167, 'b':0.01492, 'c':0.02782, 'd':0.04253, 'e':0.12702, 'f':0.02228, 'g':0.02015, 'h':0.06094, 'i':0.06966, 'j':0.00153, 'k':0.00772, 'l':0.04025, 'm':0.02406, 'n':0.06749, 'o':0.07507, 'p':0.01929, 'q':0.00095, 'r':0.05987, 's':0.06327, 't':0.09056, 'u':0.02758, 'v':0.00978, 'w':0.02360, 'x':0.00150, 'y':0.01974, 'z':0.00074,} # taken from wikipedia
      self.letter_frequencies = {'a':0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0, 'g':0, 'h':0, 'i':0, 'j':0, 'k':0, 'l':0, 'm':0, 'n':0, 'o':0, 'p':0, 'q':0, 'r':0, 's':0, 't':0, 'u':0, 'v':0, 'w':0, 'x':0, 'y':0, 'z':0,}
      self.letter_frequency_percentages = {}
      self.num_letters = 0
      
      self.update(text)


   def update(self, text):
      self.letter_frequencies = {'a':0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0, 'g':0, 'h':0, 'i':0, 'j':0, 'k':0, 'l':0, 'm':0, 'n':0, 'o':0, 'p':0, 'q':0, 'r':0, 's':0, 't':0, 'u':0, 'v':0, 'w':0, 'x':0, 'y':0, 'z':0,}

      self.num_letters = 0
      for char in text.lower():
         if char.isalpha():
            self.letter_frequencies[char] += 1
            self.num_letters += 1

      for char in self.letter_frequencies.keys():
         self.letter_frequency_percentages[char] = float(self.letter_frequencies[char]) / self.num_letters

   def __getitem__(self, index):
      return self.letter_frequencies[index]

   def __repr__(self):
      return str(self.letter_frequency_percentages)

   def chi_squared(self):
      '''
      This method measures how close the given letter frequency probability distribution is to english's letter frequency probability distribution using the Chi-squared Statistic. The Chi-squared Statistic is a measure of how similar two categorical probability distributions are. If the two distributions are identical, the chi-squared statistic is 0, if the distributions are very different, some higher number will result. 
      '''
      chi_squared_val = 0
      for char in self.letter_frequencies.keys():
         expected = self.expected_letter_frequency_percentages[char] * self.num_letters
         actual = self.letter_frequencies[char]

         chi_squared_val += ((actual - expected) * (actual - expected)) / expected

      return chi_squared_val
      

def index_of_coincidence(text):
   #print "'" + text + "'"
   letter_freqs = LetterFrequencies(text)
   alphabet = "abcdefghijklmnopqrstuvwxyz"
   sum_val = 0.0
   for char in alphabet:
      freq = letter_freqs[char]
      sum_val += freq * (freq - 1)

   N = letter_freqs.num_letters

   if N == 1:
      return sum_val

   return sum_val / (N * (N - 1))



class NGramScorer(object):
   """
   Fitness measuring using the log10 average of english that uses each ngram
   """
   def __init__(self, n):
      super(NGramScorer, self).__init__()
      self.ngrams = {}
      self.floor = 0.01
      self.n = n
      self.loadNGramStatistics()
   
   def loadNGramStatistics(self):
      file_name = ''
      if self.n == 1:
         file_name = 'english_monograms.txt'
      elif self.n == 2:
         file_name = 'english_bigrams.txt'
      elif self.n == 3:
         file_name = 'english_trigrams.txt'
      else:
         file_name = 'english_quadgrams.txt'
         self.n = 4
      
      with open(file_name) as f:
         count = 0
         for line in f:
            line = line.strip()
            ngram, part, num = line.partition(' ')
            num = int(num)
            ngram = ngram.lower()
            self.ngrams[ngram] = num
            count += num

         for key in self.ngrams.keys():
            self.ngrams[key] = log10(float(self.ngrams[key])/count)

         self.floor /= count

   def score(self,text):
      '''
      Higher score means closer to English
      '''
      score = 0.0

      for i in range(0,len(text)-self.n+1):
         ngram = text[i:i+self.n]
         #print ngram
         if ngram in self.ngrams:
            #print "yes!"
            score += self.ngrams[ngram] 
         else:
            score += self.floor
      return score


def main():
   # ct = 'aoljhlzhyjpwolypzvulvmaollhysplzaruvduhukzptwslzajpwolyzpapzhafwlvmzbizapabapvujpwolypudopjolhjoslaalypuaolwshpualeapzzopmalkhjlyahpuubtilyvmwshjlzkvduaolhswohila'
   # lf = LetterFrequencies(ct)
   # print lf.letter_frequencies
   # print lf.chi_squared()
   qgs = NGramScorer(4)
   print qgs.score('ATSKVLXPPBVESHESUIBKATASLNFESZITUTTIMBLORESTANEOUTWHUTINURSTOMATNEYFYENUBKUOOZDWHEUODSYFERETUFESIFFEINUPHWQKWOFWHEAFEDBLCYVGVLXPPBUIPCSZNSTOHEATEMENSCATHISHESRIESEDYFOUAELICERCRTQNPBEQSCETHTOMQILORESTONOWEDIXSCONCIETETHTOMKBONDWESONSOETANEOUTWHUTINURSTOM'.lower())


if __name__ == '__main__':
   main()
      