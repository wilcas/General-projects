import re




def findLongestWord():
	f = open('karamazov.txt')
	cur = ""
	for line in f:
		words = re.findall(r"[\w']+", line) #split line at white space
		for word in words:
			if len(word) > len(cur):
				cur = word
	return cur

def padFile():
	f = open('karamazov.txt')
	paddedF = ""
	longestWord = findLongestWord()
	for line in f:
		print "hey"
		words = re.findall(r"[\w']+", line)
		for word in words:
			print "here"
			if len(word) < len(longestWord):
				paddedWord = word + longestWord[len(word):len(longestWord)]
				paddedF += "\t" + paddedWord
			else:
				paddedF += "\t" + word
	return paddedF

#f1 = open('paddedKaramazov.txt','w')	

#f1.write(padFile())



"""
def getAnagrams():
	f1 = open('paddedKaramazov.txt')
	#make words into list
	allWords = set()
	anagrams = dict()
	for line in f1:
		words = line.split()
		allWords = allWords.union(set(words))
	return f(allWords.pop(),allWords,anagrams)

def f(word,S,anagrams):
	if len(S) == 0:
		return anagrams
	else:
		sortedW = ''.join(sorted(word))
		for elem in S:
			sortedE = ''.join(sorted(elem))
			if sortedE == sortedW:
				if word in anagrams:
					anagrams[word].add(elem)
				else:
					anagrams[word] = set([elem])
			else:
				pass
		return f(S.pop(),S,anagrams)


print getAnagrams()"""



