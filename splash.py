
# #############################################
# imports for the splash code functionality
# #############################################
import os
import pathlib
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import Canvas
from tkinter import font
import PIL
from tkinter import filedialog
from PIL import Image, ImageTk
import time
from tkinter import messagebox as mBox
import sqlite3

class splashScreen():
    '''
    The splashScreen class
    '''
    filename=[]
     
    def __init__(self):
        '''
        splashScreen constructor
        '''
        
        self.splash()
        

        
        
        #self.splashfrm.mainloop()
     
    def splash(self):
        '''
        The splash interface code
        '''
        self.root = tk.Tk()
        self.root.title('Accounting Cycle')
        self.root.resizable(0, 0)
        self.root.iconbitmap('./images/icon.ico')
        f = tk.Frame(self.root, highlightthickness=0).grid()
        self.image = Image.open("./images/black.jpg")
        self.image = self.image.resize((640,630), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image)
        label = tk.Label(self.root,image=self.image)
        label.place(x=0,y=0)
        canvas=Canvas(f, height=535, width=580, highlightthickness=0)
        canvas.create_image(0,-45,image = self.image, anchor = 'nw')
        canvas.create_text(290,40, text='ACCOUNTING CYCLE', font=("Times new roman bold",28),fill = 'white')
        canvas.create_text(290,90, text='FINANCIAL ACCOUNTING PROJECT', font=("Times New Roman bold",22),fill = 'white')
        canvas.create_text(180,160, text=' Course Instructor:\n\tMiss Saima Munawwar', font=("Times 10 bold",18),fill = 'white')
        canvas.create_text(470,145, text='CS Section : A', font=("Times 10 bold",18),fill = 'white')
        canvas.create_text(280,220, text='Group Members:', font=("Times 10 bold",20),fill = 'white')
        canvas.create_text(300,260, text='Name\t\t  Roll Number', font=("Times 10 bold",19),fill = 'white') 
        canvas.create_text(180,330, text='Abdul Rafay \nMuhammad Arsal \nMuhammad Osama \nBilal Nasir', font=("Times 10 bold",16),fill = 'white')
        canvas.create_text(420,330, text='18B-071-CS \n18B-115-CS \n18B-003-CS \n18B-078-CS', font=("Times 10 bold",15),fill = 'white')
        self.btn1 = tk.Button(f, text="Existing Database",command=lambda: self.Open())
        self.btn1_wind = canvas.create_window(290,440,anchor='center',window=self.btn1)
        self.btn2 = tk.Button(f, text="New Database", command=lambda: self.Create())
        self.btn2_wind = canvas.create_window(290,480,anchor='center',window=self.btn2)
        canvas.grid()
        self.root.eval('tk::PlaceWindow %s center' % self.root.winfo_toplevel())
        self.root.mainloop()

    
    def Open(self):
        global filename
        self.filename.clear()
        ftypes = [('database', '*.db'), ('All files', '*')]
        file_name = str(filedialog.askopenfilename(filetype=ftypes))
        self.filename.append(file_name)
        if len(file_name) == 0:
            return file_name
        else:
            self.root.quit()  # stops mainloop
            self.root.destroy()
            return file_name

    def Create(self):
        self.filename.clear()
        ftypes = [('database', '*.db'), ('All files', '*')]
        file_name = str(filedialog.asksaveasfilename(filetype=ftypes))
        self.filename.append(file_name)
        self.Data(file_name)
        self.root.quit()  # stops mainloop
        self.root.destroy()
        return file_name
        
    def Data(self,x):
        db = sqlite3.connect(x)
        con=db.cursor()
        con.execute('''CREATE TABLE IF NOT EXISTS journal (
    Transact      INT         PRIMARY KEY
                              NOT NULL,
    Date          DATETIME    NOT NULL,
    Time          DATETIME,
    Description   STRING (40) NOT NULL,
    DebitAccount              NOT NULL,
    DebitAmount   REAL        NOT NULL,
    CreditAccount             NOT NULL,
    CreditAmount  DECIMAL     NOT NULL,
    Posted        BOOLEAN     NOT NULL
                              DEFAULT (0) 
)''')

        con.execute('''CREATE TABLE IF NOT EXISTS ledger 
                    (Account INTEGER     NOT NULL, 
                    Transact INTEGER     KEY NOT NULL, 
                    Amount REAL    NOT NULL, 
                    Balance REAL    NOT NULL)''')

        con.execute('''CREATE TABLE IF NOT EXISTS chart 
                    (Account INTEGER PRIMARY KEY    NOT NULL, 
                    Name STRING(60)    NOT NULL, 
                    Type STRING(10)    NOT NULL,
                    Balance REAL       NOT NULL)''')

        db.commit()

        # Check if Chart of Accounts already set-up, may not be overwritten
        count = con.execute("SELECT count(Account) FROM chart")
        for row in count:
            tableFull = bool(row[0])
        if (not tableFull):
            db.execute('''INSERT INTO chart VALUES (101, "CASH", "DEBIT", 0),
                        (110, "RECEIVABLES","DEBIT",0),
                        (200, "PAYABLES","CREDIT",0), 
                        (300, "EQUITY","CREDIT",0),
                        (350, "OWNER'S DRAWING", "CREDIT",0),  
                        (400, "REVENUE","CREDIT",0),
                        (500, "EXPENSES","DEBIT",0)        
                        ''')
            db.commit()


        db.close()
        
    def on_OKkill(self):
        if len(self.filename)==0:
            mBox.showinfo("NO FILE SELECTED","Please select database you want to work on.")
        else:
            self.root.quit()     # stops mainloop
            self.root.destroy()
        
        
        
if __name__ == '__main__':
    spl = splashScreen()
    
