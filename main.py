def readLines(file):
    fin = open(file)
    lines = fin.readlines()
    fin.close()
    return [line.rstrip() for line in lines if line.rstrip()]
    
prefixes_modifers = readLines("prefixes_modifers.txt")

prefixes = readLines("prefixes.txt")


def getPrefixModifer(x):
    x -= 1
    if (x < len(prefixes_modifers)):
        return prefixes_modifers[x]
    return "[*%s]"%(x)

def getPrefix(x):
    x -= 1
    if (x < len(prefixes)):
        return prefixes[x]
    return "[%s]"%(x)

class Atom:
    def __init__(self, element, name=None):
        self._element = element
        if name == None:
            self._name = element
        else:
            self._name = name
        self._neighbours = set()
    
    def __str__(self):
        return self._element
    
    def __repr__(self):
        return self._name
    
    def getElement(self):
        return self._element
    
    def _connect(self, other):
        self._neighbours.add(other)
    
    def connect(self, other):
        self._connect(other)
        other._connect(self)
    
    def _disconnect(self, other):
        if other in self._neighbours:
            self._neighbours.remove(other)
    
    def disconnect(self, other):
        self._disconnect(other)
        other._disconnect(self)
    
    def isConnected(self, other):
        return other in self._neighbours
    
    def neighbours(self):
        return self._neighbours

def longestPath(atom, prev=None):
    maxPath = []
    maxLength = 0
    for nb in atom.neighbours():
        if nb != None:
            if nb.getElement() == "C" and nb != prev:
                currPath = longestPath(nb, atom)
                if len(currPath) > maxLength:
                    maxPath = currPath
                    maxLength = len(currPath)
    maxPath.append(atom)
    return maxPath

def getName(startAtom, prevAtom=None, spaces=False, brackets=False):
    path = longestPath(startAtom, prevAtom)
    path = list(reversed(path))
    
    adds = dict()
    
    for i in range(len(path)):
        curr = path[i]
        prevNb = path[i - 1] if i > 0 else prevAtom
        nextNb = path[i + 1] if i < len(path) - 1 else None
        for nb in curr.neighbours():
            if nb.getElement() != "H" and nb != prevNb and nb != nextNb:
                name = getName(nb, curr, spaces, brackets)
                if adds.get(name, None) == None:
                    adds[name] = []
                adds[name].append(str(i + 1))
    
    name = []
    for it in adds.items():
        places = " ".join(it[1])
        if (len(it[1]) > 1):
            modifer = getPrefixModifer(len(it[1]))
        else:
            modifer = ""
        subName = modifer + (" " if spaces and modifer else "") + it[0]
        
        if brackets:
            name.append("[" + places + "]")
            name.append("(" + subName + ")")
        else:
            name.append(places)
            name.append(subName)
    
    name.append(getPrefix(len(path)) + ("ил" if prevAtom != None else "ан"))
    return " ".join(name)

def parse(text):
    lines = text.split("\n")
    maxLen = max([len(line) for line in lines])
    inpMatrix = [list(line) for line in lines]
    for y in range(len(inpMatrix)):
        inpMatrix[y] = inpMatrix[y] + [" "] * (maxLen - len(inpMatrix[y]))
    firstAtom = None
    atomMatrix = [[None] * maxLen for i in range(len(inpMatrix))]
    for y in range(len(inpMatrix)):
        for x in range(maxLen):
            if inpMatrix[y][x] in "HC":
                atomMatrix[y][x] = Atom(inpMatrix[y][x])
                if firstAtom == None:
                    firstAtom = atomMatrix[y][x]
    for y in range(len(inpMatrix)):
        for x in range(maxLen):
            if inpMatrix[y][x] == "-":
                atomMatrix[y][x - 1].connect(atomMatrix[y][x + 1])
            elif inpMatrix[y][x] == "|":
                atomMatrix[y - 1][x].connect(atomMatrix[y + 1][x])
    return firstAtom


fin = open("input.txt", "r")
text = fin.read()
fin.close()
print(getName(parse(text)))