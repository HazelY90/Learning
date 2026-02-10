import random
import time

class Game:
    def __init__(self,rows,cols,bombs):
        self.rows=rows
        self.cols=cols
        self.bombs=bombs
        self.safecells=rows*cols-bombs
        self.boards=[[0 for _ in range(cols)] for _ in range(rows)]
        self.mines=set()
        self.opened = [[False for _ in range(cols)] for _ in range(rows)]

        self.lives=3
        self.first_click=True

        self.time_running=False
        self.start_time=time.time()
        self.accumulate_time=0
        

    def generate_mines(self,r,c):

        # generate mines
        self.forbiddenzone=[(r-1,c-1),(r-1,c),(r-1,c+1),(r,c-1),(r,c),(r,c+1),(r+1,c-1),(r+1,c),(r+1,c+1)]

        while len(self.mines)<self.bombs:
            i=random.randint(0,self.rows-1)
            j=random.randint(0,self.cols-1)
            if (i,j) in self.forbiddenzone:
                continue
            else:
                self.boards[i][j]=-1
                # if the minecell is new, add count to the cells around it.
                if (i,j) not in self.mines:
                    rounds=[(i-1,j-1),(i-1,j),(i-1,j+1),(i,j-1),(i,j+1),(i+1,j-1),(i+1,j),(i+1,j+1)]
                    for r0,c0 in rounds:
                        if 0<=r0<self.rows and 0<=c0<self.cols and self.boards[r0][c0]!=-1:
                            self.boards[r0][c0]+=1           
                self.mines.add((i,j))
    
    def check_status(self,r,c):
        if self.first_click:
            self.generate_mines(r,c)
            self.first_click=False
            self.time_running=True
            self.start_time=time.time()
        visited=set()
        if self.boards[r][c]==-1 and self.lives==0:
            self.time_running=False
            status="lost"
            visited.add((r,c))
        elif self.boards[r][c]==-1:
            self.lives-=1
            self.pause()
            status= "revive"
            visited.add((r,c))
        else:
            status="continue"
            visited=self.cell_to_open(r,c,visited)
        if self.safecells==0:
            self.time_running=False
            status="win"
        
        return status,visited
            

    def cell_to_open(self,r,c,visited=None):
        
        if not visited:
            visited=set()
        if (r,c) in visited:
            return visited
        if not self.opened[r][c] and self.boards[r][c]!=-1:
            self.opened[r][c]=True
            self.safecells-=1        
        visited.add((r,c))
        
        if self.boards[r][c]==0:
            for dr in [-1,0,1]:
                for dc in [-1,0,1]:
                    if dr==0 and dc==0:
                        continue
                    if 0 <= (r+dr) < self.rows and 0 <= (c+dc) < self.cols:
                        self.cell_to_open(r+dr,c+dc,visited)
        return visited
                 
    def update_time(self):
        if self.time_running:
            seconds=int(time.time()-self.start_time+self.accumulate_time)
            minutes=seconds//60
            seconds=seconds%60
            t=f"{minutes:02d}:{seconds:02d}"
            return t
        return None


    def pause(self):
        seconds=time.time()-self.start_time+self.accumulate_time
        self.accumulate_time=seconds
        self.time_running=False

    
    def resume(self):
        self.start_time=time.time()
        self.time_running=True


