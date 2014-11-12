#include <stdio.h>
#include <stdlib.h>  
#include <string.h>
#include <stdint.h>
#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>

#define BLOCKSIZE 4096
#define BLOCKSIZE_NOADMIN 4032
#define MAX_DISKS 100
#define ITERATIONS 1024
#define DISKKEY_HASH_SIZE 32

/*Found at openssl wiki*/
int encrypt(unsigned char *plaintext, int plaintext_len, unsigned char *key,
  unsigned char *iv, unsigned char *ciphertext)
{
  EVP_CIPHER_CTX *ctx;

  int len;

  int ciphertext_len;

  /* Create and initialise the context */
  if(!(ctx = EVP_CIPHER_CTX_new())) handleErrors();

  /* Initialise the encryption operation. IMPORTANT - ensure you use a key
   * and IV size appropriate for your cipher
   * In this example we are using 256 bit AES (i.e. a 256 bit key). The
   * IV size for *most* modes is the same as the block size. For AES this
   * is 128 bits */
  if(1 != EVP_EncryptInit_ex(ctx, EVP_aes_256_xts(), NULL, key, iv))
    handleErrors();

  /* Provide the message to be encrypted, and obtain the encrypted output.
   * EVP_EncryptUpdate can be called multiple times if necessary
   */
  if(1 != EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintext_len))
    handleErrors();
  ciphertext_len = len;

  /* Finalise the encryption. Further ciphertext bytes may be written at
   * this stage.
   */
  if(1 != EVP_EncryptFinal_ex(ctx, ciphertext + len, &len)) handleErrors();
  ciphertext_len += len;

  /* Clean up */
  EVP_CIPHER_CTX_free(ctx);

  return ciphertext_len;
}

/*Found at openssl wiki*/
int decrypt(unsigned char *ciphertext, int ciphertext_len, unsigned char *key,
  unsigned char *iv, unsigned char *plaintext)
{
  EVP_CIPHER_CTX *ctx;

    int len;

  int plaintext_len;

  /* Create and initialise the context */
  if(!(ctx = EVP_CIPHER_CTX_new())) handleErrors();

  /* Initialise the decryption operation. IMPORTANT - ensure you use a key
   * and IV size appropriate for your cipher
   * In this example we are using 256 bit AES (i.e. a 256 bit key). The
   * IV size for *most* modes is the same as the block size. For AES this
   * is 128 bits */
  if(1 != EVP_DecryptInit_ex(ctx, EVP_aes_256_xts(), NULL, key, iv))
    handleErrors();

  /* Provide the message to be decrypted, and obtain the plaintext output.
   * EVP_DecryptUpdate can be called multiple times if necessary
   */
  if(1 != EVP_DecryptUpdate(ctx, plaintext, &len, ciphertext, ciphertext_len))
    handleErrors();
  plaintext_len = len;

  /* Finalise the decryption. Further plaintext bytes may be written at
   * this stage.
   */
  if(1 != EVP_DecryptFinal_ex(ctx, plaintext + len, &len)) handleErrors();
  plaintext_len += len;

  /* Clean up */
  EVP_CIPHER_CTX_free(ctx);

  return plaintext_len;
}

char* disks[MAX_DISKS];
int numDisks = 0;

int hasDisk(char *filename) {
   int i = 0;
   for (i = 0; i < numDisks; i++) {
      if (strcmp(filename, disks[i]) == 0) {
         return i;
      }
   }
   return -1;
}

/* This function opens a regular file and designates the first nBytes 
of it as space for the emulated disk. nBytes should be an integral number 
of the block size. If nBytes > 0 and there is already a file by the given 
filename, that file’s content may be overwritten. If nBytes is 0, an existing 
disk is opened, and should not be overwritten. There is no requirement to 
maintain integrity of any file content beyond nBytes. The return value is -1 
on failure or a disk number on success. 
*/
int mountDisk(char * filename, int nBytes) {
   FILE *fp, *randFp;
   char *randStuff;
   char *randUserStuff;
   char *diskKey;
   char *diskKeyHash;
   char *adminSector;
   char *adminCipher;
   char *adminKey;
   unsigned char *salt = "264722680";
   uint64_t numUsers = 1;
   char *adminpsswd = "admin";
   char *adminIV;

   if (nBytes % BLOCKSIZE != 0) {
      return -1;
   }

   if (nBytes > 0) {
      randFp = fopen("/dev/urandom", "r");
      
      //random values for rest of user header block
      randUserStuff = (char *) malloc(sizeof(char) * BLOCKSIZE_NOADMIN);
      fread(randUserStuff, 1, BLOCKSIZE_NOADMIN, randFp);

      //random values for rest of disk space
      randStuff = (char *) malloc(sizeof(char) * (nBytes - BLOCKSIZE));
      fread(randStuff, 1, nBytes - BLOCKSIZE, randFp);
      
      //Get the key for the disk
      diskKey = (char *) malloc(sizeof(char) * 64);
      fread(diskKey, 1, 16, randFp);

      fclose(randFp);

      //create hash of the disk key
      diskKeyHash = (char *) malloc(sizeof(char) * DISKKEY_HASH_SIZE);
      PKCS5_PBKDF2_HMAC(diskKey, 64, salt, strlen(salt), ITERATIONS, EVP_sha512(), DISKKEY_HASH_SIZE, diskKeyHash);

      //Concatenate the disk key with the number of users to get the admin sector.
      adminSector = (char *) malloc(sizeof(char) * 72);
      memcpy(diskKey, adminSector, 64);
      memcpy(&numUsers, adminSector + 64, sizeof(uint64_t));

      //Create a key for the admin in this disk.
      adminKey = (char *) malloc(sizeof(char) * 64);
      PKCS5_PBKDF2_HMAC(adminpsswd, strlen(adminpsswd), salt, strlen(salt), ITERATIONS, EVP_sha512(), 64, adminKey); 

      //Create the admin cipher for the sector.
      adminCipher = (char *) malloc(sizeof(char) * 80);
      adminIV = (char *) calloc(16, sizeof(char));
      encrypt(adminSector, 72, adminKey, adminIV, adminCipher);

      //Write header and random values to the disk.
      fp = fopen(filename, "w+");
      fwrite(diskKeyHash, 1, DISKKEY_HASH_SIZE, fp);
      fwrite(adminCipher, 1, 80, fp);
      fwrite(randUserStuff, 1, BLOCKSIZE_NOADMIN, fp);
      fwrite(randStuff, 1, nBytes - BLOCKSIZE, fp);
      fclose(fp);

      //Claim the disk as "open"
      if (hasDisk(filename) == -1) {
         disks[numDisks] = filename;
         numDisks++;
         return numDisks - 1;
      }

      return -1;
   }
   else if (nBytes == 0) {
      return hasDisk(filename);
   }


}

