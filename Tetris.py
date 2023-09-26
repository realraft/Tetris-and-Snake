from tkinter import *
from Grid import Grid
from Tetrominoes import Tetrominoes
import numpy as np
import time

        
### complete class Tetris

class Tetris(Grid):
    def __init__(self,root, nrow, ncol, scale):
        super().__init__(root, nrow, ncol, scale)
        self.block=None
        self.__pause=False
        self.__game_over=False

    def is_overlapping(self,ii,jj):
         try:
            for a in range(len(self.block.pattern_list[self.block.current])):
                for b in range(len(self.block.pattern_list[self.block.current][a])):
                    if self.block.pattern_list[self.block.current][a,b] !=0:
                        if self.gridmatrix[ii+a,jj+b] != 0:
                            return True
            return False
         except:
             return False

    def place(self):
        pat = self.block.pattern_list[self.block.current]
        self.block.delete()
        for a in range(len(pat)):
            for b in range(len(pat[a])):
                self.addij(self.block.i+a,self.block.j+b,pat[a,b])
        self.block=None

    def is_pause(self):
        return self.__pause
    def pause(self):
        print("PAUSE")
        self.__pause = not self.__pause

    def is_game_over(self):
        return self.__game_over
    def game_over(self):
         self.__game_over = not self.__game_over

    def next(self):
        if self.block==None: #create new block if there is not one already
            self.block=Tetrominoes.random_select(self.canvas,self.nrow,self.ncol,self.scale)
            Tetrominoes.activate(self.block)
        elif self.block.i+len(self.block.pattern_list[self.block.current])>=self.nrow: #check if at the bottom of the screen
            self.place()
        elif not self.is_overlapping(self.block.i+1,self.block.j):
            self.block.down()
        else:
            self.place()

        for i in range(self.nrow): # check for complete rows
            if 0 not in self.gridmatrix[i]:
                 self.flush_row(i)

        for i in range(3): #check top 3 rows 
            for pix in self.gridmatrix[i]:
                if int(pix)!=0:
                    print("GAME OVER!")
                    self.canvas.create_text(self.ncol*self.scale//2,self.nrow*self.scale//2,text="GAME OVER",fill="orange",font=("Arial 25 bold"))
                    self.game_over()

    def up(self):
        self.block.rotate()
    def left(self):
        if not self.block.j-1<0 and not self.is_overlapping(self.block.i,self.block.j-1):
            self.block.left()
    def right(self):
        if not self.block.j+len(self.block.pattern_list[0])>self.ncol-1 and not self.is_overlapping(self.block.i,self.block.j+1):
            self.block.right()
    def down(self):
        while self.block != None:
            self.next()
            

#########################################################
############# Main code #################################
#########################################################
    

    
def main():
    ##### create a window, canvas 
        root = Tk() # instantiate a tkinter window
        game=Tetris(root,36,12,25) 
        
        ####### Tkinter binding mouse actions
        root.bind("<Up>",lambda e:game.up())
        root.bind("<Left>",lambda e:game.left())
        root.bind("<Right>",lambda e:game.right())
        root.bind("<Down>",lambda e:game.down())
        root.bind("<p>",lambda e:game.pause())        

        while True:
            if not game.is_pause(): game.next()
            root.update()   # update the graphic
            time.sleep(0.25)  # wait few second (simulation)
            if game.is_game_over(): break
        
        root.mainloop() # wait until the window is closed


        

if __name__=="__main__":
    main()

