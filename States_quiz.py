import pandas
import tkinter as tk
import random
from tkinter import messagebox
# from  time import sleep

GAME = True

class App(tk.Tk):
    def __init__(self, ) -> None:
        super().__init__()
        self.title('Quiz')
        self.geometry('600x400')
        data = pandas.read_csv('Book1.csv')
        self.d = data.to_dict()
        self.mon_list = list(self.d['Monument'].values())
        self.score = -1
        self.time = 130

        self.rowconfigure(0,weight=3)
        self.rowconfigure(1,weight=5)
        self.rowconfigure(2,weight=3)
        self.rowconfigure(3,weight=7)
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=5)
        self.columnconfigure(2,weight=1)
        
        self.head_frame = tk.LabelFrame(border=0,borderwidth=0,height=0)
        self.head_frame.grid(row=0,column=0,columnspan=3,sticky='new')
        
        self.score_label = tk.Label (self.head_frame,text = '0/10', font=('Helvetica',15,'bold'))
        self.score_label.grid(row=0,column=0)
        self.score_update()

        self.heading = tk.Label (self.head_frame,text = 'Quiz', font=('Helvetica',20,'bold')).grid(row=0,column=1)
        self.timer = tk.Label (self.head_frame,text = '1:30', font=('Helvetica',15,'bold'))
        self.timer.grid(row=0,column=2)
        self.timer_update()

        self.head_frame.columnconfigure(0,weight=1)
        self.head_frame.columnconfigure(1,weight=5)
        self.head_frame.columnconfigure(2,weight=1)
        
        self.ques = tk.Label(text= 'Map the following monument to its location',font=('Helvetica',10,'bold')).grid(row=1,column=0
        ,columnspan=3,sticky='new')

        self.frame1 = tk.LabelFrame(border=0,borderwidth=0)
        self.frame1.grid(row=2,column=0,columnspan=3,sticky='new')
        
        self.building = tk.Label(self.frame1,text ='Lets Start!',font = ('Helvetica',15,'bold'),relief='groove',width=12,
        height=2)
        self.building.grid(row=0 ,column=1,sticky='n',padx='10')
        self.prev = tk.Button(self.frame1,text ='Prev\n←',height=2).grid(row=1 ,column=0,sticky='se')
        self.next = tk.Button(self.frame1,text ='Next\n→',height=2,command=self.click_next).grid(row=1 ,column=2,sticky='sw') 
        self.label_update()

        self.frame1.rowconfigure(0,weight=1)
        self.frame1.rowconfigure(1,weight=1)
        self.frame1.columnconfigure(0,weight=5)
        self.frame1.columnconfigure(1,weight=3)
        self.frame1.columnconfigure(2,weight=5)

        self.frame2 = tk.LabelFrame()
        self.frame2.grid(row=3, column= 0 ,columnspan=3 ,sticky='nsew')
        self.create_options()

    def create_options(self):

        self.places = []
        for x,y in enumerate(self.d['Location'].values()):
            
            self.places.append(tk.Button(self.frame2, text=y,width=8,height=2,command= lambda c =x: self.click(c))) 
            
            if x < 5: 
                self.places[x].grid(row=0,column=x,padx =20,sticky='ew')
            else:
                self.places[x].grid(row=1,column = x-5,padx =10,sticky='ew')
        [self.frame2.columnconfigure(i,weight =1) for i in range(0,6)]
        [self.frame2.rowconfigure(i,weight =1) for i in range(0,1)]

    def click(self,x):
        # print(self.places)
        # global SELECTED
        self.places[x]['state'] ='disabled'
        l = list(self.d['Location'].values())
        self.SELECTED = l[x]
        self.option = x

    def click_next(self):
        temp = None
        for i,j in enumerate(self.d['Monument'].values()):
            if j == self.ch : temp = i
        if self.d['Location'][temp] == self.SELECTED:
            self.score_update()
            self.label_update()
        else:
            self.places[self.option]['state'] = 'active'
            self.label_update()

    def label_update(self):
        global GAME
        if not self.mon_list:
            ans = messagebox.askyesno(title='Game Over', message=f'You scored{self.score}!!\n Do u wish to play again')
            if not ans:
                GAME = False
            self.destroy()
        else:
            self.ch = random.choice(self.mon_list)
            self.mon_list.remove(self.ch)
            self.building.configure(text = self.ch)
        
    
    def score_update(self):
        global GAME
        self.score += 1
        v = str(self.score) + '/' + '10'
        self.score_label.configure(text= v)
        if self.score == 10:
            ans = messagebox.askyesno(title='Game Over' , message=f'You win!!\nDo u wish to play again?')
            if not ans:
                GAME = False
            self.destroy()

    def timer_update(self):
        global GAME
        self.time -= 1
        t = str(self.time//100) + ':' 
        t += str(self.time % 100) if len(str(self.time % 100))==2 else   '0' + str(self.time % 100)
        self.timer.configure(text=t)
        if self.time == 0:
            ans = messagebox.askyesno(title='Time Up' , message=f'You scored{self.score}!!\nDo u wish to play again?')
            if not ans:
                GAME = False
            self.destroy()
        self.after(1000,self.timer_update)



if __name__ == '__main__':
    while GAME:
        a = App()
        a.mainloop()
    # a.destroy()