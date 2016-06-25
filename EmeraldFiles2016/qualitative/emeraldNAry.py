
f = open('huffmanData.txt')

keys = []
freqs = []

for line in f:
	elems = line.split(',')
	(elem, freq) = (elems[0], elems[1])
	keys.append(elem)
	freqs.append(float(freq[0:len(freq)-1]))

print keys
print freqs