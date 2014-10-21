import sys

#returns a dictionary mapping character to where it occurs
#takes in a dictionary with mapping keys to a list of occurences
def readModText(charDict,readsText): 
    for i in xrange(len(readsText)):
      char = readsText[i+1]
      if char in charDict:
        charDict[char].append(i)
    return charDict


#takes in a dictionary and prints the data at each key
#writes the data to a file f 

def writeDictionary(charDict, f):
  for key in charDict:
    label = "%s occurs at:\t" % key
    f.write("\n"+label)
    for location in charDict[key]:
      value = "%d" % location
      f.write(value + '\t')
  return

#Dictionary: change keys to edit what is being searched for
#in string
d = {":" : [], "#" : [], "B" : [], "J" : [], "P" : [],"?" : [],
     "Y" : [], "7" : [], "M" : [], "I" : [],"O" : []}

#string to search, first argument givenon command line
reads = sys.argv[1]

#file to be saved to, second input
fileName = sys.argv[2]

#initialize file
f = open(fileName+".txt", 'w')

#initialize dictionary
toWrite = readModText(d, reads)

#write dictionary to a file
writeDictionary(toWrite, f)
