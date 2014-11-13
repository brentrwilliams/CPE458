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
#define KEY_BYTE_LEN 64
#define IV_BYTE_LEN 16
#define USER_SECTOR_BYTE_LEN 80
#define MAX_USERS 49

void handleErrors(void)
{
  ERR_print_errors_fp(stderr);
  abort();
}

void printHex(char * text, int size) {
   int i;

   for(i = 0; i < size; i++) {
      printf("%02x", 255 & text[i]);
   }

   printf("\n");
}

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

char* disks[MAX_DISKS] = {0};
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

int hasDiskNum(int disk) {
   if(disk > MAX_DISKS) {
      return -1;
   }
   else if(disks[disk] == NULL) {
      return -1;
   }
   else {
      return 1;
   }
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
   uint64_t filler = 0;
   uint64_t numUsers = 1;
   char *adminpsswd = "admin";
   char *adminIV = calloc(IV_BYTE_LEN, sizeof(char));
   int size;

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
      diskKey = (char *) malloc(sizeof(char) * KEY_BYTE_LEN);
      fread(diskKey, 1, KEY_BYTE_LEN, randFp);
      //printf("disk key generated: ");
      //printHex(diskKey, KEY_BYTE_LEN);

      fclose(randFp);

      //create hash of the disk key
      diskKeyHash = (char *) malloc(sizeof(char) * DISKKEY_HASH_SIZE);
      PKCS5_PBKDF2_HMAC(diskKey, KEY_BYTE_LEN, salt, strlen(salt), ITERATIONS, EVP_sha512(), DISKKEY_HASH_SIZE, diskKeyHash);
      //printf("disk key hash generated: ");
      //printHex(diskKeyHash, DISKKEY_HASH_SIZE);

      //Concatenate the disk key with the number of users to get the admin sector.
      adminSector = (char *) malloc(sizeof(char) * USER_SECTOR_BYTE_LEN);
      memcpy(adminSector, diskKey, KEY_BYTE_LEN);
      memcpy(adminSector + KEY_BYTE_LEN, &filler, sizeof(uint64_t));
      memcpy(adminSector + KEY_BYTE_LEN + 8, &numUsers, sizeof(uint64_t));

      //printf("disk key in admin sector: ");
      //printHex(adminSector, KEY_BYTE_LEN);

      //Create a key for the admin in this disk.
      adminKey = (char *) malloc(sizeof(char) * KEY_BYTE_LEN);
      PKCS5_PBKDF2_HMAC(adminpsswd, strlen(adminpsswd), salt, strlen(salt), ITERATIONS, EVP_sha512(), KEY_BYTE_LEN, adminKey); 

      //printf("admin key: ");
      //printHex(adminKey, KEY_BYTE_LEN);

      //Create the admin cipher for the sector.
      adminCipher = (char *) malloc(sizeof(char) * USER_SECTOR_BYTE_LEN);
      //adminIV = (char *) calloc(IV_BYTE_LEN, sizeof(char));
      size = encrypt(adminSector, USER_SECTOR_BYTE_LEN, adminKey, adminIV, adminCipher);

      printf("size: %d\n", size);

      decrypt(adminCipher, USER_SECTOR_BYTE_LEN, adminKey, adminIV, adminSector);

      //printf("key after decryption: ");
      //printHex(adminSector, KEY_BYTE_LEN);

      //Write header and random values to the disk.
      fp = fopen(filename, "w+");
      fwrite(diskKeyHash, 1, DISKKEY_HASH_SIZE, fp);
      fwrite(adminCipher, 1, USER_SECTOR_BYTE_LEN, fp);
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
   disks[disk] = NULL;
}

