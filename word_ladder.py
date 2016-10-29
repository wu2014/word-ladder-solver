"""
File: word_ladder.py

Implement a word ladder puzzle solver
"""

class Graph:
    def __init__(self):
        self.vertices = {}
        self.numVertices = 0
        
    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertices[key] = newVertex
        return newVertex
    
    def getVertex(self,n):
        if n in self.vertices:
            return self.vertices[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertices
    
    def addEdge(self,f,t,cost=0):
            if f not in self.vertices:
                nv = self.addVertex(f)
            if t not in self.vertices:
                nv = self.addVertex(t)
            self.vertices[f].addNeighbor(self.vertices[t],cost)
    
    def getVertices(self):
        return list(self.vertices.keys())
        
    def __iter__(self):
        return iter(self.vertices.values())

class Vertex:
    def __init__(self,key):
        self.id = key
        self.connectedTo = {}

    def addNeighbor(self,nbr,weight=0):
        self.connectedTo[nbr] = weight

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self,nbr):
        return self.connectedTo[nbr]

class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self,item):
        self.queue.append(item)

    def dequeue(self):
        return self.queue.pop(0)

    def __str__(self):
        return str(self.queue)

    def empty(self):
        return self.queue == []    
        
def bfs(start,finish,g):
    parents = {}
    q = Queue()
    q.enqueue(start)
    parents[start.getId()] = None

    while not q.empty():
        v = q.dequeue()
        for nbr in v.getConnections():
            n = nbr.getId()
            if n not in parents:
                parents[n] = v
                if nbr == finish:
                    return parents
                q.enqueue(nbr)
    return parents


def getPath(start,finish,parents):
    finish = finish.getId()
    path = [finish]
    if finish in parents:
        v = parents[finish]
        while(v != start):
            path.append(v.getId())
            v = parents[v.getId()]
    else:
        "Sorry, No Path found"

    path.append(start.getId())

    return path[::-1]

def buildGraph():
    d = {}
    # edges = []
    g = Graph()    
    wfile = file('words.dat')
    wordLength = int(wfile.readline().rstrip('\n'))
    # create buckets of words that differ by one letter.
    for line in wfile:
        word = line[0:wordLength]
        for i in range(wordLength):
            bucket = word[0:i] + '_' + word[i+1:wordLength]
            if d.has_key(bucket):
                d[bucket].append(word)
            else:
                d[bucket] = [word]
    # add vertices and edges for words in the same bucket.
    for i in d.keys():
        for j in d[i]:
            for k in d[i]:
                if j != k:
                    # edges.append((j,k))
                    g.addEdge(j,k)
    # return edges
    return g

# e = buildGraph()
# print e

# g = buildGraph()

if __name__ == '__main__':

    g = buildGraph()
    # print g.getVertices()

    word1 = raw_input('Enter the start word: ')
    word2 = raw_input('Enter the stop word: ')

    if word1 in g:
        start = g.getVertex(word1)
        if word2 in g:
            finish = g.getVertex(word2)
            predecessors = bfs(start, finish, g)
            # print predecessors
            path = getPath(start, finish, predecessors) 
           
            shortest_path = 'The shortest path is: '
            for p in path:
                shortest_path += p + ' -> '
            print (shortest_path[:-3])
        else:
            print("Word2 not in graph") 
    else:
        print("Word1 not in graph")

