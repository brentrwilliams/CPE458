#include <iostream>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>
#include "scoreText.h"

#include "QuadGramScorer.hpp"

#define KEY_STR_SIZE 26
#define KEY_SIZE 25
#define KEY_WIDTH 5
#define KEY_HEIGHT 5
#define TEMP 20
#define STEP 0.2
#define COUNT 1000

using namespace std;

class PlayfairCipher
{
   public:
      char* bestKey;
      char* ciphertext;
      float bestScore;
      int textLength;
      QuadGramScorer* qgs;

      PlayfairCipher(const char* ciphertext);
      ~PlayfairCipher();
      void decrypt(const char* ciphertext, char* plaintext, const char* key) const;
      void simulateAnnealing();
      void outputState();
};