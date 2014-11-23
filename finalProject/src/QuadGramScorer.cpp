#include "QuadGramScorer.hpp"

QuadGramScorer::QuadGramScorer()
{
   ngrams = new unordered_map<string, float>();
   loadQuadGramStatistics();
}


QuadGramScorer::~QuadGramScorer()
{
}


void QuadGramScorer::loadQuadGramStatistics()
{
   ifstream myfile ("english_quadgrams.txt");
   if (!myfile)
   {
      cerr << "Error opening file" << endl;
      exit(1);
   }
   
   long count = 0;
   while (myfile)
   {
      std::string quadGram;
      myfile >> quadGram;
      std::transform(quadGram.begin(), quadGram.end(), quadGram.begin(), ::tolower);

      std::string numStr;
      myfile >> numStr;
      int num = atoi(numStr.c_str());

      (*ngrams)[quadGram] = (float) num;

      count += num;
   }

   for(unordered_map<string, float>::iterator it = ngrams->begin(); it != ngrams->end(); ++it )
   {
      (*ngrams)[it->first] = (float) log10((*ngrams)[it->first]/((float)count));
   }
}


float QuadGramScorer::score(string text)
{
   float score = 0.0f;
   std::transform(text.begin(), text.end(), text.begin(), ::tolower);
   for (int i = 0; i < text.length()-3; ++i)
   {
      string quadGram = text.substr(i, 4);
      if (ngrams->find(quadGram) != ngrams->end())
      {
         score += (*ngrams)[quadGram];
         cout << quadGram << ": " << (*ngrams)[quadGram] << endl;
      }
      else
      {
         score += FLOOR;
      }
   }
   return score;
}


int main(int argc, char const *argv[])
{
   QuadGramScorer qgs;

   string text = "ATTACKTHEEASTWALLOFTHECASTLEATDAWN";
   cout << qgs.score(text) << endl;

   return 0;
}