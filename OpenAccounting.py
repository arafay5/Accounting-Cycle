import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import messagebox as mBox
from tkinter import simpledialog
from tkinter import Scrollbar
from tkinter import Canvas
from tkinter import font
from PIL import Image, ImageTk
# other standard and third party imports
#    all 3rd party are pip installable
import sqlite3
import datetime as dt
import pytz 
import math as mt
import numpy as np
import sys
import os
import pathlib
import time

# Custom module imports
from AccountDB import AccountDB
import FormDialogs
from FormDialogs import insertJournalForm, insertChartForm
from FormDialogs import ReportFormats
from Tooltips import createToolTip, ToolTip
from ReportPreps import TrialBalance
import splash
from into_excel import dbtoexcel

 
class AccountingSystem():

    def __init__(self):
        '''
        Constructor Setup the Application
        '''
        # Create instance
        self.win = tk.Tk()
           
        # Add a title
        self.win.title("Open Accounting")
        self.win.iconbitmap("images/icon.ico")
        
        
        # Add a icon
        if not sys.platform.startswith('linux'):
            self.win.iconbitmap("images/icon.ico")
        self.win.config(bg='#748B99')
        self.win.resizable(0,0)
        # Initialize widgets
        self.createWidgets() 

    # -- Exit GUI cleanly -------------
    def _quit(self):
        self.win.quit()
        self.win.destroy()
        print('run is done, exited normally!')
        exit() 
        
    def do_showChart(self):
        self.scrolList3.delete(1.0,tk.END)
        listAll = AccountDB.getChartAccounts(self)
        for row in listAll:
            #self.do_formatedList(row) 
            self.scrolList3.insert(tk.END,row[0])
            self.scrolList3.insert(tk.END,'\t    ')
            mName = row[1]
            nameLength = len(mName)+(40-len(mName))
            mName = mName.ljust(nameLength)
            self.scrolList3.insert(tk.END,mName)
            self.scrolList3.insert(tk.END,'  ')
            mType = row[2]
            typeLength = len(row[2])+(12-len(row[2]))
            mType = mType.ljust(typeLength)
            self.scrolList3.insert(tk.END,mType)
            self.scrolList3.insert(tk.END,'\t') 
            mBalance = str(round(row[3],2))
            balanceLength = len(mBalance)+(8-len(mBalance))
            mBalance = mBalance.rjust(balanceLength)
            self.scrolList3.insert(tk.END,mBalance)
            self.scrolList3.insert(tk.END,'\n')
            
    def do_showLedger(self, account):   
        self.scrolList2.delete(1.0,tk.END)
        account = int(account)

        listAll = AccountDB.getLedgerAccount(self,account)
        for row in listAll:
            #self.do_formatedList(row) 
            self.scrolList2.insert(tk.END,row[0])
            self.scrolList2.insert(tk.END,'\t    ')
            mTransact = str(row[1])
            transactLength = len(mTransact)+(10-len(mTransact))
            mTransact = mTransact.ljust(transactLength)
            self.scrolList2.insert(tk.END,mTransact)
            self.scrolList2.insert(tk.END,'\t  ')
            mAmount = str(row[2])
            amountLength = len(mAmount)+(8-len(mAmount))
            mAmount = mAmount.ljust(amountLength)
            self.scrolList2.insert(tk.END,mAmount)
            self.scrolList2.insert(tk.END,'\t')
            mBalance = str(round(row[3],2))
            balanceLength = len(mBalance)+(8-len(mBalance))
            mBalance = mBalance.rjust(balanceLength)
            self.scrolList2.insert(tk.END,mBalance)
            self.scrolList2.insert(tk.END,'\n')
            
    def do_showJournal(self, jDates):
        '''
        Show formatted journal
        '''  
        self.scrolList1.delete(1.0,tk.END)
        listAll = AccountDB.getJournalEntries(self,jDates)
        for row in listAll:
            self.scrolList1.insert(tk.END,row[0])
            self.scrolList1.insert(tk.END,'\t')
            mDate  = row[1]
            dateLength = 10
            mDate = mDate.ljust(dateLength)
            self.scrolList1.insert(tk.END,mDate)
            self.scrolList1.insert(tk.END,'  ')
            mTime  = row[2]
            timeLength = 9
            mTime = mTime.ljust(timeLength)
            self.scrolList1.insert(tk.END,mTime)
            self.scrolList1.insert(tk.END,'  ')
            mDescription = row[3]
            descLength = len(row[3])+(30-len(row[3]))
            mDescription = mDescription.ljust(descLength)
            self.scrolList1.insert(tk.END,mDescription)
            self.scrolList1.insert(tk.END,'  \t')
            mdAccount = str(row[4])
            daccountLength = len(mdAccount)+(4-len(mdAccount))
            mdAccount = mdAccount.ljust(daccountLength)
            self.scrolList1.insert(tk.END,mdAccount)
            self.scrolList1.insert(tk.END,' ')
            mdAmount = str(round(row[5],2))
            damountLength = len(mdAmount)+(8-len(mdAmount))
            mdAmount = mdAmount.rjust(damountLength)
            self.scrolList1.insert(tk.END,mdAmount)
            self.scrolList1.insert(tk.END,'\t\t     ')
            mcAccount = str(row[6])
            caccountLength = len(mcAccount)+(4-len(mcAccount))
            mcAccount = mcAccount.ljust(caccountLength)
            self.scrolList1.insert(tk.END,mcAccount)
            self.scrolList1.insert(tk.END,'\t')
            mcAmount = str(round(row[7],2))
            camountLength = len(mcAmount)+(8-len(mcAmount))
            mcAmount = mcAmount.rjust(camountLength)
            self.scrolList1.insert(tk.END,mcAmount)
            self.scrolList1.insert(tk.END,'\n')
        
    def do_reptTransact(self, jTransact):
        '''
        Show formatted journal transaction
        font conversion factor is 7 = 10pt
        '''       
        self.win.update()
        self.tab4.focus_force()
        self.tabControl.update()
        self.tab4.lift(aboveThis=None)
        self.tabControl.update()
        transaction = AccountDB.getJournalTransact(self,jTransact)
        self.reportWin.delete("all")
        self.reportWin.configure(background='#B6C3CC')
        self.reportWin.create_text(5,18,anchor=tk.NW, text='Transaction'.upper(), fill="blue")
        self.reportWin.create_text(90,18,anchor=tk.NW, text='Date'.upper(), fill="blue")
        self.reportWin.create_text(140,18,anchor=tk.NW, text='Time'.upper(), fill="blue")
        self.reportWin.create_text(200,18,anchor=tk.NW, text='Description'.upper(), fill="blue")
        self.reportWin.create_text(522,18,anchor=tk.NW, text='Debit'.upper(), fill="blue")
        self.reportWin.create_text(606,18,anchor=tk.NW, text='Credit'.upper(), fill="blue")
        cline = 18
        cline = cline + 20
        self.reportWin.create_line(10,cline, 670,cline, fill="blue")
        cline = cline + 3
        self.reportWin.create_line(10,cline, 670,cline, fill="blue")
        for row in transaction:
            cline = cline + 13
            mTransact = str(row[0])
            transactLength = 16                # 16 x 7 = 112
            mTransact = mTransact.ljust(transactLength)
            self.reportWin.create_text(30,cline,anchor=tk.NW, text=mTransact, fill="#2A0800")
            mDate  = row[1]
            #mDate ="2018-10-24"
            dateLength = 11                # 11 x 7 = 77
            mDate = mDate.ljust(dateLength)
            self.reportWin.create_text(80,cline,anchor=tk.NW, text=mDate, fill="#2A0800")
            mTime  = row[2]
            #mTime = "12:40:00"
            timeLength = 9                  # 9 x 7 = 63
            mTime = mTime.ljust(timeLength)
            self.reportWin.create_text(140,cline,anchor=tk.NW, text=mTime, fill="#2A0800")
            mDescription = row[3]
            #mDescription ="Pay bills"       # 30 x 9 = 270
            descLength = len(mDescription)+(30-len(mDescription))
            mDescription = mDescription.ljust(descLength)
            self.reportWin.create_text(200,cline,anchor=tk.NW, text=mDescription, fill="#2A0800")
            mdAccount=row[4].split(",")
            lcline = cline
            if len(mdAccount) > 1:
                for i in range(len(mdAccount)):
                    dAccount = str(mdAccount[i])
                    #mdAccount = "100"               # 4 x 7 =28
                    daccountLength = len(dAccount)+(4-len(dAccount))
                    dAccount = dAccount.ljust(daccountLength)
                    self.reportWin.create_text(522,lcline,anchor=tk.NW, text=dAccount, fill="#2A0800")
                    a=AccountDB.get_transact_balance(self,dAccount,mTransact)
                    mdAmount = str(abs(a[0][0]))
                    #mdAmount = "-24.91 "            # 8 x 7 = 56
                    damountLength = len(mdAmount)+(8-len(mdAmount))
                    mdAmount = mdAmount.rjust(damountLength)
                    self.reportWin.create_text(550, lcline, anchor=tk.NW, text=mdAmount, fill="#2A0800")
                    lcline=lcline+13
            else:
                mdAccount = str(row[4])
                #mdAccount = "100"               # 4 x 7 =28
                daccountLength = len(mdAccount)+(4-len(mdAccount))
                mdAccount = mdAccount.ljust(daccountLength)
                self.reportWin.create_text(522,cline,anchor=tk.NW, text=mdAccount, fill="#2A0800")
                mdAmount = str(round(row[5],2))
                #mdAmount = "-24.91 "            # 8 x 7 = 56
                damountLength = len(mdAmount)+(8-len(mdAmount))
                mdAmount = mdAmount.rjust(damountLength)
                self.reportWin.create_text(550, cline, anchor=tk.NW, text=mdAmount, fill="#2A0800")
            mcAccount = row[6].split(",")
            rcline=cline
            if len(mcAccount) > 1:
                for i in range(len(mcAccount)):
                    cAccount=str(mcAccount[i])
                    caccountLength = len(mcAccount)+(4-len(mcAccount))
                    cAccount = cAccount.ljust(caccountLength)
                    self.reportWin.create_text(606,rcline,anchor=tk.NW, text=cAccount, fill="#2A0800")
                    a=AccountDB.get_transact_balance(self,cAccount,mTransact)
                    mcAmount = str(abs(a[0][0]))
                    #mcAmount = "-24.91 "
                    camountLength = len(mcAmount)+(8-len(mcAmount))
                    mcAmount = mcAmount.rjust(camountLength)
                    self.reportWin.create_text(634,rcline,anchor=tk.NW, text=mcAmount, fill="#2A0800")
                    rcline+=13
            else:
                mcAccount=str(row[6])
                caccountLength = len(mcAccount) + (4 - len(mcAccount))
                mcAccount = mcAccount.ljust(caccountLength)
                self.reportWin.create_text(606, cline, anchor=tk.NW, text=mcAccount, fill="#2A0800")
                mcAmount = str(round(row[7], 2))
                # mcAmount = "-24.91 "
                camountLength = len(mcAmount) + (8 - len(mcAmount))
                mcAmount = mcAmount.rjust(camountLength)
                self.reportWin.create_text(634, cline, anchor=tk.NW, text=mcAmount, fill="#2A0800")

            if cline != lcline:
                cline = cline+(lcline-cline-13)
            elif rcline != cline:
                cline = cline + (rcline-cline-13)
        cline = cline + 20
        self.reportWin.create_line(10,cline, 670,cline, fill="blue")
        cline = cline + 3
        self.reportWin.create_line(10,cline, 670,cline, fill="blue")

    def do_reptChart(self):
        '''
        '''        
        self.win.update()
        self.tab4.focus_force()
        self.tabControl.update()
        self.tab4.lift(aboveThis=None)
        self.tabControl.update()
        chartAcct=AccountDB.getChartAccounts(self)       
        self.reportWin.delete("all")
        self.reportWin.configure(background='#B6C3CC')
        self.reportWin.create_text(15,18,anchor=tk.NW, text='ACCOUNT', fill="blue")
        self.reportWin.create_text(100,18,anchor=tk.NW, text='ACCOUNT NAME', fill="blue")
        self.reportWin.create_text(420,18,anchor=tk.NW, text='TYPE', fill="blue")
        self.reportWin.create_text(495,18,anchor=tk.NW, text='BALANCE', fill="blue")
        cline = 18
        cline = cline + 20
        self.reportWin.create_line(10,cline, 670,cline, fill="blue")
        cline = cline + 3
        self.reportWin.create_line(10,cline, 670,cline, fill="blue")
        for row in chartAcct:
            cline = cline + 13
            maccount = str(row[0])        
            maccountLength = len(maccount)+(4-len(maccount))    # 4 x 7 =28
            maccount = maccount.ljust(maccountLength)
            self.reportWin.create_text(20,cline,anchor=tk.NW, text=maccount, fill="#2A0800")
            mDescription = row[1]
            descLength = len(mDescription)+(30-len(mDescription))
            mDescription = mDescription.ljust(descLength)
            self.reportWin.create_text(100,cline,anchor=tk.NW, text=mDescription.upper(), fill="#2A0800")
            mType = row[2]       
            mTypeLength = len(mType)+(8-len(mType))     # 6 x 7 = 42
            mType = mType.rjust(mTypeLength)
            self.reportWin.create_text(415,cline,anchor=tk.NW, text=mType, fill="#2A0800")
            mBalance = str(round(row[3],2))        
            mbalanceLength = len(mBalance)+(8-len(mBalance))     # 8 x 7 = 56
            mBalance = mBalance.rjust(mbalanceLength)
            self.reportWin.create_text(495,cline,anchor=tk.NW, text=mBalance, fill="#2A0800")
        cline = cline + 20
        self.reportWin.create_line(10,cline, 670,cline, fill="blue")
        cline = cline + 3
        self.reportWin.create_line(10,cline, 670,cline, fill="blue")
    

    
    def click_on_widget(self, widget, button=1):
        widget.focus_force()
        self.win.update()
        widget.event_generate("<Button-{}>".format(button))
        self.win.update()
    
    def do_balSheet(self):
        '''
        '''
        
        proceedAnswer = mBox.askyesno("Balance Sheet Report","This can take a while.\nPrepare report now?")
        if (proceedAnswer):
            debandcred = TrialBalance.trialBalance(self)
            if (debandcred[0]-debandcred[1]==0):
                ReportFormats.do_reptBalSheet(self)
            else:
                mBox.showinfo('Failed trial balance' , 'The Ledger appears to be out of balance. \n A balance sheet may have errors\nPerform a Trial Balance to Investigate')
    def do_LedgerAcct(self):
        '''
        '''
        proceedAnswer = mBox.askyesno("Ledger Account Report","Prepare report now?")
        pass
    
       
    def do_RevandExp(self):
        '''
        '''
        
        proceedAnswer = mBox.askyesno("Income Statement","Prepare report now?")
        if (proceedAnswer):
            debandcred = TrialBalance.trialBalance(self)
            if (debandcred[0]-debandcred[1]==0):
                ReportFormats.do_reptRevandExp(self)
            else:
                mBox.showinfo('Failed trial balance' , 'The Ledger appears to be out of balance. \nAn Income statment may have errors\nPerform a Trial Balance to Investigate')


    def do_trialBalance(self):
        '''
        Calculate net balances for each chart account and compare to Chart of 
        Account balances. If any do not agree, notify which are out and return results
        '''
        proceedAnswer = mBox.askyesno("Trial Balance Report","This can take a while.\nPerform a trail balance now?")
        if (proceedAnswer):
            ReportFormats.do_reptTrialBalance(self)
        
    
    # #####################################
    # Create GUI Functions (Visualization)
    # #####################################   
    def createWidgets(self):
        '''
        Create the GUI interfaces
        '''
        # Messages and Dialogs -------------------------------------------
        def info(self):
            mBox.showinfo('About OpenAccounting, ' , 'Application to Perform Basic Accounting functions.\n\n. Project by Abdul Rafay \n Muhammad Arsal \n Osama Yousuf \n Bilal Nasir ')

        def fetchLedgerAccount(self):
            answer = simpledialog.askstring("Get Ledger Account", "What Account Number to retrieve?\n Enter '0' for ALL\n", parent=self.win)
            if answer is not None:
                ReportFormats.do_reptLedger(self,answer)
            else:
                print("No Value entered")
                return 0
            
        def getJournalDates(self):
            answer = simpledialog.askstring("Get Journal Range", "Start and End Date for Journal Retrieval\n, a comma separated pair. \n Enter '0,0' for ALL\n", parent=self.win)
            if answer is not None:
                jDates = (answer,)
                self.do_showJournal((jDates))
            else:
                print("No Value entered")
                return 0
        
        def getTransact(self):
            answer = simpledialog.askstring("Get Transaction", "Transaction to retrieve?\n\nEnter a Transaction Number\n Enter '0' for ALL \n", parent=self.win)
            if answer is not None:
                jTransact = (answer)
                self.do_reptTransact(jTransact)                
            else:
                print("No Value entered")
                return 0

            
        # Tab Controls created here --------------------------------------
        style = ttk.Style()
        style.configure("TNotebook", background='#748B99')
        self.tabControl = ttk.Notebook(self.win,style="TNotebook")     # Create Tab Controls

        self.tab1 = tk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text='Journal')
        self.tab1.config(bg='#748B99')
        
        self.tab3 = tk.Frame(self.tabControl)
        self.tabControl.add(self.tab3, text='Chart of Accounts')
        self.tab3.config(bg='#748B99')
        
        self.tab4 = tk.Frame(self.tabControl)
        self.tab4.config(bg='#748B99')
        self.tabControl.add(self.tab4, text='Views and Reports')
        style_bu = ttk.Style()
        # style_bu.theme_use('clam')
        style_bu.configure('TButton', background='#2A0800')
        style_bu.configure('TButton', foreground='black')

        self.tabControl.grid()  # Pack to make visible
        
        frm1 = tk.LabelFrame(self.tab1, text='General Journal', width= 650, height=600)
        frm1.grid()
        frm1.config(bg='#748B99')
        style_gen = ttk.Style()
        style_gen.configure("BW.TLabel", foreground="#2A0800", background='#748B99')
        ttk.Label(frm1, text="The General Journal is the book of first entry in the accounting system. It is accessed directly in the course of recording the daily activities of the enterprise.\n All other related books are accessible as appropriate for addition and update from the general journal.", style='BW.TLabel').grid(column=0, row=0, padx=4, pady=4,sticky='W')
        frm1a = tk.LabelFrame(frm1, width= 550, height=500)
        frm1a.grid(column=0,row=1)
        frm1a.config(bg='#B6C3CC')
        jDates = (0,0)
        self.updateJournal = ttk.Button(frm1a, text="Update Display",style="TButton", command=lambda: self.do_showJournal(jDates)).grid(column=0,row=1,padx=4, pady=4)
        self.newEntry = ttk.Button(frm1a, text="New Entry",style="TButton", command=lambda: insertJournalForm(self)).grid(column=2,row=1,padx=4, pady=4)
        ttk.Label(frm1, text="Transact\t    Date\t\t        Time\t\tDescription\t\t\tDebit:   Account    Amount\t   Credit:  Account    Amount",style="BW.TLabel").grid(column=0, row=2, padx=4, pady=4,sticky='W')
        scrolW1  = 100; scrolH1  =  35
        self.scrolList1 = scrolledtext.ScrolledText(frm1, width=scrolW1, height=scrolH1, wrap=tk.WORD)
        self.scrolList1.grid(column=0, row=3, padx=4, pady=4, sticky='WE', columnspan=3)
        self.scrolList1.config(bg='#B6C3CC')
        self.do_showJournal((0,0))

        
        ## Set tab and contents for the Chart of Accounts
        frm3 = tk.LabelFrame(self.tab3, text='Chart of Accounts', width= 650, height=600)
        frm3.grid()
        frm3.config(bg='#748B99')
        ttk.Label(frm3, text="The Chart of Accounts is the organizing principle of the accounting system. It is accessed directly in defining the business\n activities for the of the enterprise.\n\n At system initialization the basic default accounts are automatically configured. Subsequently the chart is accessible as\n needed to set up new customer and supplier accounts for ongoing operation of the business",style='BW.TLabel').grid(column=0, row=0, padx=4, pady=4,sticky='W')
        frm3a = tk.LabelFrame(frm3, width= 400, height=450)
        frm3a.grid(column=0,row=1)
        frm3a.config(bg='#748B99')
        self.updateChart = ttk.Button(frm3a, text="Update Display",style="TButton", command=lambda: self.do_showChart()).grid(column=0,row=0,padx=4, pady=4)
        #self.printChart = ttk.Button(frm3a, text="PRINT", command=lambda: notImplementedInfo(self)).grid(column=1,row=0,padx=4, pady=4)
        self.newAccount = ttk.Button(frm3a, text="New Account",style="TButton", command=lambda: insertChartForm(self)).grid(column=2,row=0,padx=4, pady=4)
        style_gen = ttk.Style()
        style_gen.configure("BW.TLabel", foreground="#2A0800", background='#748B99')
        ttk.Label(frm3, text="Account \t Name \t\t\t\t\t\t\tType\t\tBalance",style="BW.TLabel").grid(column=0, row=2, padx=4, pady=4,sticky='W')
        scrolW1= 80; scrolH1=32
        self.scrolList3 = scrolledtext.ScrolledText(frm3, width=scrolW1, height=scrolH1, wrap=tk.WORD)
        self.scrolList3.grid(column=0, row=3, padx=4, pady=4, sticky='W', columnspan=3)
        self.scrolList3.config(bg='#B6C3CC')
        self.do_showChart()
        
        frm4 = tk.LabelFrame(self.tab4, text='Accounting Reports', width= 800, height=590)
        frm4.grid(padx=8, pady=4)
        frm4.config(bg='#748B99')
        self.reportctl = tk.LabelFrame(frm4, text = "List of Reports")
        self.reportctl.grid(column=0, row=0, padx=8, pady=4, sticky='W')
        self.reportctl.config(bg='#748B99')

        frm4b = tk.Frame(frm4, width= 700, height=450)
        frm4b.grid(column=0, row=3)
        frm4b.config(bg='#748B99')
        self.action_balanceSheet = ttk.Button(self.reportctl, text="Balance Sheet",style="TButton", command=lambda: self.do_balSheet())
        self.action_balanceSheet.grid(column=6, row=0, padx=4, pady=6)
        self.action_journalReport = ttk.Button(self.reportctl, text="Journal Report",style="TButton", command=lambda: self.do_reptTransact(0))
        self.action_journalReport.grid(column=1, row=0, padx=4, pady=6)
        self.action_trialbalance = ttk.Button(self.reportctl, text="Trial Balance",style="TButton", command=lambda: self.do_trialBalance())
        self.action_trialbalance.grid(column=3, row=0, padx=4, pady=6)
        self.action_ledgerAccount = ttk.Button(self.reportctl, text="Ledgers",style="TButton", command=lambda: fetchLedgerAccount(self))
        self.action_ledgerAccount.grid(column=2, row=0, padx=4, pady=6)
        self.action_listAccounts = ttk.Button(self.reportctl, text="List of Accounts",style="TButton", command=lambda: self.do_reptChart())
        self.action_listAccounts.grid(column=0, row=0, padx=4, pady=6)
        self.action_EquityStatement = ttk.Button(self.reportctl, text="Equity Statement",style="TButton", command=lambda: ReportFormats.do_reptequitystatement(self))
        self.action_EquityStatement.grid(column=5, row=0, padx=4, pady=6)
        self.action_revenueExpense = ttk.Button(self.reportctl, text="Income Statement",style="TButton", command=lambda: self.do_RevandExp())
        self.action_revenueExpense.grid(column=4, row=0, padx=4, pady=6)
        self.action_closing = ttk.Button(self.reportctl, text="Closing Entries",style="TButton", command=lambda: ReportFormats.do_reptclosing(self))
        self.action_closing.grid(column=7, row=0, padx=4, pady=6)
        self.action_closing = ttk.Button(self.reportctl, text="Post Closing Trial Balance",style="TButton", command=lambda: ReportFormats.do_reptPostClosing(self))
        self.action_closing.grid(column=8, row=0, padx=4, pady=6)
        self.reportWin = Canvas(frm4b, width=700, height=550,bg='#B6C3CC',scrollregion=(0,0,1000,2000))
        hbar=Scrollbar(frm4b,orient=tk.HORIZONTAL)
        hbar.pack(side=tk.BOTTOM,fill=tk.X)
        hbar.config(command=self.reportWin.xview)
        vbar=Scrollbar(frm4b,orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT,fill=tk.Y)
        vbar.config(command=self.reportWin.yview)
        self.reportWin.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.reportWin.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)
               
        self.reportWin.create_text(10,10, anchor=tk.NW, text="Select a view or report, it will display here") 

        # meubar created here --------------------------------------------
        menuBar = Menu(self.win)
        self.win.config(menu=menuBar)
        # Add menu items
        
        # Add an Data entry Menu
        entryMenu = Menu(menuBar, tearoff=0)
        entryMenu.add_command(label="Journal Entry", command=lambda: insertJournalForm(self))
        entryMenu.add_command(label="New Account", command=lambda: insertChartForm(self))
        menuBar.add_cascade(label="Edit", menu=entryMenu)
        
        # Add an Data entry Menu
        viewMenu = Menu(menuBar, tearoff=0)
        viewMenu.add_command(label="View Journal", command=lambda: self.do_reptTransact(0))
        viewMenu.add_command(label="View Transaction", command=lambda: getTransact(self))
        viewMenu.add_command(label="View Accounts", command=lambda: self.do_reptChart())
        viewMenu.add_command(label="View Ledger", command=lambda: fetchLedgerAccount(self))
        viewMenu.add_separator()
        viewMenu.add_command(label="Trial Balance", command=lambda: self.do_trialBalance())
        menuBar.add_cascade(label="View", menu=viewMenu)
        
        # Add an Edit Menu
        reportMenu = Menu(menuBar, tearoff=0)
        reportMenu.add_command(label="Balance Sheet", command=lambda: self.do_balSheet())
        reportMenu.add_command(label="Ledger Account", command=lambda: fetchLedgerAccount(self))
        reportMenu.add_command(label="Income Report", command=lambda: self.do_RevandExp())
        reportMenu.add_command(label="Expense Report", command=lambda: self.do_RevandExp())
        menuBar.add_cascade(label="Reports", menu=reportMenu)
        #.db into excel
        excelMenu = Menu(menuBar, tearoff=0)
        excelMenu.add_command(label="Convert all tables", command=lambda: dbtoexcel.all_worksheets(self))
        excelMenu.add_command(label="Convert Ledger Account", command=lambda: dbtoexcel.worksheet2(self))
        excelMenu.add_command(label="Convert Journal Entries", command=lambda: dbtoexcel.worksheet0(self))
        excelMenu.add_command(label="Convert Chart of Accounts", command=lambda: dbtoexcel.worksheet1(self))
        menuBar.add_cascade(label="Convert DB to Excel", menu=excelMenu)



        
if __name__ == '__main__':

    spl = splash.splashScreen()
    asys = AccountingSystem()
    w = (2*asys.win.winfo_screenwidth())/3
    h = (3*asys.win.winfo_screenheight())/4
    asys.win.geometry("%dx%d+0+0" % (w+150, h))

    asys.win.eval('tk::PlaceWindow %s center' % asys.win.winfo_toplevel())
    asys.win.mainloop()
