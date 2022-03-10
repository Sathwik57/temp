from threading import Thread
import tkinter as tk
from tkinter import messagebox, ttk
from  datetime import datetime
from tkinter.constants import ANCHOR

from pygame import mixer

#initialising pygame
# pygame.init()

#initialing pygame audio module and fectchin our alarm sound
mixer.init(42050, -16, 2, 2048)
alarm_sound = mixer.Sound('ALARM_CLOCK_MyAlarm.wav')

#class for base window
class App(tk.Tk):

    def __init__(self ) -> None:
        super().__init__()
        self.geometry('450x350')
        self.title('My Alarm')
        self.configure(bg = '#423F3E')
        
        #heading for app
        self.heading = tk.Label(self,text = 'Alarm Clock' ,bg='#c7ccd1', font = ('Arial', 20 , 'bold'))
        self.heading.grid(row= 0 , column = 1,sticky= 'ew')

        #grid configuration
        self.rowconfigure(0,weight= 1)
        self.rowconfigure(1,weight= 1)
        self.rowconfigure(2,weight= 1)
        self.columnconfigure(0,weight= 1)
        self.columnconfigure(1,weight= 1)
        self.columnconfigure(2,weight= 1)

        #creating button to open alarms window
        self.alarms = tk.Button(self, text='Alarms' ,width=7, borderwidth= 0 ,command=self.open_alarm)
        self.alarms.grid(row= 2, column = 0,sticky='e')
        self.exit = tk.Button(self, text='Exit' , borderwidth= 0 ,width = 7 ,command= self.destroy)
        self.exit.grid(row= 2, column = 2, sticky ='w' , padx= 20)

        #func to check for alarms  
        self.ring_alarm()

    #alarms window
    def open_alarm(self):

        #Alarms window, created as toplevel because only on Tk window is allowed
        win = tk.Toplevel()
        win.title('Alarms')
        win.geometry('400x300')

        win.rowconfigure(0, weight= 1)
        win.rowconfigure(1, weight= 5)
        win.rowconfigure(2, weight= 2)
        win.columnconfigure(0, weight= 5)
        win.columnconfigure(1, weight= 2)

        #creatind Label Frame for alarm setting options
        frame1 = tk.LabelFrame(win,text='Set Alarm')
        frame1.grid(row=1,column=0,sticky='ew')

        frame1.rowconfigure(0, weight= 2)
        frame1.rowconfigure(1, weight= 2)
        frame1.columnconfigure(0, weight= 2)
        frame1.columnconfigure(1, weight= 2)
        frame1.columnconfigure(2, weight= 1)

        #list box to display active alarms
        self.listval = tk.StringVar()
        self.l = tk.Listbox(win,listvariable=self.listval)
        self.l.grid(row =0, column=1,rowspan=2,sticky='ns',padx= 10,pady=5)
        self.list_update()

        self.hr_selected = tk.IntVar()
        self.min_selected = tk.IntVar()
        self.zone_selected = tk.StringVar()
        
        #hours label and combo box(drop down)
        h1 = ttk.Label(frame1 , text='Hrs')
        h1.grid(row=0,column=0,padx=10,sticky='w')
        h = ttk.Combobox(frame1, textvariable= self.hr_selected, width=5)
        h['values'] = [str(_) for _ in range(1,13)]
        h.grid(row=1,column=0,padx=10,pady=10)

        #Minutes label and combo box(drop down)
        m1 = ttk.Label(frame1 , text='Min')
        m1.grid(row=0,column=1,padx=10,sticky='w')
        m = ttk.Combobox(frame1, textvariable= self.min_selected, width=5)
        m['values'] = [str(_) for _ in range(0,60)]
        m.grid(row=1,column=1,padx=10,pady=10)

        z = ttk.Combobox(frame1, textvariable= self.zone_selected,width= 4,state= 'readonly' )
        z['values'] = ['AM', 'PM']
        z.current(0)
        z.grid(row=1,column=2,padx=10,pady=10)

        #Label frame for buttons, for organising purpose
        frame2 = tk.LabelFrame(win,borderwidth=0,border=0)
        frame2.grid(row=2,column=0)
        
        #Set alarm button
        self.set_alarm = tk.Button(frame2,text='Set Alarm',command=self.conf_alarm)
        self.set_alarm.grid(row= 0 ,column=0,padx=5)
        #exit button to close alarms window
        self.exit_but  = tk.Button(frame2,text='Exit',width=5,command=win.destroy).grid(row= 0 ,column=1,padx=5)

        #delete alarm button
        self.delete_alarm  = tk.Button(win,text='Delete Alarm',command=self.delete).grid(row= 2,column=1,padx=5)
        frame1.columnconfigure(0, weight= 1)
        frame1.columnconfigure(1, weight= 1)
        # self.state(win)
        win.mainloop()

    def delete(self):
        '''
        Deletes the alarm selected in the listbox and displays dialogbox    
            Parameters: None
            Return: None
        '''
        with open('Alarms.txt','r') as f:
                old_lines = f.readlines()
    
        with open('Alarms.txt','w') as f:
            for x,y in enumerate(old_lines):

                if y.rstrip('\n') != self.l.get(ANCHOR): 
                    f.write(y)
        answer = messagebox.showinfo(message= f'{self.l.get(ANCHOR)} deleted')
        self.list_update()     


    def conf_alarm(self):
        '''
        Sets alarm as per the time selected and stores in text file    
            Parameters: None
            Return: None
        '''
        l = [self.hr_selected.get(), self.min_selected.get() , self.zone_selected.get()]
        answer = messagebox.askyesno(title='Confirmation',message='Do you wish to save?')
        if answer:
            with open('Alarms.txt','a') as f:
                f.write(f'{l[0]}:{l[1]} {l[2]}\n')
            messagebox.showinfo(message=f'Alarm set at {l[0]}:{l[1]} {l[2]}')
            self.list_update()
            # self.open_alarm()

    def list_update(self):
        '''
        Fetches the stored alarms from alarm file and displays in listbox of alarms window     
            Parameters: None
            Return: None
        '''
        self.l.delete(0,'end')
        try:
            with open('Alarms.txt','r') as f:
                x = f.readlines()
            l=[ l1.rstrip('\n') for l1 in x]
        except FileNotFoundError:
            l = []
        if l:
            [self.l.insert('end',i) for i in l] 
        
    def ring_alarm(self):
        '''
        Continuosly checks alarms from alarms file and and calls ring fun at specified time     
            Parameters: None
            Return: None
        '''
        n = datetime.now()
        hour= n.strftime('%I:%M %p')
        try:
            with open('Alarms.txt','r') as f:
                x = f.readlines()
            l=[ l1.rstrip('\n') for l1 in x]
        except FileNotFoundError:
            l = []
        if l:
            for x in l:
                if 'AM' in x:
                    t = x.replace(' AM','')
                    am = 'AM'
                else:
                    t = x.replace(' PM','')
                    am = 'PM'
                now_time =t.split(':')
                fin_time=''
                for temp in now_time:
                    if len(temp)==1: temp = '0' + temp
                    fin_time = fin_time + temp +':'
                fin_time = fin_time[:-1] + ' '+ am 

                if fin_time == hour:
                    self.ring()

        self.after(200,self.ring_alarm)

    def stop1(self,x):
        '''
        Stops alarm playback sound and destroys alarm popup    
            Parameters: Alarm dialogbox
            Return: None
        '''
        mixer.Sound.stop(alarm_sound)
        x.destroy()

    def ring(self):                
        '''
        Plays music at specified time     
            Parameters: None
            Return: None
        '''
        mixer.Sound.play(alarm_sound,loops = -1)
        a_info = tk.Toplevel()
        a_info.title('Alarm')
        lab = tk.Label(a_info, text ='Alarm!!!', font=('Helvetica',15)).grid()
        lab1 = tk.Button(a_info, text ='Dismiss', font=('Helvetica',10),command= lambda: self.stop1(a_info)).grid()
        a_info.mainloop()
        # time.sleep(60)    

                    

