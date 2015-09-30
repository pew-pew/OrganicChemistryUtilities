import OrganicChemistryLib as OCL
import tkinter as tk

C_COLORS = "#444444 gray white lightgreen green".split(" ")

class DrawableAtom(OCL.Atom):
    def __init__(self, element, x, y, r=10, name=None):
        self.x = x
        self.y = y
        self.r = r
        self.color = "black"
        self._groupName = ""
        self._depth = 0
        
        super().__init__(element, name=name)
    
    def draw(self, canvas):
        x, y, r = self.x, self.y, self.r
        fill = "lightblue" if self.getElement() == "H" else C_COLORS[self._depth % len(C_COLORS)]
        canvas.create_oval(x - r, y - r, x + r, y + r, outline=self.color, fill=fill, width=self.r // 10)
        canvas.create_text(x, y, text=self.getElement(), font=("Times", self.r), fill=self.color)
    
    def drawConnections(self, canvas):
        for nb in self.neighbours():
            canvas.create_line(self.x, self.y, nb.x, nb.y, width=self.r // 10)
    
    def mark(self, name, depth):
        self._groupName = name
        self._depth = depth

class Workspace:
    def __init__(self, root, width=400, height=400):
        self.root = root
        self.width = width
        self.height = height
        
        self.canvas = tk.Canvas(root, width=width, height=height, background="white")
        self.canvas.pack()
        self.atoms = set()
        
        self.canvas.bind("<Button-1>", self.onB1Press)
        self.canvas.bind("<ButtonRelease-1>", self.onB1Release)
        self.canvas.bind("<B1-Motion>", self.onB1Motion)
        self.canvas.bind("<Button-3>", self.onB3Press)
        self.canvas.bind("<Button-2>", self.onB2Press)
        
        self.status = None
        self.statusData = None
        
        self.update()
    
    def redraw(self):
        self.canvas.delete("all")
        self.drawConnections()
        self.drawAtoms()
    
    def update(self):
        self.redraw()
    
    def onB2Press(self, event):
        print(OCL.getName(self.getAtomAt(event.x, event.y)))
        self.update()
        
    def onB3Press(self, event):
        atom = self.getAtomAt(event.x, event.y)
        if self.status == None and atom != None:
            atom.disconnectAll()
        if atom == None:
            self.addAtom("H", event.x, event.y)
        self.update()
    
    def onB1Press(self, event):
        atom = self.getAtomAt(event.x, event.y)
        if atom != None:
            if self.status == None:
                self.status = "atom-pressed"
                self.statusData = atom
            elif self.status == "atom-search-for-connection":
                atom.connect(self.statusData)
                self.status = None
                self.statusData.color = "black"
                self.statusData = None
        else:
            self.addAtom("C", event.x, event.y)
        
        self.update()
    
    def onB1Release(self, event):
        if self.status == "atom-moving":
            self.status = None
            ax = self.statusData.x
            ay = self.statusData.y
            if ax < 0 or ax >= self.width or ay < 0 or ay > self.height:
                self.atoms.remove(self.statusData)
                self.statusData.disconnectAll()
            self.statusData.color = "black"
            self.statusData = None
        elif self.status == "atom-pressed":
            self.status = "atom-search-for-connection"
            self.statusData.color = "red"
        self.update()
    
    def onB1Motion(self, event):
        if self.status == "atom-pressed":
            self.statusData.color = "darkgreen"
            self.status = "atom-moving"
        
        if self.status == "atom-moving":
            self.statusData.x = event.x
            self.statusData.y = event.y
        self.update()
    
    def drawConnections(self):
        for atom in self.atoms:
            atom.drawConnections(self.canvas)
    
    def drawAtoms(self):
        for atom in self.atoms:
            atom.draw(self.canvas)
    
    def addAtom(self, element, x, y, r=25, name=None):
        self.atoms.add(DrawableAtom(element, x, y, r, name))
        self.update()
    
    def getAtomAt(self, x, y):
        for atom in self.atoms:
            if (x - atom.x) ** 2 + (y - atom.y) ** 2 <= atom.r ** 2:
                return atom
        return None
    
    

root = tk.Tk()
ws = Workspace(root, width=700, height=700)
ws.addAtom("C", 30, 30)
ws.addAtom("C", 70, 30)
ws.addAtom("C", 110, 30)
ws.addAtom("H", 200, 300)
root.mainloop()