import cv2
from vecteur import Vecteur
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import IPython.display as display
import time
import imageio
class Modelisation:
    def __init__(self):
        def click_event(event, x, y, flags, params):

            f = open("etalonnage.txt", 'a')
            if event == cv2.EVENT_LBUTTONDOWN:
                # print(x,y)
                f.write(str(x) + ',')
                f.write(str(y)+',')
            f.close()
        self.ecranLargeur = 1920
        self.ecranHauteur = 1080
        f = open("etalonnage.txt", 'r+')
        self.imageEnCours = 0
        
        self.image = cv2.imread("frames/basket/frame11.png")
        self.nbLignes = self.image.shape[0]
        self.nbColonnes = self.image.shape[1]

        self.ratioFenetre = self.nbColonnes/self.nbLignes
        # print ("l'image contient ", self.nbLignes, "lignes et " ,self.nbColonnes, " colonnes")
        filesize = os.path.getsize("etalonnage.txt")
        if filesize == 0:
            cv2.namedWindow('mon image', cv2.WINDOW_NORMAL)
            cv2.moveWindow('mon image', int(self.ecranLargeur/2), 10)
            cv2.resizeWindow('mon image', int(
                self.ecranHauteur*0.75*self.ratioFenetre), int(self.ecranHauteur*0.75))
            cv2.setWindowProperty('mon image', cv2.WND_PROP_TOPMOST, 1)
            cv2.imshow('mon image', self.image)
            cv2.setMouseCallback('mon image', click_event)
            cv2.waitKey()
            cv2.destroyAllWindows()
            with open("etalonnage.txt", "r") as filestream:
                for line in filestream:
                    currentline = line.split(",")

            nbPixel = int(((int(currentline[3])-int(currentline[1]))
                          ** 2+(int(currentline[2])-int(currentline[0]))**2)**0.5)
            distanceMetre = float(input("Quelle est la distance mesurée ?"))
            self.pixelSize = distanceMetre/nbPixel
            f = open("etalonnage.txt", 'a')
            f.truncate(0)
            f.write(str(self.pixelSize))

        else:
            with open("etalonnage.txt", "r") as filestream:
                for line in filestream:
                    currentline = line.split(",")
            self.pixelSize = float(currentline[0])
        _, _, files = next(os.walk("frames/basket"))
        file_count = len(files)
        self.nbImages = file_count-1
        f.close()
        self.positions = []
        self.vitesses = []
        d=display.display('test', display_id='essai')

    def show(self, position, vitesse):
        self.image = imageio.imread(
            'frames/basket/frame'+str(self.imageEnCours)+'.png')
        self.dessineCroix(position)
        cv2.putText(self.image, "Image "+str(self.imageEnCours), (30, 270),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.imwrite('img.png',self.image)
        dispImg = display.Image(filename='img.png',width = 400, height = 400)
        display.update_display(dispImg,display_id='essai')
        time.sleep(0.3)
        self.imageEnCours = self.imageEnCours +1
        
    def metersToPixel(self, lc):
        pix = lc/self.pixelSize
        pix = Vecteur(int(pix.x), int(pix.y))
        return pix

    def pixelToMeters(self, pix):
        lc = pix*self.pixelSize
        return lc

    def dessineCroix(self, position):
        # print(position)
        pix = self.metersToPixel(position)
        pix = Vecteur(pix.x, self.nbLignes-pix.y)
        # print(pix)
        tailleCroix = 3
        color = (255, 255, 255)
        cv2.line(self.image, (pix.x-tailleCroix, pix.y-tailleCroix),
                 (pix.x+tailleCroix, pix.y+tailleCroix), color, 2)
        cv2.line(self.image, (pix.x+tailleCroix, pix.y-tailleCroix),
                 (pix.x-tailleCroix, pix.y+tailleCroix), color, 2)
        cv2.putText(self.image, "Modele", (pix.x, pix.y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 1, cv2.LINE_AA)

    def dessineVecteur(self, vposition, vecteur, echelle=0.5):
        end_point = vposition+vecteur*echelle
        # print(position)
        vposition = self.metersToPixel(vposition)
        vposition = Vecteur(vposition.x, self.nbLignes-vposition.y)
        
        end_point = self.metersToPixel(end_point)
        end_point = Vecteur(end_point.x, self.nbLignes-end_point.y)
        
        self.image = cv2.arrowedLine(self.image, (vposition.x, vposition.y), (end_point.x,
                                     end_point.y), (255, 255, 0), 2)

    def showVecteur(self, vPos, vVitesse) :
         with imageio.get_writer('modelisationVecteur.gif', mode='I',fps=2) as writer:
             # print(listFichier)
             for i  in range(len(vVitesse)):
                 self.image = imageio.imread('frames/basket/frame'+str(i)+'.png')
                 self.dessineCroix(vPos[i])
                 self.dessineVecteur(vPos[i],vVitesse[i])
                 writer.append_data(self.image)
  