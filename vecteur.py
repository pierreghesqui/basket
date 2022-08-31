class Vecteur:
    
    def __init__(self,x,y):
        #générer notre jeu
        self.x = x
        self.y = y
    
    def __add__(self, other):
        x2 = self.x+other.x
        y2 = self.y + other.y
        vecteur2 = Vecteur(x2,y2)
        return vecteur2
    
    def __sub__(self,other):
        x2 = self.x-other.x
        y2 = self.y - other.y
        vecteur2 = Vecteur(x2,y2)
        return vecteur2
    
    def __mul__(self,other):
        x2 = self.x*other
        y2 = self.y*other
        vecteur2 = Vecteur(x2,y2)
        return vecteur2
    
    def __rmul__(self,other):
        x2 = self.x*other
        y2 = self.y*other
        vecteur2 = Vecteur(x2,y2)
        return vecteur2
    
    def __truediv__(self,other):
        x2 = self.x/other
        y2 = self.y/other
        vecteur2 = Vecteur(x2,y2)
        return vecteur2
    def norme(self):
        return (self.x**2+self.y**2)**0.5
    def __str__(self):
        return "x= " + str(self.x)+ "; y = "+ str(self.y)   