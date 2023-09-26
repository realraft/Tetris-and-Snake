'''ECE 122 PROJECT 3 BY OWEN RAFTERY (33742773)'''

from tkinter import *
import time
import random

class Pixel:
    color=['black','white','yellow','red','blue','green','orange','purple','brown','cyan']

    def __init__(self,canvas,i,j,nrow=40,ncol=40,scale=20,c=3,vector=[0,0]):
        self.canvas=canvas
        self.nrow=nrow
        self.ncol=ncol
        self.scale=scale
        self.c=c
        self.seti(i)
        self.setj(j)
        self.rec=self.canvas.create_rectangle(self.j*self.scale, self.i*self.scale, self.j*self.scale+self.scale, self.i*self.scale+self.scale, fill=self.color[c],outline='gray')
        self.vector=vector
    
    def __str__(self):
        return "(%s,%s) %s"%(self.i,self.j,self.color[self.c])
    
    def seti(self,i):
        if i>(self.nrow-1):
            i=i%self.nrow
        self.i=i
    
    def setj(self,j):
        if j>(self.ncol-1):
            j=j%self.ncol
        self.j=j
    
    def next(self):
        #for i
        if self.i+self.vector[0]>(self.nrow-1):
            self.canvas.move(self.rec, 0, -1*self.scale*self.nrow+self.scale)
            self.i=0
        elif self.i+self.vector[0]<0:
            self.canvas.move(self.rec, 0, self.scale*self.nrow-self.scale)
            self.i=self.nrow-1
        else:
            self.canvas.move(self.rec, 0, self.vector[0]*self.scale)
            self.i=self.i+self.vector[0]
        
        # for j
        if self.j+self.vector[1]>(self.ncol-1):
            self.canvas.move(self.rec, -1*self.ncol*self.scale+self.scale, 0)
            self.j=0
        elif self.j+self.vector[1]<0:
            self.canvas.move(self.rec, self.ncol*self.scale-self.scale, 0)
            self.j=self.ncol-1
        else:
            self.canvas.move(self.rec, self.vector[1]*self.scale, 0)
            self.j=self.j+self.vector[1]
    
    def right(self):
        self.vector=[0,1]
    def left(self):
        self.vector=[0,-1]
    def up(self):
        self.vector=[-1,0]
    def down(self):
        self.vector=[1,0]
    
    def delete(self):
        self.canvas.delete(self.rec)

#################################################################
########## TESTING FUNCTION
#################################################################
def delete_all(canvas):
    canvas.delete("all")
    print("Delete All")


def test1(canvas,nrow,ncol,scale):
    print("Generate 10 points at random")
    random.seed(4) # for reproducibility
    for k in range(10):
        i=random.randint(0,nrow-1) 
        j=random.randint(0,ncol-1)
        c=random.randint(1,9)    # color number
        pix=Pixel(canvas,i,j,nrow,ncol,scale,c)
        print(pix)

def test2(canvas,nrow,ncol,scale):
    print("Generate 10 points at random (using modulo)")
    random.seed(5) # for reproducibility
    for k in range(10):
        i=random.randint(0,nrow-1)*34
        j=random.randint(0,ncol-1)*13
        ij=str(i)+","+str(j)
        c=random.randint(1,9)    # color number
        pix=Pixel(canvas,i,j,nrow,ncol,scale,c)
        print(ij,"->",pix)

        
def test3(root,canvas,nrow,ncol,scale):
    print("Move one point along a square")

    pix=Pixel(canvas,35,35,nrow,ncol,scale,3)
    pix.vector=[-1,0] # set up direction (up)
    for i in range(30):
        pix.next()       # next move in the simulation 
        root.update()    # update the graphic
        time.sleep(0.05) # wait in second (simulation)
        
    pix.vector=[0,-1] # set up new direction (left)
    for i in range(30):
        pix.next()       # next move in the simulation 
        root.update()    # update the graphic
        time.sleep(0.05) # wait in second (simulation)
        
    pix.vector=[1,0]   # set up new direction (down)
    for i in range(30):
        pix.next()       # next move in the simulation 
        root.update()    # update the graphic
        time.sleep(0.05) # wait in second (simulation)
        
    pix.vector=[0,1]    # set up new direction (right)
    for i in range(30):
        pix.next()       # next move in the simulation 
        root.update()    # update the graphic
        time.sleep(0.05) # wait in second (simulation)

    #delete point
    pix.delete()


  
def test4(root,canvas,nrow,ncol,scale):
    print("Move four point along a square")

    pixs=[]
    pixs.append(Pixel(canvas,35,35,nrow,ncol,scale,3,[-1,0]))
    pixs.append(Pixel(canvas,5,35,nrow,ncol,scale,4,[0,-1]))
    pixs.append(Pixel(canvas,5,5,nrow,ncol,scale,5,[1,0]))
    pixs.append(Pixel(canvas,35,5,nrow,ncol,scale,6,[0,1]))
    
    print("Starting coords")
    for p in pixs: print(p)

    for i in range(30):
        for p in pixs:
            p.next()       # next move in the simulation     
        root.update()      # update the graphic
        time.sleep(0.05)   # wait in second (simulation)

    print("Ending coords")
    for p in pixs:
        print(p)
        p.delete()


        
def test5(root,canvas,nrow,ncol,scale):
    print("Move one point any direction -use arrow commands")

    pix=Pixel(canvas,20,20,nrow,ncol,scale,2)

    ### binding used by test5
    root.bind("<Right>",lambda e:pix.right())
    root.bind("<Left>",lambda e:pix.left())
    root.bind("<Up>",lambda e:pix.up())
    root.bind("<Down>",lambda e:pix.down())

    ### simulation
    while True:
        pix.next()
        root.update()     # update the graphic
        time.sleep(0.05)  # wait in second (simulation)



        

###################################################
#################### Main method ##################
###################################################


def main():
       
        ##### create a window, canvas
        root = Tk() # instantiate a tkinter window
        nrow=40
        ncol=40
        scale=20
        canvas = Canvas(root,width=ncol*scale,height=nrow*scale,bg="black") # create a canvas width*height
        canvas.pack()

        ### general binding events to choose a testing function
        root.bind("1",lambda e:test1(canvas,nrow,ncol,scale))
        root.bind("2",lambda e:test2(canvas,nrow,ncol,scale))
        root.bind("3",lambda e:test3(root,canvas,nrow,ncol,scale))
        root.bind("4",lambda e:test4(root,canvas,nrow,ncol,scale))
        root.bind("5",lambda e:test5(root,canvas,nrow,ncol,scale))
        root.bind("<d>",lambda e:delete_all(canvas))
        
       
        
        root.mainloop() # wait until the window is closed
        
if __name__=="__main__":
    main()

