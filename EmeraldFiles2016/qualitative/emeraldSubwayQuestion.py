dataFile = open('emeraldSubwayData.txt')

#reads in values from a csv file to make an undirected edgemap
#weights can be excluded since we can find the eulerian circuit
#and
def createGraph (data):
	G = dict() #Graph mapping a node to a set of neighbors
	for line in data:
		graphData = line.split(',')
		(v1,v2) = (graphData[0], graphData[1])
		if v1 in G:
			G[v1].add(v2)
		else:
			G[v1] = set([v2])
		if v2 in G:
			G[v2].add(v1)
		else:
			G[v2] = set([v1])
	return G


#finds the euler path through the graph using the algorithm at 
#http://www.graph-magics.com/articles/euler.php

def getEuler (G):
	#initialize
	stack = []
	eulerianCircuit = []
	cur= "Denver" #start with one of two vertices with an odd degree 
	stack.append(cur)
	while((len(stack) != 0)):
		if (len(G[cur]) != 0):
			stack.append(cur) #add vertex to stack
			tmp = cur
			cur = G[tmp].pop()#pick random neighbor as cur/remove forward edge
			G[cur].discard(tmp) #remove back edge @TODO FIX THIS LINE
		else:
			eulerianCircuit.append(cur) #cur is part of circuit
			cur = stack.pop()
	return eulerianCircuit

graph = createGraph(dataFile)

print getEuler(graph)




