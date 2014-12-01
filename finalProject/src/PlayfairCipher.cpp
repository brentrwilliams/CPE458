#include "PlayfairCipher.hpp"

using namespace std;

char getCharFromKey(int i, int j, const char* key)
{
   return key[i*5 + j];
}

int keyIndex(int i, int j)
{
   return i*5 + j;
}


void printKeySquare(const char* key)
{
   for (int i = 0; i < KEY_SIZE; ++i)
   {
      cout << key[i] << " ";
      if ( (i+1) % 5 == 0 )
      {
         cout << endl;
      }
   }
}


int getIndex(char ch, const char* key)
{
   for (int i = 0; i < KEY_SIZE; i++)
   {
      if (ch == key[i])
      {
         return i;
      }
   }
   return -1;
}


void decodeLetterPair(char* oldPair, char* newPair, const char* key)
{
   int i0, i1, row0, col0, row1, col1;
   
   i0 = getIndex(oldPair[0], key);
   i1 = getIndex(oldPair[1], key);

   row0 = i0 / KEY_WIDTH;
   col0 = i0 % KEY_HEIGHT;

   row1 = i1 / KEY_WIDTH;
   col1 = i1 % KEY_HEIGHT;

   if (row0 != row1 && col0 != col1)
   {
      newPair[0] = getCharFromKey(row0,col1, key);
      newPair[1] = getCharFromKey(row1,col0, key);
   }
   else if (row0 == row1)
   {
      newPair[0] = getCharFromKey(row0, (col0+4)%5, key);
      newPair[1] = getCharFromKey(row1, (col1+4)%5, key);
   }
   else
   {
      newPair[0] = getCharFromKey((row0+4)%5, col0, key);
      newPair[1] = getCharFromKey((row1+4)%5, col1, key);
   }

   // cout << "key:" << endl;
   // printKeySquare(key);
   // cout << "oldPair: " << oldPair << endl;
   // cout << "newPair: " << newPair << endl << endl;
}

void swap2Rows(char* key)
{
   int i = rand() % 5;
   int j = rand() % 5;
   while (i == j)
   {
      j = rand() % 5;
   }

   char temp[5];

   for (int x = 0; x < 5; x++)
   {
      temp[x] = key[keyIndex(i,x)];
   }
   
   for (int x = 0; x < 5; x++)
   {
      key[keyIndex(i,x)] = key[keyIndex(j,x)];
   }

   for (int x = 0; x < 5; x++)
   {
      key[keyIndex(j,x)] = temp[x];
   }
}


void swap2Cols(char* key)
{
   int i = rand() % 5;
   int j = rand() % 5;
   while (i == j)
   {
      j = rand() % 5;
   }

   char temp[5];

   for (int x = 0; x < 5; x++)
   {
      temp[x] = key[keyIndex(x,i)];
   }
   
   for (int x = 0; x < 5; x++)
   {
      key[keyIndex(x,i)] = key[keyIndex(x,j)];
   }

   for (int x = 0; x < 5; x++)
   {
      key[keyIndex(x,j)] = temp[x];
   }
}


void swapRows(char* key)
{
   char temp[5];
   int i, j;
   i = 0;
   j = 4;
   for (int x = 0; x < 5; x++)
   {
      temp[x] = key[keyIndex(i,x)];
   }
   
   for (int x = 0; x < 5; x++)
   {
      key[keyIndex(i,x)] = key[keyIndex(j,x)];
   }

   for (int x = 0; x < 5; x++)
   {
      key[keyIndex(j,x)] = temp[x];
   }

   i = 1;
   j = 3;
   for (int x = 0; x < 5; x++)
   {
      temp[x] = key[keyIndex(i,x)];
   }
   
   for (int x = 0; x < 5; x++)
   {
      key[keyIndex(i,x)] = key[keyIndex(j,x)];
   }

   for (int x = 0; x < 5; x++)
   {
      key[keyIndex(j,x)] = temp[x];
   }
}


void swapCols(char* key)
{
   char temp[5];
   int i, j;
   i = 0;
   j = 4;
   for (int x = 0; x < 5; x++)
   {
      temp[x] = key[keyIndex(x,i)];
   }
   
   for (int x = 0; x < 5; x++)
   {
      key[keyIndex(x,i)] = key[keyIndex(x,j)];
   }

   for (int x = 0; x < 5; x++)
   {
      key[keyIndex(x,j)] = temp[x];
   }

   i = 1;
   j = 3;
   for (int x = 0; x < 5; x++)
   {
      temp[x] = key[keyIndex(x,i)];
   }
   
   for (int x = 0; x < 5; x++)
   {
      key[keyIndex(x,i)] = key[keyIndex(x,j)];
   }

   for (int x = 0; x < 5; x++)
   {
      key[keyIndex(x,j)] = temp[x];
   }
}

void reverseKey(char* key)
{
   char newKey[25];

   for (int i = 0; i < 25; ++i)
   {
      newKey[i] = key[24-i];
   }
   for (int i = 0; i < 25; ++i)
   {
      key[i] = newKey[i];
   }
}

void swapLetters(char* key)
{
   int i1 = rand() % 25;
   int i2 = rand() % 25;

   char temp = key[i1];
   key[i1] = key[i2];
   key[i2] = temp;
}


