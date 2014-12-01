from CryptoUtils import LetterFrequencies, index_to_char, char_to_index
import random
import re
from CryptoUtils import NGramScorer


def encrypt(plaintext, cipherAlph):
	plaintextAlph = "abcdefghijklmnopqrstuvwxyz"

	ciphertext = ""

	plaintext = "".join(plaintext.splitlines())
	plaintext = "".join(plaintext.split(" "))
	plaintext = "".join(plaintext.split(","))
	plaintext = "".join(plaintext.split("."))
	plaintext = plaintext.lower()

	plaintextAlphList = list(plaintextAlph)

	if len(cipherAlph) != 26:
		return "error"


	for letter in plaintext:
		ind = plaintextAlphList.index(letter)
		ciphertext += cipherAlph[ind]

	return ciphertext


def decrypt(ciphertext, cipherAlph):
	plaintextAlph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

	plaintext = ""

	cipherAlphList = list(cipherAlph)

	if len(cipherAlph) != 26:
		return "error"

	for i in xrange(0, 26):
		ciphertext = ciphertext.replace(cipherAlph[i], plaintextAlph[i])

	#for letter in ciphertext:
	#	ind = cipherAlphList.index(letter)
	#	plaintext += plaintextAlph[ind]

	plaintext = ciphertext.lower()
	return plaintext

def crack(ctext):
	fitness = NGramScorer(3)
	difitness = NGramScorer(2)
	quadfitness = NGramScorer(4)
	maxkey = list('abcdefghijklmnopqrstuvwxyz')
	maxscore = -99e9
	parentscore,parentkey = maxscore,maxkey[:]
	print "Substitution Cipher solver, you may have to wait several iterations"
	print "for the correct result. Press ctrl+c to exit program."
	# keep going until we are killed by the user
	i = 0
	while i < 30:
	    i = i+1
	    #print i
	    random.shuffle(parentkey)
	    deciphered = decrypt(ctext, parentkey)
	    parentscore = fitness.score(deciphered) + difitness.score(deciphered) + quadfitness.score(deciphered)
	    count = 0
	    while count < 1000:
	        a = random.randint(0,25)
	        b = random.randint(0,25)
	        child = parentkey[:]
	        # swap two characters in the child
	        child[a],child[b] = child[b],child[a]
	        deciphered = decrypt(ctext, child)
	        score = (fitness.score(deciphered) + difitness.score(deciphered)) + quadfitness.score(deciphered)
	        # if the child was better, replace the parent with it
	        if score > parentscore:
	        	#print "tri: " + str(fitness.score(deciphered))
	        	#print "di: " + str(difitness.score(deciphered))
	        	parentscore = score
	        	parentkey = child[:]
	        	count = 0
	        count = count+1
	    # keep track of best score seen so far
	    if parentscore>maxscore:
	        maxscore,maxkey = parentscore,parentkey[:]
	        #print '\nbest score so far:',maxscore,'on iteration',i
	        #ss = SimpleSub(maxkey)
	        deciphered = decrypt(ctext, maxkey)
	        #print '    best key: '+''.join(maxkey)
	        #print '    plaintext: '+ deciphered
	        #print "tri: " + str(fitness.score(deciphered))
	        #print "di: " + str(difitness.score(deciphered))

	return decrypt(ctext, maxkey)


def main():
	cipherAlph = "qwertyuiopasdfghjklzxcvbnm"
	             #abcdefghijklmnopqrstuvwxyz    
	             #gnixthhlfmcxelfumllqicemhm

	#text = "hello my name is drew aNd i Am going to decrypt this message i hope it works because this is getting really annoying and i want this to work very badly please program do this for me the world depends on it and i want it to work hello my name is drew aNd i Am going to decrypt this message i hope it works because this is getting really annoying and i want this to work very badly please program do this for me the world depends on it and i want it to work"
	text = '''Most of the production will take place in Montreal, where the studio is currently ramping up its feature animation team to work on Charming and subsequent productions. These first films will allow us to build infrastructure, a team, pipeline and so on, says Butler. It will help us make the feature animation studio we want to be. At the same time, were also going to start to go out and develop our own scripts for our movies. And theyll be ones we own more of going forward.
In terms of animation style, Butler plans to maintain a visual effects quality to the work. Were very ambitious about the quality, he says. I want to capitalize on the high production values we instituted on Beans and then keep it in the box. In VFX you typically have to be a lot more agile, but I learnt my craft at Disney and I feel like we can manage them in a similar way. We want to be successful  make good looking films and make more than one.
Cinesite will continue to work in visual effects  upcoming projects include The Man From U.N.C.L.E. and San Andreas, for example  but this work will run alongside animated features. Id love to do a feature length version of Beans, admits Butler when asked about future plans, who also notes that the studio also plans on accepting scripts and developing ideas for films.'''


	cipher = encrypt(text, cipherAlph)
	print cipher

	print decrypt(cipher, cipherAlph)

	print crack(cipher)


if __name__ == '__main__':
   main()