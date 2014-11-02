import urllib2
import time

def two_space_hex(hex_str):
   if len(hex_str) == 3:
      return '0' + hex_str[2]
   else:
      return hex_str[2:]

def taskIVA():
	mac = '0000000000000000000000000000000000000000'
	knownVals = ''
	numFound = 0
	testVal = 0
	while(True):
		testMac = knownVals + two_space_hex(hex(testVal)) + mac[(numFound + 1)*2:]

		start = time.time()
		response = urllib2.urlopen('http://localhost:8080/?q=foo&mac=' + testMac)
		stop = time.time()

		if(response.read().find("Invalid signature") == -1):
			print testMac
			quit()

		tot = stop - start
		if tot >= .01 * (numFound + 1):	
			numFound += 1 
			knownVals += two_space_hex(hex(testVal))
			
			testVal = 0
			print "yay!: " + testMac
		elif testVal > 256:
			print "huh??????"
		else:
			testVal+= 1


	html = response.read()
	print html


def main():
	
	taskIVA()

if __name__ == '__main__':
   main()