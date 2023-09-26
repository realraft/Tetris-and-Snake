from tkinter import *
from Grid import Grid
from Pixel import Pixel
import time


### complete class Snake
            
class Snake(Grid):
    def __init__(self,root,obs=20,fruit=20,nrow=50,ncol=30,scale=20):
        self.obs = obs
        self.fruit=fruit
        super().__init__(root,nrow,ncol,scale)
        super().random_pixels(obs,1) #obs
        super().random_pixels(fruit,3) #fruit
        self.snake = [Pixel(self.canvas,nrow//2,ncol//2,nrow,ncol,scale,c=4,vector=[0,1])]
        self.__pause=False
        self.__game_over=False

    def is_there_fruit(self):
        for row in self.gridmatrix:
            if 3.0 in row:
                return True
        return False

    def next(self):
        for pix in self.snake:
            if self.gridmatrix[pix.i,pix.j]==-1.0:
                pix.right()
            elif self.gridmatrix[pix.i,pix.j]==-2.0:
                pix.up()
            elif self.gridmatrix[pix.i,pix.j]==-3.0:
                pix.left()
            elif self.gridmatrix[pix.i,pix.j]==-4.0:
                pix.down()

            if self.snake.index(pix)==0 and self.gridmatrix[self.snake[0].i,self.snake[0].j]<0:
                self.gridmatrix[self.snake[0].i,self.snake[0].j]=0.0
            pix.next()

        if self.gridmatrix[self.snake[-1].i,self.snake[-1].j]==3.0:
            self.snake=[Pixel(self.canvas,self.snake[0].i-self.snake[0].vector[0],self.snake[0].j-self.snake[0].vector[1],self.nrow,self.ncol,self.scale,c=5,vector=self.snake[0].vector)]+self.snake
            self.gridmatrix[self.snake[-1].i,self.snake[-1].j]=0.0
            self.reset()
            self.fruit=self.fruit-1
        elif not self.is_there_fruit():
            print("YOU WIN!")
            self.canvas.create_text(self.ncol*self.scale//2,self.nrow*self.scale//2,text="YOU WIN",fill="orange",font=("Arial 25 bold"))
            self.__game_over=True
        elif self.gridmatrix[self.snake[-1].i,self.snake[-1].j]==1.0:
            print("GAME OVER!")
            self.canvas.create_text(self.ncol*self.scale//2,self.nrow*self.scale//2,text="GAME OVER",fill="orange",font=("Arial 25 bold"))
            self.__game_over=True

    def right(self):
         if self.snake[-1].vector!=[0,1] and self.snake[-1].vector!=[0,-1]:
            self.snake[-1].vector=[0,1]
            self.gridmatrix[self.snake[-1].i,self.snake[-1].j]=-1.0

    def left(self):
         if self.snake[-1].vector!=[0,1] and self.snake[-1].vector!=[0,-1]:
            self.snake[-1].vector=[0,-1]
            self.gridmatrix[self.snake[-1].i,self.snake[-1].j]=-3.0

    def up(self):
         if self.snake[-1].vector!=[1,0] and self.snake[-1].vector!=[-1,0]:
            self.snake[-1].vector=[-1,0]
            self.gridmatrix[self.snake[-1].i,self.snake[-1].j]=-2.0

    def down(self):
         if self.snake[-1].vector!=[1,0] and self.snake[-1].vector!=[-1,0]:
            self.snake[-1].vector=[1,0]
            self.gridmatrix[self.snake[-1].i,self.snake[-1].j]=-4.0
    
    def is_pause(self):
        return self.__pause
    def pause(self):
        print("PAUSE")
        self.__pause = not self.__pause

    def is_game_over(self):
        return self.__game_over

#########################################################
############# Main code #################################
#########################################################
    

  
def main(): 
        
        ##### create a window, canvas 
        root = Tk() # instantiate a tkinter window
        python = Snake(root,20,20) #20 obstacles, and 20 fruits
        #python = Snake(root,5,5,25,25,30) # 5 obstacles/fruits, 25 row, 25 column, 30 scale
        
        
        ####### Tkinter binding mouse actions
        root.bind("<Right>",lambda e:python.right())
        root.bind("<Left>",lambda e:python.left())
        root.bind("<Up>",lambda e:python.up())
        root.bind("<Down>",lambda e:python.down())
        root.bind("<p>",lambda e:python.pause())
       
        while True:
            if not python.is_pause(): python.next()
            root.update()
            time.sleep(0.15)  # wait few second (simulation)
            if python.is_game_over(): break
            
        
        root.mainloop() # wait until the window is closed
        

if __name__=="__main__":
    main()