/* This function unmounts the open disk (identified by ‘disk’). */
int unmountDisk(int disk) {
   disks[disk] = 0;
}

int verifyUser(char *uname, char *password, int disk) {
   FILE *fp;
   char *diskKeyHash;
   char *userBuffer;
   char *possPlaintext = malloc(sizeof(char) * 80);
   char *possDiskKeyHash = malloc(sizeof(char) * DISKKEY_HASH_SIZE);
   int i, j, verified = 1;
   char *userKey;
   char *iv = malloc(sizeof(char) * 16);
   uint64_t blockNum, byteNum;
   unsigned char *salt = "264722680";

   //Create a key for the user in this disk.
   userKey = (char *) malloc(sizeof(char) * 64);
   PKCS5_PBKDF2_HMAC(password, strlen(password), salt, strlen(salt), ITERATIONS, EVP_sha512(), 64, userKey);   

   fp = fopen(disks[disk], "r");

   diskKeyHash = (char *) malloc(sizeof(char) * DISKKEY_HASH_SIZE);
   fread(diskKeyHash, 1, DISKKEY_HASH_SIZE, fp);

   userBuffer = (char *) malloc(sizeof(char) * 80);

   fread(userBuffer, 1, 80, fp);

   if(strcmp(uname, "admin") == 0) {

   }
   else {
      for(i = 0; i < 49, i++) {
         blockNum = i + 1;
         byteNum = blockNum * 80;

         memcpy(iv, &blockNum);
         memcpy(iv + 8, &byteNum);

         fread(userBuffer, 1, 80, fp);
         decrypt(userBuffer, 80, userKey, iv, possPlaintext);

         
         PKCS5_PBKDF2_HMAC(possPlaintext, 64, salt, strlen(salt), ITERATIONS, EVP_sha512(), DISKKEY_HASH_SIZE, possDiskKeyHash);

         for(j = 0; j < 32; j++) {
            verified = verified && possDiskKeyHash[j] == diskKeyHash[j]);
         }

         verified = verified && (strcmp(possPlaintext + 64, uname) == 0);

         if(verified) {
            return verified;
         }

      }

      return 0;
   }


}

/* readBlock() re16, ads an entirck of BLOCKSIZE bytes from the open disk
 (identified by ‘disk’) and copies the result into a local buffer, block 
 (which must be at least of BLOCKSIZE bytes). The bNum is a logical block number,
  which must be translated into a byte offset within the disk. The translation from
 logical to physical block is straightforward: bNum=0 is the very first byte of the
 file. bNum=1 is BLOCKSIZE bytes into the disk, bNum=n is n*BLOCKSIZE bytes into
 the disk. On success, it returns 0. -1 or smaller is returned if disk is not available
 (hasn’t been opened) or any other failures. readBlock will also perform the decryption
 operation. You should define your own error code system. 
*/
int readBlock(int disk, int bNum, void *block, char * uname, char * password) {

   return 0;
}

/* writeBlock() takes disk number ‘disk’ and logical block number ‘bNum’ and encrypts
 and then writes the content of the buffer ‘block’ to that location. ‘block’ must be 
 integral with BLOCKSIZE. Just as in readBlock(), writeBlock() must translate the logical 
 block bNum to the correct byte position in the file. On success, it returns 0. -1 or smaller 
 is returned if disk is not available (i.e. hasn’t been opened) or any other failures. You should 
 define your own error code system. 
*/
int writeBlock(int disk, int bNum, void *block, char * uname, char * password) {


   

}