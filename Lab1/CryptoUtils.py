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
   return asciiToBase64(hexToAscii(text))

def intToBase64(num):
   return base64.b64encode(bytes(num))