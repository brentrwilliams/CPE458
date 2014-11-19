def encrypt(plaintext, cipherAlph):
	plaintextAlph = "abcdefghijklmnopqrstuvwxyz"

	ciphertext = ""

	plaintext = "".join(plaintext.splitlines())
	plaintext = "".join(plaintext.split(" "))
	plaintext = plaintext.lower()

	plaintextAlphList = list(plaintextAlph)

	if len(cipherAlph) != 26:
		return "error"


	for letter in plaintext:
		ind = plaintextAlphList.index(letter)
		ciphertext += cipherAlph[ind]

	return ciphertext


def decrypt(ciphertext, cipherAlph):
	plaintextAlph = "abcdefghijklmnopqrstuvwxyz"

	plaintext = ""

	cipherAlphList = list(cipherAlph)

	if len(cipherAlph) != 26:
		return "error"

	for letter in ciphertext:
		ind = cipherAlphList.index(letter)
		plaintext += plaintextAlph[ind]

	return plaintext
	


def main():
	cipherAlph = "qwertyuiopasdfghjklzxcvbnm"
	text = "hello my name is drew aNd i Am going to decrypt this message"

	cipher = encrypt(text, cipherAlph)
	print cipher

	print decrypt(cipher, cipherAlph)


if __name__ == '__main__':
   main()