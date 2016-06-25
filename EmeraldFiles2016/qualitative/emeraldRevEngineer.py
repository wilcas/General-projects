
#generates all possible B/C outputs from serial inputs to A
def generateBitString():
	inputBits = '0010101000100000'
	bI = 0
	cI = 1
	cCommand = '1110100'
	bCommand = '01110100'
	while (cI != bI):
		inputBits += bCommand[bI] + cCommand[cI - 1]
		bI = (bI + 1) % len(bCommand)
		cI = (cI + 1) % len(cCommand)
	return inputBits +"11111100110000"

print generateBitString()
