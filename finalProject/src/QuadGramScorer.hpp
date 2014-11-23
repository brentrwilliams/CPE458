#include <fstream>
#include <iostream>
#include <string>
#include <unordered_map>
#include <math.h> 

using namespace std;

#define FLOOR 0.01


class QuadGramScorer
{
   public:
      unordered_map<string, float> *ngrams;
      QuadGramScorer();
      ~QuadGramScorer();
      void loadQuadGramStatistics();
      float score(string text);
   
};