int verifyUser(char *uname, char *password, int disk, char *returnDiskKey) {
   FILE *fp;
   char *diskKeyHash;
   char *userBuffer;
   char *possPlaintext = malloc(sizeof(char) * USER_SECTOR_BYTE_LEN);
   char *possDiskKeyHash = malloc(sizeof(char) * DISKKEY_HASH_SIZE);
   int i, j, verified = 1;
   char *userKey;
   uint64_t *numUsers;
   char *iv = calloc(IV_BYTE_LEN, sizeof(char));
   uint64_t blockNum, byteNum;
   unsigned char *salt = "264722680";

   //Create a key for the user in this disk.
   userKey = (char *) malloc(sizeof(char) * KEY_BYTE_LEN);
   PKCS5_PBKDF2_HMAC(password, strlen(password), salt, strlen(salt), ITERATIONS, EVP_sha512(), KEY_BYTE_LEN, userKey);   

   //printf("userKey: ");
   //printHex(userKey, KEY_BYTE_LEN);

   fp = fopen(disks[disk], "r");

   diskKeyHash = (char *) malloc(sizeof(char) * DISKKEY_HASH_SIZE);
   fread(diskKeyHash, 1, DISKKEY_HASH_SIZE, fp);
   //printf("disk key hash from file: ");
   //printHex(diskKeyHash, DISKKEY_HASH_SIZE);


   userBuffer = (char *) malloc(sizeof(char) * USER_SECTOR_BYTE_LEN);

   fread(userBuffer, 1, USER_SECTOR_BYTE_LEN, fp);

   if(strcmp(uname, "admin") == 0) {
      decrypt(userBuffer, USER_SECTOR_BYTE_LEN, userKey, iv, possPlaintext);
      //printf("disk key from admin plain text: ");
      //printHex(possPlaintext, KEY_BYTE_LEN);

      PKCS5_PBKDF2_HMAC(possPlaintext, KEY_BYTE_LEN, salt, strlen(salt), ITERATIONS, EVP_sha512(), DISKKEY_HASH_SIZE, possDiskKeyHash);
      
      //printf("disk key hash from given disk key in admin text: ");
      //printHex(possDiskKeyHash, DISKKEY_HASH_SIZE);

      
      numUsers = (uint64_t *) (possPlaintext + KEY_BYTE_LEN + 8);
      printf("num users: %ld\n", *numUsers);
      //printHex(, 8);

      for(j = 0; j < DISKKEY_HASH_SIZE; j++) {
            verified = verified && (possDiskKeyHash[j] == diskKeyHash[j]);
            //printf("cur verified: %d\n", verified);
      }

      if(returnDiskKey != NULL) {
         memcpy(returnDiskKey, possPlaintext, KEY_BYTE_LEN);
      }
      fclose(fp);
      return verified; 

   }
   else {
      for(i = 0; i < MAX_USERS; i++) {
         verified = 1;
         blockNum = i + 1;
         byteNum = blockNum * USER_SECTOR_BYTE_LEN;

         memcpy(iv, &blockNum, (IV_BYTE_LEN)/2);
         memcpy(iv + (IV_BYTE_LEN/2), &byteNum, (IV_BYTE_LEN)/2);

         fread(userBuffer, 1, USER_SECTOR_BYTE_LEN, fp);
         decrypt(userBuffer, USER_SECTOR_BYTE_LEN  , userKey, iv, possPlaintext);
         
         PKCS5_PBKDF2_HMAC(possPlaintext, KEY_BYTE_LEN, salt, strlen(salt), ITERATIONS, EVP_sha512(), DISKKEY_HASH_SIZE, possDiskKeyHash);

         /*printf("actual key: ");
         printHex(diskKeyHash, DISKKEY_HASH_SIZE);
         printf("possib key: ");
         printHex(possDiskKeyHash, DISKKEY_HASH_SIZE);
         printf("\n");*/

         for(j = 0; j < DISKKEY_HASH_SIZE; j++) {
            verified = verified && (possDiskKeyHash[j] == diskKeyHash[j]);
            //printf("verified: %d\n", verified);
         }

         //verified = verified && (strcmp(possPlaintext + KEY_BYTE_LEN, uname) == 0);

         if(verified) {
            if(returnDiskKey != NULL) {
               memcpy(returnDiskKey, possPlaintext, KEY_BYTE_LEN);
            }
            fclose(fp);
            return verified;
         }

      }

      fclose(fp);
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
   char *key = (char *) malloc(sizeof(char) * KEY_BYTE_LEN);
   char *cipherBlock = (char *) malloc(sizeof(char) * BLOCKSIZE);
   long diskSize;
   FILE *fp;
   uint64_t blockNum;
   uint64_t byteNum;
   char *iv = (char *) malloc(sizeof(char) * IV_BYTE_LEN);

   if(!verifyUser(uname, password, disk, key)) {
      return -1;
   }

   if(!hasDiskNum(disk)) {
      return -1;
   }

   fp = fopen(disks[disk], "r");
   fseek(fp, 0L, SEEK_END);
   diskSize = ftell(fp);

   if(bNum * BLOCKSIZE > diskSize) {
      return -1;
   }

   blockNum = bNum;
   byteNum = blockNum * BLOCKSIZE;

   memcpy(iv, &blockNum, sizeof(uint64_t));
   memcpy(iv + 8, &byteNum, sizeof(uint64_t));

   fseek(fp, byteNum + BLOCKSIZE, SEEK_SET);
   fread(cipherBlock, 1, BLOCKSIZE, fp);

   decrypt(cipherBlock, BLOCKSIZE, key, iv, block);

   fclose(fp);
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
   char *key = (char *) malloc(sizeof(char) * KEY_BYTE_LEN);
   char *cipherBlock = (char *) malloc(sizeof(char) * BLOCKSIZE);
   char *decryptBlock = (char *) malloc(sizeof(char) * BLOCKSIZE);
   long diskSize;
   int size;

   FILE *fp;
   uint64_t blockNum;
   uint64_t byteNum;
   char *iv = (char *) malloc(sizeof(char) * IV_BYTE_LEN);

   if(!verifyUser(uname, password, disk, key)) {
      return -1;
   }

   if(!hasDiskNum(disk)) {
      return -1;
   }

   fp = fopen(disks[disk], "r+");
   fseek(fp, 0L, SEEK_END);
   diskSize = ftell(fp);

   if(bNum * BLOCKSIZE > diskSize) {
      return -1;
   }

   blockNum = bNum;
   byteNum = blockNum * BLOCKSIZE;

   memcpy(iv, &blockNum, sizeof(uint64_t));
   memcpy(iv + 8, &byteNum, sizeof(uint64_t));

   size = encrypt(block, BLOCKSIZE, key, iv, cipherBlock);
   decrypt(cipherBlock, BLOCKSIZE, key, iv, decryptBlock);

   printf("%s\n", decryptBlock);
   printf("size: %d\n", size);

   fseek(fp, byteNum + BLOCKSIZE, SEEK_SET);
   fwrite(cipherBlock, 1, BLOCKSIZE, fp);

   fclose(fp);
   return 0;
}

int creatUser(int disk, char * uname, char * password, char * adminpsswd) {
   FILE *fp;
   char *adminKey, *diskKeyHash;
   char *newAdminCipherText;
   char *adminBuffer;
   char *adminPlaintext = malloc(sizeof(char) * USER_SECTOR_BYTE_LEN);
   char *possDiskKeyHash = malloc(sizeof(char) * DISKKEY_HASH_SIZE);
   char *plain;
   char *newUserKey, *newUserPlain, *newUserCipher, *hashedUserName;
   unsigned char *salt = "264722680";
   char *iv = (char *) malloc(sizeof(char) * IV_BYTE_LEN);
   char *adminIV = (char *) malloc(sizeof(char) *IV_BYTE_LEN);
   uint64_t *numUsers, bNum, byteNum;

   if(!verifyUser("admin", adminpsswd, disk, NULL)) {

      return -1;
   }

   //Create a key for the admin in this disk.
   adminKey = (char *) malloc(sizeof(char) * KEY_BYTE_LEN);
   PKCS5_PBKDF2_HMAC(adminpsswd, strlen(adminpsswd), salt, strlen(salt), ITERATIONS, EVP_sha512(), KEY_BYTE_LEN, adminKey);   

   fp = fopen(disks[disk], "r+");

   // Get the disk key hash
   diskKeyHash = (char *) malloc(sizeof(char) * DISKKEY_HASH_SIZE);
   fread(diskKeyHash, 1, DISKKEY_HASH_SIZE, fp);

   bNum = 0;
   byteNum = bNum * USER_SECTOR_BYTE_LEN;
   memcpy(adminIV, &bNum, sizeof(uint64_t));
   memcpy(adminIV + 8, &byteNum, sizeof(uint64_t));

   // Read in the admin ciphertext and decrypt it
   adminBuffer = (char *) malloc(sizeof(char) * USER_SECTOR_BYTE_LEN);
   fread(adminBuffer, 1, USER_SECTOR_BYTE_LEN, fp);
   decrypt(adminBuffer, USER_SECTOR_BYTE_LEN, adminKey, adminIV, adminPlaintext);

   // Get the number of users and update it
   numUsers = (uint64_t *) (adminPlaintext + KEY_BYTE_LEN + 8);
   
   bNum = *numUsers;
   byteNum = bNum * USER_SECTOR_BYTE_LEN;
   memcpy(iv, &bNum, sizeof(uint64_t));
   memcpy(iv + 8, &byteNum, sizeof(uint64_t));

   printf("creation num users: %ld\n", *numUsers);
   (*numUsers)++;
   printf("new num users: %ld\n", *numUsers);
   memcpy(adminPlaintext + KEY_BYTE_LEN + 8, numUsers, sizeof(uint64_t));

   // Update the admin ciphertext with the new number of users 
   newAdminCipherText = (char *) malloc(sizeof(char) * USER_SECTOR_BYTE_LEN);
   encrypt(adminPlaintext, USER_SECTOR_BYTE_LEN, adminKey, adminIV, newAdminCipherText);

   // Write the new admin ciphetext to the disk
   fseek(fp, DISKKEY_HASH_SIZE, SEEK_SET);
   fwrite(newAdminCipherText, 1, USER_SECTOR_BYTE_LEN, fp);

   // Create the new user's key
   newUserKey = (char *) malloc(sizeof(char) * KEY_BYTE_LEN);
   PKCS5_PBKDF2_HMAC(password, strlen(password), salt, strlen(salt), ITERATIONS, EVP_sha512(), KEY_BYTE_LEN, newUserKey);   

   // Get the user name hashed
   hashedUserName = (char *) malloc(sizeof(char) * 16);
   PKCS5_PBKDF2_HMAC(uname, strlen(uname), salt, strlen(salt), ITERATIONS, EVP_sha512(), 16, hashedUserName);   

   // Create the new user's plaintext
   newUserPlain = (char *) malloc(sizeof(char) * USER_SECTOR_BYTE_LEN);
   memcpy(newUserPlain, adminPlaintext, KEY_BYTE_LEN);
   memcpy(newUserPlain + KEY_BYTE_LEN, hashedUserName, 16);

   // Create the new user's ciphertext
   newUserCipher = (char *) malloc(sizeof(char) * USER_SECTOR_BYTE_LEN);
   encrypt(newUserPlain, USER_SECTOR_BYTE_LEN, newUserKey, iv, newUserCipher);

   // Write the new user's ciphertext to their user sector on the disk
   fseek(fp, ((*numUsers) - 2) * USER_SECTOR_BYTE_LEN, SEEK_CUR);
   fwrite(newUserCipher, 1, USER_SECTOR_BYTE_LEN, fp);

   fclose(fp);
}

int main() {
   int disk;
   int verified;
   char text[BLOCKSIZE];
   int writeFlag;
   char *readText = (char *) malloc(sizeof(char) * BLOCKSIZE);

   disk = mountDisk("test2.disk", 4096 * 4);
   creatUser(disk, "sally", "5678", "admin");
   creatUser(disk, "bob", "1234", "admin");
   

   printf("disk num: %d\n", disk);

   verified = verifyUser("admin", "admin", disk, NULL);

   printf("user verified? %d\n", verified);

   verified = verifyUser("bob", "1234", disk, NULL);

   printf("user verified? %d\n", verified);   

   verified = verifyUser("sally", "5678", disk, NULL);

   printf("user verified? %d\n", verified);   

   int i;
   for (i = 0; i < BLOCKSIZE; i+= 4)
   {
      text[i] = 'H';
      text[i+1] = 'i';
      text[i+2] = '!';
      text[i+3] = '!';
   }
   text[BLOCKSIZE-1] = '\0';
   writeFlag = writeBlock(0, 2, text, "bob", "1234");
   printf("writeFlag: %d\n", writeFlag);

   writeFlag = readBlock(0, 2, readText, "bob", "1234");
   printf("readFlag: %d\n", writeFlag);
   printf("%s\n", readText);

   return 0;
}