#class for displaying time
class Digital_clock:
    def __init__(self,master) -> None:
        self.master =master
        self.time_frame =tk.LabelFrame(master,text='      Time:',font=('Helvetica',12,'bold'),border=0,borderwidth=0)
        self.time_frame.grid(row=1 ,column = 0,columnspan=3 , padx= 10)
        

        #time conversion to string 
        self.now = datetime.now()
        hrs = self.now.strftime('%I')
        min = self.now.strftime('%M')
        sec = self.now.strftime('%S')
        am = self.now.strftime('%p')

        #displaying time inside Label frame
        self.h = tk.Label(self.time_frame).grid(row=1,column=0,padx=10)
        self.hour = tk.Label(self.time_frame , text= hrs,relief='sunken' ,width= 5 ,height= 4,bg='#c7ccd1',font =('Helvetica',20,'bold'),)
        self.hour.grid(row=1 , column= 1,sticky='ew')
        self._ = tk.Label(self.time_frame , text= ':' ,width= 1 ,height= 4,font =('Helvetica',20,'bold'))
        self._.grid(row=1 , column= 2,sticky='e')
        self.min = tk.Label(self.time_frame , text= min,relief='sunken',width= 5 ,height= 4,bg='#c7ccd1',font =('Helvetica',20,'bold'))
        self.min.grid(row=1 , column= 3,padx=5,sticky='ew')
        self._1 = tk.Label(self.time_frame , text= ':' ,width= 1 ,height= 4,font =('Helvetica',20,'bold'))
        self._1.grid(row=1 , column= 4,sticky='w')
        self.sec = tk.Label(self.time_frame , text= sec,relief='sunken' ,bg='#c7ccd1',width= 5 ,height= 4,font =('Helvetica',20,'bold'))
        self.sec.grid(row=1 , column= 5,sticky='ew',padx=5)
        self.mid = tk.Label(self.time_frame , text= am ,relief='sunken' ,width= 4 ,height= 1,font =('Helvetica',13,'bold'))
        self.mid.grid(row=1 , column= 6,padx=5,sticky='e')
        self.h1 = tk.Label(self.time_frame).grid(row=1,column=7,padx=3)

        #empty label row to display gap b/w frame heading and time
        self.empty =tk.Label(self.time_frame).grid(row=0)
        self.empty1 =tk.Label(self.time_frame).grid(row=2)

        #row,column configuration of label frame
        self.time_frame.rowconfigure(0,weight= 1)
        self.time_frame.rowconfigure(1,weight= 1)
        self.time_frame.rowconfigure(1,weight= 1)        
        self.time_frame.columnconfigure(0,weight= 5)
        self.time_frame.columnconfigure(1,weight= 5)
        self.time_frame.columnconfigure(2,weight= 1)
        self.time_frame.columnconfigure(3,weight= 5)
        self.time_frame.columnconfigure(4,weight= 1)
        self.time_frame.columnconfigure(5,weight= 5)
        self.time_frame.columnconfigure(6,weight= 3)
        self.time_frame.columnconfigure(7,weight= 5)

        self.display_time()

    def display_time(self):
        '''
        Displays time    
            Parameters: None
            Return: None
        '''
        self.now = datetime.now()
        hrs = self.now.strftime('%I')
        min = self.now.strftime('%M')
        sec = self.now.strftime('%S')
        am = self.now.strftime('%p')
        self.hour.configure(text = hrs)
        self.min.configure(text = min)
        self.sec.configure(text = sec)
        self.mid.configure(text = am)
        self.master.after(200,self.display_time)
        
a = App()
clock = Digital_clock(a)
a.mainloop()
