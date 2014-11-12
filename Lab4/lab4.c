#include <stdio.h>
#include <stdlib.h>  
#include <string.h>
#define BLOCKSIZE 4096
#define BLOCKSIZE_NOADMIN 4064
#define MAX_DISKS 100


char* disks[MAX_DISKS];
int numDisks = 0;

int hasDisk(char *filename) {
   int i = 0;
   for (i = 0; i < numDisks; i++) {
      if (strcmp(filename, disks[i])) {
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
   char *driveKey;

   if (nBytes % BLOCKSIZE != 0) {
      return -1;
   }

   if (nBytes > 0) {
      randFp = fopen("/dev/urandom", "r");
      
      randUserStuff = (char *) malloc(sizeof(char) * BLOCKSIZE_NOADMIN);
      fread(randUserStuff, 1, BLOCKSIZE_NOADMIN, randFp);

      randStuff = (char *) malloc(sizeof(char) * nBytes);
      fread(randStuff, 1, nBytes, randFp);
      
      driveKey = (char *) malloc(sizeof(char) * 16);
      fread(driveKey, 1, 16, randFp);

      fclose(randFp);

      fp = fopen(filename, "w+");



      
      fwrite(randStuff, 1, nBytes, fp);
      fclose(fp);

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

/* readBlock() reads an entire block of BLOCKSIZE bytes from the open disk
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
int writeBlock(int disk, int bNum, void *block) {

   return 0;

}