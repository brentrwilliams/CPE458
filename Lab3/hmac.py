from hashlib import sha1
import binascii

trans_5C = bytearray((x ^ 0x5c) for x in range(256))
trans_36 = bytearray((x ^ 0x36) for x in range(256))
blocksize = sha1().block_size # 64
 
def hmac_sha1(key, msg):
   if len(key) > blocksize:
      key = sha1(key).digest()
   key = key + bytearray(blocksize - len(key))

   o_key_pad = key.translate(trans_5C)
   i_key_pad = key.translate(trans_36)
   return sha1(o_key_pad + sha1(i_key_pad + msg).digest())
 
if __name__ == "__main__":
   h = hmac_sha1(binascii.unhexlify("707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f909192939495969798999a9b9c9d9e9fa0"), b"Sample #4")
   print(h.hexdigest())
