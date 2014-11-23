
#include <iostream>
#include <stdlib.h>
#include <string.h>

#include "PlayfairCipher.hpp"
#include "QuadGramScorer.hpp"

using namespace std;

char getCharFromKey(int i, int j, const char* key)
{
   return key[i*5 + j];
}

PlayfairCipher::PlayfairCipher(const char* bestKey, float bestScore, const char* ciphertext)
{
   this->bestScore = bestScore;
   this->bestKey = new char [KEY_STR_SIZE];
   strcpy(this->bestKey, bestKey);
   this->ciphertext = new char [strlen(ciphertext)];
   strcpy(this->ciphertext, ciphertext);
}


PlayfairCipher::~PlayfairCipher()
{
   delete[] bestKey;
   delete[] ciphertext;
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
}


void PlayfairCipher::decrypt(char* ciphertext, char* plaintext, const char* key)
{
   int textLen = strlen(ciphertext);
   char oldPair[3], newPair[3];
   oldPair[2] = 0;
   newPair[2] = 0;

   for (int i = 0; i < textLen; i += 2)
   {
      oldPair[0] = ciphertext[i];
      oldPair[1] = ciphertext[i+1];
      decodeLetterPair(oldPair, newPair, key);

      plaintext[i] = newPair[0];
      plaintext[i+1] = newPair[1];
   }
}


void PlayfairCipher::simulateAnnealing()
{
   int textLen = strlen(ciphertext);
   char maxKey[KEY_SIZE];
   char* plaintext = new char[textLen];
   QuadGramScorer qgs();
   
   strcpy(maxKey,bestKey);
   plaintext = decrypt(ciphertext,maxKey);

}


ostream& operator<<(ostream &os, const PlayfairCipher &pfc)
{
    os << pfc.bestKey << ' ' << pfc.bestScore;
    return os;
}


int main(int argc, char const *argv[])
{
   if (argc != 3)
   {
      cerr << "Unexpected number of arguments: " << endl;
      cerr << "\tFound " << (argc-1) << ", epected 2" << endl;
      return 1;
   }

   const char* bestKey = argv[1];
   float bestScore = atof(argv[2]);
   char ciphertext[] = "ugrmkcsxhmufmkbtoxgcmvatluiv";

   PlayfairCipher pfc(bestKey, bestScore);
   pfc.simulateAnnealing();
   cout << pfc  << endl;


   // printKeySquare(bestKey);
   
   // char* plaintext = pfc.decrypt(ciphertext,bestKey);
   // cout << "ciphertext:\t" << ciphertext << endl;
   // cout << "decrypted:\t" << plaintext << endl << endl;

   return 0;
}