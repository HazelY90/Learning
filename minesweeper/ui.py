import tkinter as tk
from tkinter import messagebox
from game import Game

class Minesweeper:

    COLORS={          
            1: "blue",
            2: "green",
            3: "red",
            4: "darkblue",
            5: "darkred",
            6: "cyan",
            7: "black",
            8: "gray"
        }

    MODES={
        "easy":(9,9,10),
        "median":(16,16,40),
        "hard":(16,30,99),
        "professional":(20,30,126)
    }

    def __init__(self):
        self.root=tk.Tk()
        self.root.geometry("")
        self.root.title("Mine Sweeper")

        # create the menu bar
        self.menubar=tk.Menu()
        self.filemenu=tk.Menu(self.menubar,tearoff=0)
        self.filemenu.add_command(label="Restart",command=self.restart)
        self.menubar.add_cascade(menu=self.filemenu,label="File")

        self.modemenu=tk.Menu(self.menubar,tearoff=0)
        self.modemenu.add_command(label="Easy",command=self.easymode)
        self.modemenu.add_command(label="Median",command=self.medianmode)
        self.modemenu.add_command(label="Hard",command=self.hardmode)
        self.modemenu.add_command(label="Professional",command=self.professionalmode)
        self.menubar.add_cascade(menu=self.modemenu,label="Mode")

        self.root.config(menu=self.menubar)

        # create information labels
        self.topframe=tk.Frame(self.root)
        self.topframe.columnconfigure(0,weight=1)
        self.topframe.columnconfigure(1,weight=1)
        self.topframe.columnconfigure(2,weight=1)
        self.topframe.rowconfigure(0,weight=1)
        self.topframe.rowconfigure(1,weight=2)
        
        self.modelabel=tk.Label(self.topframe,text="Easy Mode",font=("Arial",14),bd=1,relief="ridge",width=26,padx=10, pady=5)
        self.modelabel.grid(row=0,column=0,columnspan=2)
        self.lifelabel=tk.Label(self.topframe,text="Lives:3",font=("Arial",14),bd=1,relief="ridge",width=12,padx=10, pady=5)
        self.lifelabel.grid(row=1,column=0)
        self.timelabel=tk.Label(self.topframe,text="Time: 00:00",font=("Arial",14),bd=1,relief="ridge",width=12,padx=10, pady=5)
        self.timelabel.grid(row=1,column=1)
        self.rebtn=tk.Button(self.topframe,text="Restart",width=10,font=("Arial",14),command=self.restart)
        self.rebtn.grid(row=0,column=2,padx=10)
        self.pausebtn=tk.Button(self.topframe,text="Pause",width=10,font=("Arial",14),command=self.pause_resume)
        self.pausebtn.grid(row=1,column=2,padx=10)
        
        self.topframe.pack(pady=10)

        #load pictures
        self.mine_img=[tk.PhotoImage(file="mine0.png"),tk.PhotoImage(file="mine1.png")]

        # create easy-mode mine area
        self.mode="easy"
        self.minearea=None
        self.easymode()

        # start showing time
        self.timer_id = None  
        self.update_timer()

        self.root.mainloop()

    def easymode(self):
        self.mode="easy"
        self.modelabel.config(text="Easy mode")
        self.create_minearea(*self.MODES[self.mode])
        self.newgame()

    def medianmode(self):
        self.mode="median"
        self.modelabel.config(text="Median mode")
        self.create_minearea(*self.MODES[self.mode])
        self.newgame()

    def hardmode(self):
        self.mode="hard"
        self.modelabel.config(text="Hard mode")
        self.create_minearea(*self.MODES[self.mode])
        self.newgame()
    
    def professionalmode(self):
        self.root.state('zoomed')
        self.mode="professional"
        self.modelabel.config(text="Professional mode")
        self.create_minearea(*self.MODES[self.mode])
        self.newgame()

    def create_minearea(self,m,n,k):
        # create the mine area.
        if self.minearea:
            self.minearea.destroy()
        self.minearea=tk.Frame(self.root)
        for i in range(m):
            self.minearea.rowconfigure(i,weight=1,uniform="rou_group")
        for j in range(n):
            self.minearea.columnconfigure(j,weight=1,uniform="column_group")
        self.buttons=[[] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                self.button=tk.Button(self.minearea,width=3, height=1,font=("Arial",14))
                self.button.grid(row=i,column=j)
                self.button.bind("<Button-1>", lambda event, r=i, c=j: self.opencell(r, c))
                self.button.bind("<Button-3>", lambda event, r=i, c=j: self.flagcell(r, c))
                self.buttons[i].append(self.button)
        self.minearea.pack(padx=30,pady=20)

    def newgame(self):          
        self.game=Game(*self.MODES[self.mode])
        self.lifelabel.config(text=f"Lives:{self.game.lives}")
        self.timelabel.config(text="Time: 00:00")
                        
    def opencell(self,i,j):
        if self.buttons[i][j]["state"] == "disabled" or self.buttons[i][j]["text"]=="🚩":
            return
        status,cells=self.game.check_status(i,j)
        if status=="lost":
            self.show_mines("fail")
            messagebox.showinfo("Failed!","Boom! Out of lives. Game Over.")
            return
        elif status=="revive":
            self.buttons[i][j].config(image=self.mine_img[1], width=36,height=32, relief="sunken")
            res=messagebox.askyesno("Hint!","Mine Hit! Spend a life to continue?")
            if res:
                self.game.resume()
                self.buttons[i][j].config(image="",text="",width=3,height=1,bg="SystemButtonFace",relief="raised",compound="none",state="normal")
                self.lifelabel.config(text=f"Lives:{self.game.lives}")
            else:
                self.show_mines("fail")
                messagebox.showinfo("Failed!","Better luck next time!")
                return
        else:
            for (r,c) in cells:   
                if self.game.boards[r][c]==0:
                    self.buttons[r][c].config(state="disabled",relief="sunken")
                else:
                    self.buttons[r][c].config(text=f"{self.game.boards[r][c]}",disabledforeground=self.COLORS[self.game.boards[r][c]],relief="sunken",state="disabled")
                
            if status=="win":
                self.show_mines("win")
                messagebox.showinfo("Congratulations!","Congratulations! You have won the game!")

    def flagcell(self,i,j):
        if self.buttons[i][j]["state"]=="disabled":
            return
        current_text = self.buttons[i][j]["text"]
        if current_text == "":
            self.buttons[i][j].config(text="🚩", fg="red")
        else:
            self.buttons[i][j].config(text="",fg="black")
   
    def show_mines(self,result):
        if result=="fail":
            for r,c in self.game.mines:
                self.buttons[r][c].config(image=self.mine_img[1], width=36,height=32, relief="sunken")
        else:
            for r,c in self.game.mines:
                self.buttons[r][c].config(image=self.mine_img[0], width=36,height=32, relief="sunken") 
    
    def update_timer(self):
        time=self.game.update_time()
        if time:
            self.timelabel.config(text=f"Time: {time}")
            self.timelabel.update_idletasks()
        self.timer_id = self.root.after(1000, self.update_timer)
    
    def pause_resume(self):
        if self.pausebtn['text']=="Pause":
            self.game.pause()
            self.timer_id=None
            self.pausebtn.config(text='Resume')
        else:
            self.game.resume()
            self.update_timer()
            self.pausebtn.config(text='Pause')

    def restart(self):
        m=self.MODES[self.mode][0]
        n=self.MODES[self.mode][1]
        for i in range(m):
            for j in range(n):
                self.buttons[i][j].config(image="",text="",width=3,height=1,bg="SystemButtonFace",relief="raised",compound="none",state="normal")
        self.newgame()
    