void changeKey(char* key)
{
   int i = rand() % 50;
   if (i == 0)
      swap2Rows(key);
   else if (i == 1)
      swap2Cols(key);
   else if (i == 2)
      swapRows(key);
   else if (i == 3)
      swapCols(key);
   else if (i == 4)
      reverseKey(key);
   else
      swapLetters(key);
}


PlayfairCipher::PlayfairCipher(const char* ciphertext)
{
   char* plaintext;
   this->textLength = strlen(ciphertext) + 1;
   this->ciphertext = new char[textLength];
   plaintext = new char[textLength];
   bestKey = new char[KEY_SIZE];

   strcpy(this->ciphertext, ciphertext);
   strcpy(bestKey, "ABCDEFGHIKLMNOPQRSTUVWXYZ");

   for(int i = 0; i < textLength; i++)
      this->ciphertext[i] = toupper(this->ciphertext[i]);

   decrypt(this->ciphertext, plaintext, bestKey);
   this->bestScore = scoreTextQgram(plaintext, this->textLength);
   free(plaintext);
}


PlayfairCipher::~PlayfairCipher()
{
   delete[] ciphertext;
}


void PlayfairCipher::decrypt(const char* ciphertext, char* plaintext, const char* key) const
{
   int textLen = strlen(ciphertext);
   char oldPair[3], newPair[3];
   oldPair[2] = 0;
   newPair[2] = 0;

   for (int i = 0; i < textLen; i += 2)
   {
      oldPair[0] = toupper(ciphertext[i]);
      oldPair[1] = toupper(ciphertext[i+1]);
      decodeLetterPair(oldPair, newPair, key);

      plaintext[i] = newPair[0];
      plaintext[i+1] = newPair[1];
   }
}


void PlayfairCipher::simulateAnnealing()
{
   float score, maxScore = bestScore;
   char key[KEY_SIZE];
   char maxKey[KEY_SIZE];
   char* plaintext = new char[textLength];
   strcpy(maxKey, bestKey);

   for (float t = TEMP; t >= 0; t -= STEP)
   {
      for (int c = 0; c < COUNT; c++)
      {
         strcpy(key, maxKey);
         changeKey(key);

         decrypt(ciphertext, plaintext, key);
         score = scoreTextQgram(plaintext, textLength);
         float scoreDiff = score - maxScore;
         if (scoreDiff >= 0)
         {
            maxScore = score;
            strcpy(maxKey, key);
         }
         else if (t > 0)
         {
            float prob = exp(scoreDiff / t);
            //cout << prob << endl;
            if (prob > (1.0 * rand() / RAND_MAX))
            {
               maxScore = score;
               strcpy(maxKey, key);
            }
         }

         if (maxScore > bestScore)
         {
            bestScore = maxScore;
            strcpy(bestKey, maxKey);
         }
      }
   }
}


void PlayfairCipher::outputState()
{
   cerr << "key: " << bestKey << endl; 
   char* plaintext = new char[textLength];
   decrypt(ciphertext, plaintext, bestKey);
   cerr << "Plaintext:\n" << plaintext << endl;
   delete[] plaintext;
}

void PlayfairCipher::outputBestPlaintext()
{
   char* plaintext = new char[textLength];
   decrypt(ciphertext, plaintext, bestKey);
   cout << plaintext;
}


int main(int argc, char const *argv[])
{
   

   if (argc < 3)
   {
      cerr << "\nERROR: Invalid number of arguments: Found " << argc-1 << ", expected 2 (or 3)." << endl;
      cerr << "\t" << argv[0] << " CIPHERTEXT NUM_ROUNDS [v]" << endl;
      return 1;
   }

   int verbose = 0;
   if (argc >= 4)
   {
      verbose = 1;
   }

   const char* ciphertext = argv[1];
   // "XZOGQRWVQWNROKCOAELBXZWGEQYLGDRZXYZRQAEKLRHDUMNUXYXSXYEMXEHDGNXZYNTZONYELBEUGYSCOREUSWTZRLRYBYCOLZYLEMWNSXFBUSDBORBZCYLQEDMHQRWVQWAEDPGDPOYHORXZINNYWPXZGROKCOLCCOCYTZUEUIICERLEVHMVQWLNWPRYXHGNMLEKLRHDUYSUCYRAWPUYECRYRYXHGNBLUYSCCOUYOHRYUMNUXYXSXYEMXEHDGN";
   int maxUnchangedRounds = atoi(argv[2]);

   int i = 1;
   int lastChangedRound = i;
   float bestScore;
   PlayfairCipher pfc(ciphertext);
   bestScore = pfc.bestScore;


   while(i - lastChangedRound < maxUnchangedRounds)
   {
      pfc.simulateAnnealing();
      if (pfc.bestScore > bestScore)
      {
         if (verbose)
         {
            cerr << "Round " << i << ":" << pfc.bestScore << endl << endl;
            pfc.outputState();
            cerr << endl << endl;
         }

         bestScore = pfc.bestScore;
         lastChangedRound = i;
      }
      i++;
   }

   pfc.outputBestPlaintext();

   return 0;
}