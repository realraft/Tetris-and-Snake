from tkinter import *
from Pixel import Pixel
import numpy as np
import random
import time

class Grid:
    
        def __init__(self,root, nrow, ncol, scale):
               self.nrow=nrow
               self.ncol=ncol
               self.scale=scale
               self.canvas = Canvas(root, width=ncol*scale,height=nrow*scale,bg="black")
               for i in range(ncol+1):
                       self.canvas.create_line(i*scale,0,i*scale,nrow*scale, fill="gray", width=1)
               for i in range(nrow+1):
                       self.canvas.create_line(0,i*scale,nrow*scale,i*scale, fill="gray", width=1)
               self.canvas.pack()
               self.pixels = []
               self.gridmatrix = np.zeros((nrow,ncol))
        
        def random_pixels(self,num,c):
                for k in range(num):
                        i=random.randint(0,self.nrow-1)
                        j=random.randint(0,self.ncol-1)
                        self.addij(i,j,c)

        def addij(self,i,j,c):
               if c>0:
                pix=Pixel(self.canvas,i,j,self.nrow,self.ncol,self.scale,c)
                self.pixels=self.pixels+[pix]
                self.gridmatrix[i,j] = c

        def addxy(self,x,y):
                i=y//self.scale
                j=x//self.scale
                print("insert %s %s %s %s %s"%(x,y,i,j,int(self.gridmatrix[i,j])))
                self.addij(i,j,1)
        
        def delij(self,i,j):
                if int(self.gridmatrix[i,j]) != 0:
                        self.gridmatrix[i,j] = 0
                self.reset()

        def delxy(self,x,y,c=1):
                i=y//self.scale
                j=x//self.scale
                print("delete %s %s %s %s %s"%(x,y,i,j,int(self.gridmatrix[i,j])))
                if int(self.gridmatrix[i,j])==0:
                        self.flush_row(i)
                else:
                        self.delij(i,j)

        def reset(self):
                for pix in self.pixels:
                        pix.delete()
                self.pixels.clear()
                for i in range(self.nrow): #this re displays all the pixels may be bad here but its here for now (would need to be placed where other reset calls are if problematic)
                       for j in range(self.ncol):
                              if self.gridmatrix[i,j]!=0:
                                     self.addij(i,j,int(self.gridmatrix[i,j]))

        def shift(self,i):
                self.gridmatrix[1:i+1,:]=self.gridmatrix[0:i,:]
                self.gridmatrix[0,:]=0
                self.reset()

        '''def flush_row(self,i): #instead of adding and deleting, draw the first three on each sides with correct diretions and call their next methods until theyre at the middle THEN delete them
                count=0
                while True:
                        if count<3:
                                self.addij(i,count,7)
                                self.addij(i,self.ncol-1-count,7)
                        elif count>=3 and count<=(self.ncol/2):
                                self.delij(i,count-3)
                                self.delij(i,self.ncol-(count-2))
                                self.addij(i,count,7)
                                self.addij(i,(self.ncol-1)-(count),7)
                        elif count>(self.ncol/2) and count<=(self.ncol/2)+2:
                                self.delij(i,self.ncol//2+1)
                                self.delij(i,self.ncol//2-2)
                        else:
                                self.delij(i,self.ncol//2)
                                self.delij(i,self.ncol//2-1)
                                self.shift(i)
                                break
                        count=count+1
                        self.canvas.update()
                        time.sleep(0.02)'''

        def flush_row(self,i):
                leftside=[]
                rightside=[]
                for a in range(3):
                        leftside=[Pixel(self.canvas,i,self.ncol-1-a,self.nrow,self.ncol,self.scale,7,[0,-1])]+leftside
                        rightside=rightside+[Pixel(self.canvas,i,a,self.nrow,self.ncol,self.scale,7,[0,1])]
                        self.delij(i,a)
                        self.delij(i,self.ncol-1-a)
                        self.canvas.update()
                        time.sleep(0.02)
                while leftside[0].j != rightside[2].j-1:
                        for pix in leftside:
                                pix.next()
                        for pix in rightside:
                                pix.next()
                        self.delij(i,leftside[0].j)
                        self.delij(i,rightside[2].j)
                        self.canvas.update()
                        time.sleep(0.02)
                leftside[0].delete()
                rightside[-1].delete()
                for a in range(2):
                        self.delij(i,leftside[a].j)
                        self.delij(i,rightside[-1*(a+1)].j)
                        leftside[-1*(a+1)].delete()
                        rightside[a].delete()
                        self.canvas.update()
                        time.sleep(0.02)
                self.shift(i)

#########################################################
############# Main code #################################
#########################################################

  
def main(): 
        
        ##### create a window, canvas 
        root = Tk()                # instantiate a tkinter window
        mesh = Grid(root,50,30,20) # instantiate a Grid object
        mesh.random_pixels(25,1) # generate 25 random (white) pixels in the Grid

        
        ####### Tkinter binding mouse actions
        root.bind("<Button-1>",lambda e:mesh.addxy(e.x,e.y))
        root.bind("<Button-3>",lambda e:mesh.delxy(e.x,e.y))
        

        root.mainloop() # wait until the window is closed
        

if __name__=="__main__":
        main()

