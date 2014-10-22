import base64

def asciiToHex(text):
   return text.encode(encoding='hex', errors='strict')

def hexToAscii(text):
   return text.decode(encoding='hex', errors='strict')

def asciiToBase64(text):
   return text.encode(encoding='base64',errors='strict') 

def base64ToAscii(text):
   return text.decode(encoding='base64',errors='strict')

def base64ToHex(text):
   return asciiToHex(base64ToAscii(text))

def hexToBase64(text):
   return asciiToBase64(hexToAscii(text

def xor(plaintext, key):
   textLen = len(plaintext);
   keyLen = len(key);
   newString = "";

   for i in range(0, textLen):
      keyChar = key[i % keyLen];
      textChar = plaintext[i];
      
      keyInt = ord(keyChar);
      textInt = ord(textChar);
      
      newInt = keyInt ^ textInt;
      newChar = chr(newInt);

      newString += newChar;

   return newString