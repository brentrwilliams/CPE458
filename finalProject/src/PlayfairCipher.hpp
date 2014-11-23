#include <iostream>

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
      float bestScore;

      PlayfairCipher(const char* bestKey, float bestScore);
      ~PlayfairCipher();
      char* decrypt(char* ciphertext, const char* key);
      void simulateAnnealing();
      friend ostream &operator<<(ostream &output, const PlayfairCipher &pfc);
};