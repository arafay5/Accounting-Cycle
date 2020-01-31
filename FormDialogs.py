
# ######################################
# Imports
# ######################################
import tkinter as tk
from tkinter import ttk, LabelFrame
from tkinter import scrolledtext
from tkinter import Canvas
from tkinter import font
from PIL import Image, ImageTk
from tkcalendar import *
from  tkinter import messagebox
 

import math as mt
import numpy as np
import datetime as dt
import pytz

from AccountDB import AccountDB
from Tooltips import createToolTip
import os 
import pathlib
# #######################################################
# Classes, Independently constructed Forms, Dialogs etc
# #######################################################
'''
Classes, External, independently constructed Forms, Dialogs etc
'''



        
        
class insertJournalForm(object):

    here = pytz.timezone('Etc/GMT+5')
    currentDT = dt.datetime.now()
    entry =[5]
    centry =[20]
    def __init__(self, goal):
        '''
        Constructor for Add to Journal in it's own pop-up data dialog window
        '''
        
        # Create instance
        self.goal =goal
        self.frm = tk.Tk()
        self.frm.config(bg='#23343F')
        # Add a title
        self.frm.title("Insert a Journal Entry")
        self.frm.resizable(0,0)
        self.journalForm()
        self.frm.mainloop() 

        

    def journalForm(self):
        self.acct_num1 = []
        self.amt1 = []
        self.acct_num2 = []
        self.amt2 = []
        self.entry = [5]
        self.centry = [20]
        def AddDebit():

            self.entry[0 ] =self.entry[0 ] +1
            self.lbl4 = tk.Label(lbfr, text="Debit Account").grid(column=0, row=self.entry)
            accts =AccountDB.getchartaccts(self)
            self.variable1 = tk.StringVar(lbfr)
            self.variable1.set(accts[0])  # default value

            self.e4 = tk.OptionMenu(lbfr, self.variable1, *accts , command=self.func)
            self.e4.grid(column=1, row=self.entry, padx=5, pady=4, sticky='W')
            self.acct_num1.append(self.variable1)
            dAcctsEnter = 'Account to Debit'
            createToolTip(self.e4, dAcctsEnter)
            self.entry[0] = self.entry[0] + 1
            self.lbl5 = tk.Label(lbfr,  text="Debit Amount").grid(column=0, row=self.entry)
            deb_amount = tk.StringVar(lbfr)
            self.e5 = tk.Entry(lbfr, width=8, textvariable=deb_amount)
            self.e5.grid(column=1, row=self.entry, padx=5, pady=4, sticky='W')
            self.amt1.append(deb_amount)
            dAmtEnter = 'Amount to debit, dollars and cents, no not include sign, will be added by system'
            createToolTip(self.e5, dAmtEnter)

        def AddCredit():
            self.centry[0 ] =self.centry[0 ] +1
            self.lbl6 = tk.Label(lbfr,  text="Credit Account").grid(column=0, row=self.centry)
            accts =AccountDB.getchartaccts(self)
            self.variable2 = tk.StringVar(lbfr)
            self.variable2.set(accts[0])  # default value

            self.e6 = tk.OptionMenu(lbfr, self.variable2, *accts , command=self.func)
            self.e6.grid(column=1, row=self.centry, padx=5, pady=4, sticky='W')
            self.acct_num2.append(self.variable2)
            cAcctEnter = 'Account to Credit'
            createToolTip(self.e6, cAcctEnter)
            # -------------------------------------------------------------
            self.centry[0] = self.centry[0] + 1
            self.lbl7 = tk.Label(lbfr, text="Credit Amount").grid(column=0, row=self.centry)
            cred_amount =tk.StringVar(lbfr)
            self.e7 = tk.Entry(lbfr, width=8 , textvariable=cred_amount)
            self.e7.grid(column=1, row=self.centry, padx=5, pady=4, sticky='W')
            self.amt2.append(cred_amount)
            cAmtEnter = 'Amount to credit, dollars and cents, no not include sign, will be added by system'
            createToolTip(self.e7, cAmtEnter)

        ''' 
        The form for journal access for anew transaction entry
        '''
        # Whole form label frame---------------------------------------
        transaction =[0]
        lbfr = tk.LabelFrame(self.frm, text=' Input Form ')
        lbfr.grid(column=0, row=0, padx=10, pady=10, sticky='W')
        lbfr.config(bg='#B6C3CC')
        # Transaction Entry field -------------------------------------
        self.lbl0 = tk.Label(lbfr, text="Transaction").grid(column=0, row=0)
        self.e0 = tk.Entry(lbfr, width=16)
        self.e0.grid(column=1, row=0, padx=5, pady=4, sticky='W')
        transEnter = 'Unique transaction ID number. Is all numeric'
        createToolTip(self.e0, transEnter)
        # -------------------------------------------------------------
        self.lbl1 = tk.Label(lbfr, text="Date").grid(column=0, row=1)
        self.e1 = DateEntry(lbfr, width=10 ,date_pattern='yyyy-M-dd')
        self.e1.grid(column=1, row=1, padx=5, pady=4, sticky='W')
        dateEnter = 'Date  transaction entered, yyyy-mm-dd, defaults to today, '
        createToolTip(self.e1, dateEnter)
        # -------------------------------------------------------------
        self.lbl2 = tk.Label(lbfr, text="Time").grid(column=0, row=2)
        self.e2 = tk.Entry(lbfr, width=9)
        self.e2.grid(column=1, row=2, padx=5, pady=4, sticky='W')
        rtime = str(self.currentDT.hour) + ':' + str(self.currentDT.minute) + ':' + str(self.currentDT.second)
        self.e2.insert(0, rtime)
        timeEnter = 'Time transaction is entered. [hh:mm:ss] optional, defaults to Now'
        createToolTip(self.e2, timeEnter)
        # -------------------------------------------------------------
        self.lbl3 = tk.Label(lbfr, text="Description").grid(column=0, row=3)
        self.e3 = tk.Entry(lbfr, width=50)
        self.e3.grid(column=1, row=3, padx=5, pady=4, sticky='W')
        descEnter = 'Transaction Description.'
        createToolTip(self.e3, descEnter)

        # -------------------------------------------------------------
        style_bu = ttk.Style()
        # style_bu.theme_use('clam')
        style_bu.configure('TButton',background='blue')
        style_bu.configure('TButton',foreground='black')
        self.btn3 = ttk.Button(lbfr, text="Add Debit Amount",style="TButton", command=lambda: AddDebit()).grid(column=0, row=4, padx=5,
                                                                                               pady=4)
        dAmtEnter = 'Add debit account'

        self.btn4 = ttk.Button(lbfr, text="Add Credit Amount", command=lambda: AddCredit()).grid(column=0, row=20,
                                                                                                 padx=5, pady=4)
        dAmtEnter = 'Add Credit account'

        # --------------------------------------------------------------
        self.btn1 = ttk.Button(lbfr, text="Commit", command=lambda: self.on_click()).grid(column=0, row=50, padx=4,
                                                                                          pady=4, sticky='W')
        self.btn2 = ttk.Button(lbfr, text="Cancel", command=lambda: self.on_cancel()).grid(column=1, row=50, padx=4,
                                                                                           pady=4, sticky='W')

    def func(self, value):
        pass

    def on_click(self):
        '''
        Save new Journal Entry and update associated General Ledger accounts
        '''
        # get debit account balance
        if len(self.amt1)==0 and len(self.amt2)==0:
            messagebox.showwarning("Error !!", "Please enter credit and debit amounts.!")
        else:
            a=AccountDB.gettrasactionid(self)
            if int(self.e0.get()) in a:
                messagebox.showwarning("Error!!","Tansaction Id already exists,Please select any other id.")
            else:
                debits = []
                debit_amts = []
                credits = []
                credit_amts = []
                debitAmount = 0
                creditAmount = 0

                for length in range(len(self.acct_num1)):
                    a = self.acct_num1[length].get()
                    a = a.replace("(", "")
                    a = a.split(',')
                    y = self.amt1[length].get()
                    debits.append(a[0])
                    debit_amts.append(int(y))
                for length in range(len(self.acct_num2)):
                    c = self.acct_num2[length].get()
                    c = c.replace("(", "")
                    c = c.split(',')
                    credits.append(c[0])
                    ca = self.amt2[length].get()
                    credit_amts.append(int(ca))
                for i in credit_amts:
                    creditAmount = int(creditAmount) + int(i)
                for j in debit_amts:
                    debitAmount = int(debitAmount) + int(j)

                if (abs(creditAmount) == abs(debitAmount)):
                    posted = 1
                    jrow = (
                    int(self.e0.get()), self.e1.get(), self.e2.get(), self.e3.get(), ",".join(debits), debitAmount,
                    ",".join(credits),
                    creditAmount, posted)
                    AccountDB.insertJournalEntry(self, jrow)
                    for a in range(len(debits)):
                        daccount = int(debits[a])
                        txType = 'DEBIT'
                        debitBalance = AccountDB.getAccountBalance(self, daccount)
                        debitSgn = AccountDB.getsgnAdjust(self, daccount, txType)
                        debittAmount = debitSgn * round(float(debit_amts[a]), 2)
                        newDBalance = (debitBalance + debittAmount)
                        lDRow = (int(debits[a]), int(self.e0.get()), debittAmount, newDBalance)
                        lrow = lDRow
                        AccountDB.insertLedgerEntry(self, lrow)
                        AccountDB.updateChartBalance(self, daccount, newDBalance)

                    # get credit  account balance
                    for b in range(len(credits)):
                        caccount = int(credits[b])
                        txType = 'CREDIT'
                        creditBalance = AccountDB.getAccountBalance(self, caccount)
                        creditSgn = AccountDB.getsgnAdjust(self, caccount, txType)
                        credittAmount = creditSgn * round(float(credit_amts[b]), 2)
                        newCBalance = (creditBalance + credittAmount)
                        lCRow = (int(credits[b]), int(self.e0.get()), credittAmount, newCBalance)
                        lrow = lCRow
                        AccountDB.insertLedgerEntry(self, lrow)
                        AccountDB.updateChartBalance(self, caccount, newCBalance)

                    self.frm.destroy()
                else:
                    messagebox.showwarning("Error!!","Credits and Debits do not Balance")

    def on_cancel(self):
        print("Cancelled action")
        self.frm.destroy()


class insertChartForm(object):
    '''
    A form-dialog class insertion Form for building and display Chart of Account 
    access in it's own pop-up Dialog window

    '''

    def __init__(self, goal):
        '''
        Constructor for Add New Account dialog window
        '''

        # Create instance
        self.frm = tk.Tk()
        self.frm.config(bg='#23343F')
        # Add a title
        self.frm.title("Add Entry into Chart of Accounts")
        self.frm.resizable(0,0)
        self.chartForm()
        self.frm.mainloop()

    def chartForm(self):
        ''' 
        The form for Chart of Account access 
        '''
        # Whole form label frame --------------------------------------
        lbfr = tk.LabelFrame(self.frm, text=' Input Form ')
        lbfr.grid(column=0, row=0, padx=10, pady=10, sticky='W')
        lbfr.config(bg="#86c3cc")
        # -------------------------------------------------------------
        self.lbl0 = tk.Label(lbfr, text="Account Type").grid(column=0, row=0)
        self.Accounts = ["100: ASSETS ", "200: LIABILITIES", "300: OWNER'S EQUITY", "400: REVENUE ", "500: EXPENSES"]
        self.Accttype = tk.StringVar(lbfr)
        self.Accttype.set(self.Accounts[0])
        self.e0 = tk.OptionMenu(lbfr, self.Accttype, *self.Accounts)
        self.e0.grid(column=1, row=0, padx=5, pady=10, sticky='W')
        acctEnter = 'Number of the New Account being Opened'
        createToolTip(self.e0, acctEnter)

        # -------------------------------------------------------------
        self.lbl2 = tk.Label(lbfr, text="Name").grid(column=0, row=2)
        self.e2 = tk.Entry(lbfr, width=50)
        self.e2.grid(column=1, row=2, padx=5, pady=10, sticky='W')
        nameEnter = 'Name or Description of the new account'
        createToolTip(self.e2, nameEnter)
        # -------------------------------------------------------------

        # -------------------------------------------------------------        
        self.btn3 = ttk.Button(lbfr, text="Commit", command=lambda: self.on_click()).grid(column=0, row=7, padx=8,
                                                                                          pady=4, sticky='W')
        self.btn4 = ttk.Button(lbfr, text="Cancel", command=lambda: self.on_cancel()).grid(column=1, row=7, padx=8,
                                                                                           pady=4, sticky='W')

    def func(self, value):
        pass

    def on_click(self):
        account = self.Accttype.get()
        if account == self.Accounts[0]:
            a = AccountDB.highestaccount(self, 100, 199)
            account = int(a) + 5
            atype="DEBIT"

        elif account == self.Accounts[1]:
            a = AccountDB.highestaccount(self, 200, 299)
            account = int(a) + 5
            atype="CREDIT"

        elif account == self.Accounts[2]:
            a = AccountDB.highestaccount(self, 300, 399)
            account = int(a) + 5
            atype = "CREDIT"

        elif account == self.Accounts[3]:
            a = AccountDB.highestaccount(self, 400, 499)
            account = int(a) + 5
            atype = "CREDIT"

        elif account == self.Accounts[4]:
            a = AccountDB.highestaccount(self, 500, 599)
            account = int(a) + 5
            atype = "DEBIT"

        existAccount = AccountDB.existChartAccount(self, account)


        row = int(account), self.e2.get().upper(), atype, 0
        ''' the activation of the form'''
        if (not existAccount):
            print("commit")
            print(row)
            AccountDB.insertChartAccount(self, row)
            print("journalForm closed")
            self.frm.destroy()
        else:
            print("ERROR: An Account Already Exists with this Number")
            self.on_cancel()

    def on_cancel(self):
        print("Cancelled action")
        self.frm.destroy()


class ReportFormats():
    def do_reptclosing(self):
        self.win.update()
        self.tab4.focus_force()
        self.tabControl.update()
        self.tab4.lift(aboveThis=None)
        self.tabControl.update()
        chartAcct = AccountDB.getclosingentries(self, (400, 501))
        self.reportWin.delete("all")
        self.reportWin.create_text(335, 14, text='CLOSING ENTRIES', font=("Times 10 bold", 16))
        self.reportWin.create_text(40, 34, anchor=tk.NW, text='Description', fill="blue", font=("Times 10 bold", 11))
        self.reportWin.create_text(420, 34, anchor=tk.NW, text="Debit", fill="blue", font=("Times 10 bold", 11))
        self.reportWin.create_text(495, 34, anchor=tk.NW, text="Credit", fill="blue", font=("Times 10 bold", 11))
        cline = 37
        cline = cline + 20
        self.reportWin.create_line(10, cline, 670, cline, fill="blue")
        cline = cline + 3
        self.reportWin.create_line(10, cline, 670, cline, fill="blue")
        blockAcct = AccountDB.getBalSheetAccounts(self, (400, 499))
        incomeTotal = 0.0
        cline=80
        for row in blockAcct:
            incomeTotal = incomeTotal + float(row[3])
            cline = cline + 20
            mDescription = row[1]
            descLength = len(mDescription) + (30 - len(mDescription))
            mDescription = mDescription.ljust(descLength)
            self.reportWin.create_text(40, cline, anchor=tk.NW, text=mDescription)
            mBalance = str(round(row[3], 2))
            mbalanceLength = len(mBalance) + (8 - len(mBalance))  # 8 x 7 = 56
            mBalance = mBalance.rjust(mbalanceLength)
            self.reportWin.create_text(420, cline, anchor=tk.NW, text=mBalance)
        cline=cline + 20
        self.reportWin.create_text(100, cline, anchor=tk.NW, text='Income Summary'.upper())
        self.reportWin.create_text(495, cline, anchor=tk.NW, text=incomeTotal)
        blockAcct = AccountDB.getBalSheetAccounts(self, (500, 599))
        expenseTotal = 0.0
        for row in blockAcct:
            expenseTotal = expenseTotal + float(row[3])
        cline = cline + 40
        self.reportWin.create_text(40, cline, anchor=tk.NW, text='Income Summary'.upper())
        self.reportWin.create_text(420, cline, anchor=tk.NW, text=expenseTotal)

        for row in blockAcct:
            cline = cline + 20
            mDescription = row[1]
            descLength = len(mDescription) + (30 - len(mDescription))
            mDescription = mDescription.ljust(descLength)
            self.reportWin.create_text(100, cline, anchor=tk.NW, text=mDescription)
            mBalance = str(round(row[3], 2))
            mbalanceLength = len(mBalance) + (8 - len(mBalance))  # 8 x 7 = 56
            mBalance = mBalance.rjust(mbalanceLength)
            self.reportWin.create_text(495, cline, anchor=tk.NW, text=mBalance)
            retainedEarnings = incomeTotal - expenseTotal
        lcline=cline
        # get equity block
        blockAcct = AccountDB.getBalSheetAccounts(self, (300, 399))
        drawing=blockAcct[1][3]
        if retainedEarnings > 0:
            self.reportWin.create_text(40, cline+40, anchor=tk.NW, text='Income Summary'.upper())
            self.reportWin.create_text(420, cline+40, anchor=tk.NW, text=abs(retainedEarnings))
            self.reportWin.create_text(100, cline+60, anchor=tk.NW, text='Owner\'s Capital'.upper())
            self.reportWin.create_text(495, cline+60, anchor=tk.NW, text=abs(retainedEarnings))
        else:
            self.reportWin.create_text(40, lcline+40, anchor=tk.NW, text='Owner\'s Capital'.upper())
            self.reportWin.create_text(420, lcline+40, anchor=tk.NW, text=abs(retainedEarnings))
            self.reportWin.create_text(100, lcline+60, anchor=tk.NW, text='Income Summary'.upper())
            self.reportWin.create_text(495, lcline+60, anchor=tk.NW, text=abs(retainedEarnings))
        cline = cline + 100
        self.reportWin.create_text(40, cline, anchor=tk.NW, text='Owner\'s Capital'.upper())
        self.reportWin.create_text(420, cline, anchor=tk.NW, text=abs(drawing))
        cline = cline + 20
        self.reportWin.create_text(100, cline, anchor=tk.NW, text='Owner\'s Drawing'.upper())
        self.reportWin.create_text(495, cline, anchor=tk.NW, text=abs(drawing))
        cline = cline + 20
        self.reportWin.create_line(10, cline, 670, cline, fill="blue")
        cline = cline + 3
        self.reportWin.create_line(10, cline, 670, cline, fill="blue")

    def do_reptLedger(self, account):
        '''
        Report formating and data retrieval for Ledger account reports
        '''
        self.win.update()
        self.tab4.focus_force()
        self.tabControl.update()
        self.tab4.lift(aboveThis=None)
        self.tabControl.update()
        ledgerAcct = AccountDB.getLedgerAccount(self, account)
        self.reportWin.delete("all")
        self.reportWin.create_text(5, 18, anchor=tk.NW, text='Account'.upper(), fill="blue",font=("Times 10 bold",9))
        self.reportWin.create_text(70, 18, anchor=tk.NW, text='Transaction'.upper(), fill="blue",font=("Times 10 bold",9))
        # self.reportWin.create_text(150,18,anchor=tk.NW, text='Date')
        # self.reportWin.create_text(196,18,anchor=tk.NW, text='Time')
        self.reportWin.create_text(240, 18, anchor=tk.NW, text='Description'.upper(), fill="blue",font=("Times 10 bold",9))
        self.reportWin.create_text(500, 18, anchor=tk.NW, text='Amount'.upper(), fill="blue",font=("Times 10 bold",9))
        self.reportWin.create_text(570, 18, anchor=tk.NW, text='Balance'.upper(), fill="blue",font=("Times 10 bold",9))
        cline = 18
        cline = cline + 20
        self.reportWin.create_line(10, cline, 670, cline, fill="blue")
        cline = cline + 3
        self.reportWin.create_line(10, cline, 670, cline, fill="blue")
        for row in ledgerAcct:

            cline = cline + 13
            maccount = str(row[0])
            maccountLength = len(maccount) + (4 - len(maccount))  # 4 x 7 =28
            maccount = maccount.ljust(maccountLength)
            self.reportWin.create_text(20, cline, anchor=tk.NW, text=maccount, fill="#2A0800")
            mTransact = str(row[1])
            transactLength = 16  # 16 x 7 = 112
            mTransact = mTransact.ljust(transactLength)
            self.reportWin.create_text(95, cline, anchor=tk.NW, text=mTransact, fill="#2A0800")
            transact = AccountDB.getJournalTransact(self, mTransact)
            for line in transact:
                mDescription = line[3]
                descLength = len(mDescription) + (30 - len(mDescription))
                mDescription = mDescription.ljust(descLength)
                self.reportWin.create_text(170, cline, anchor=tk.NW, text=mDescription, fill="#2A0800")
            mAmount = str(round(row[2], 2))
            mamountLength = len(mAmount) + (8 - len(mAmount))  # 8 x 7 = 56
            mAmount = mAmount.rjust(mamountLength)
            self.reportWin.create_text(500, cline, anchor=tk.NW, text=mAmount, fill="#2A0800")
            mBalance = str(round(row[3], 2))
            mbalanceLength = len(mBalance) + (8 - len(mBalance))  # 8 x 7 = 56
            mBalance = mBalance.rjust(mbalanceLength)
            self.reportWin.create_text(570, cline, anchor=tk.NW, text=mBalance, fill="#2A0800")
        cline = cline + 20
        self.reportWin.create_line(10, cline, 670, cline, fill="blue")
        cline = cline + 3
        self.reportWin.create_line(10, cline, 670, cline, fill="blue")

    # def do_reptTransact(self, jTransact):
    #     '''
    #     Show formatted journal transaction
    #     font conversion factor is 7 = 10pt
    #     '''
    #     self.win.update()
    #     self.tab4.focus_force()
    #     self.tabControl.update()
    #     self.tab4.lift(aboveThis=None)
    #     self.tabControl.update()
    #     transaction = AccountDB.getJournalTransact(self, jTransact)
    #     self.reportWin.delete("all")
    #     self.reportWin.create_text(10, 18, anchor=tk.NW, text='Transaction: ', fill="blue")
    #     self.reportWin.create_text(60, 18, anchor=tk.NW, text='Date', fill="blue")
    #     self.reportWin.create_text(110, 18, anchor=tk.NW, text='Time', fill="blue")
    #     self.reportWin.create_text(160, 18, anchor=tk.NW, text='Description', fill="blue")
    #     self.reportWin.create_text(522, 18, anchor=tk.NW, text='Debit', fill="blue")
    #     self.reportWin.create_text(606, 18, anchor=tk.NW, text='Credit', fill="blue")
    #     cline = 18
    #     cline = cline + 20
    #     self.reportWin.create_line(10, cline, 670, cline, fill="blue")
    #     cline = cline + 3
    #     self.reportWin.create_line(10, cline, 670, cline, fill="blue")
    #     for row in transaction:
    #         cline = cline + 13
    #         mTransact = str(row[0])
    #         transactLength = 16  # 16 x 7 = 112
    #         mTransact = mTransact.ljust(transactLength)
    #         self.reportWin.create_text(30, cline, anchor=tk.NW, text=mTransact)
    #         mDate = row[1]
    #         # mDate ="2018-10-24"
    #         dateLength = 11  # 11 x 7 = 77
    #         mDate = mDate.ljust(dateLength)
    #         self.reportWin.create_text(60, cline, anchor=tk.NW, text=mDate)
    #         mTime = row[2]
    #         # mTime = "12:40:00"
    #         timeLength = 9  # 9 x 7 = 63
    #         mTime = mTime.ljust(timeLength)
    #         self.reportWin.create_text(110, cline, anchor=tk.NW, text=mTime)
    #         mDescription = row[3]
    #         # mDescription ="Pay bills"       # 30 x 9 = 270
    #         descLength = len(mDescription) + (30 - len(mDescription))
    #         mDescription = mDescription.ljust(descLength)
    #         self.reportWin.create_text(160, cline, anchor=tk.NW, text=mDescription)
    #         mdAccount = str(row[4])
    #         # mdAccount = "100"               # 4 x 7 =28
    #         daccountLength = len(mdAccount) + (4 - len(mdAccount))
    #         mdAccount = mdAccount.ljust(daccountLength)
    #         self.reportWin.create_text(522, cline, anchor=tk.NW, text=mdAccount)
    #         mdAmount = str(round(row[5], 2))
    #         # mdAmount = "-24.91 "            # 8 x 7 = 56
    #         damountLength = len(mdAmount) + (8 - len(mdAmount))
    #         mdAmount = mdAmount.rjust(damountLength)
    #         self.reportWin.create_text(550, cline, anchor=tk.NW, text=mdAmount)
    #         mcAccount = str(row[6])
    #         # mcAccount = "220"
    #         caccountLength = len(mcAccount) + (4 - len(mcAccount))
    #         mcAccount = mcAccount.ljust(caccountLength)
    #         self.reportWin.create_text(606, cline, anchor=tk.NW, text=mcAccount)
    #         mcAmount = str(round(row[7], 2))
    #         # mcAmount = "-24.91 "
    #         camountLength = len(mcAmount) + (8 - len(mcAmount))
    #         mcAmount = mcAmount.rjust(camountLength)
    #         self.reportWin.create_text(634, cline, anchor=tk.NW, text=mcAmount)
    #
    #     cline = cline + 20
    #     self.reportWin.create_line(10, cline, 670, cline, fill="blue")
    #     cline = cline + 3
    #     self.reportWin.create_line(10, cline, 670, cline, fill="blue")

    # def do_reptChart(self):
    #     '''
    #     '''
    #     self.win.update()
    #     self.tab4.focus_force()
    #     self.tabControl.update()
    #     self.tab4.lift(aboveThis=None)
    #     self.tabControl.update()
    #     chartAcct = AccountDB.getChartAccounts(self)
    #     self.reportWin.delete("all")
    #     self.reportWin.create_text(5, 18, anchor=tk.NW, text='Account')
    #     self.reportWin.create_text(56, 18, anchor=tk.NW, text='Description')
    #     self.reportWin.create_text(420, 18, anchor=tk.NW, text='Type')
    #     self.reportWin.create_text(485, 18, anchor=tk.NW, text='Balance')
    #     cline = 18
    #     cline = cline + 20
    #     self.reportWin.create_line(10, cline, 670, cline, fill="blue")
    #     cline = cline + 3
    #     self.reportWin.create_line(10, cline, 670, cline, fill="blue")
    #     for row in chartAcct:
    #         cline = cline + 13
    #         maccount = str(row[0])
    #         maccountLength = len(maccount) + (4 - len(maccount))  # 4 x 7 =28
    #         maccount = maccount.ljust(maccountLength)
    #         self.reportWin.create_text(10, cline, anchor=tk.NW, text=maccount)
    #         mDescription = row[1]
    #         descLength = len(mDescription) + (30 - len(mDescription))
    #         mDescription = mDescription.ljust(descLength)
    #         self.reportWin.create_text(56, cline, anchor=tk.NW, text=mDescription)
    #         mType = row[2]
    #         mTypeLength = len(mType) + (8 - len(mType))  # 6 x 7 = 42
    #         mType = mType.rjust(mTypeLength)
    #         self.reportWin.create_text(420, cline, anchor=tk.NW, text=mType)
    #         mBalance = str(round(row[3], 2))
    #         mbalanceLength = len(mBalance) + (8 - len(mBalance))  # 8 x 7 = 56
    #         mBalance = mBalance.rjust(mbalanceLength)
    #         self.reportWin.create_text(485, cline, anchor=tk.NW, text=mBalance)
    #     cline = cline + 20
    #     self.reportWin.create_line(10, cline, 670, cline, fill="blue")
    #     cline = cline + 3
    #     self.reportWin.create_line(10, cline, 670, cline, fill="blue")

    def do_reptRevandExp(self):
        '''
        '''
        # Fetch revenue accounts
        # Fetch Expense accounts

        # Get Balance totals for each account 

        # Display the Revenue and Expense accounts in a table
        self.reportWin.delete("all")
        self.reportWin.create_text(335, 12, text='INCOME STATEMENT',font=("Times 10 bold",16))
        self.reportWin.create_text(150, 38, anchor=tk.NW, text='Revenue'.upper(), fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(460, 38, anchor=tk.NW, text='Expenses'.upper(), fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(12, 55, anchor=tk.NW, text='Account'.upper(), fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(83, 55, anchor=tk.NW, text='Name'.upper(), fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(273, 55, anchor=tk.NW, text='Balance'.upper(), fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(344, 55, anchor=tk.NW, text='Account'.upper(), fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(410, 55, anchor=tk.NW, text='Name'.upper(), fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(605, 55, anchor=tk.NW, text='Balance'.upper(), fill='blue',font=("Times 10 bold",9))
        cline = 55
        cline = cline + 20
        self.reportWin.create_line(10, cline, 670, cline, fill="blue")
        cline = cline + 3
        self.reportWin.create_line(10, cline, 670, cline, fill="blue")
        # get assets block       
        blockAcct = AccountDB.getBalSheetAccounts(self, (400, 499))
        revenueTotal = 0.0
        for row in blockAcct:
            revenueTotal = revenueTotal + float(row[3])
            cline = cline + 13
            maccount = str(row[0])
            maccountLength = len(maccount) + (4 - len(maccount))  # 4 x 7 =28
            maccount = maccount.ljust(maccountLength)
            self.reportWin.create_text(20, cline, anchor=tk.NW, text=maccount, fill="#2A0800")
            mDescription = row[1]
            descLength = len(mDescription) + (30 - len(mDescription))
            mDescription = mDescription.ljust(descLength)
            self.reportWin.create_text(70, cline, anchor=tk.NW, text=mDescription, fill="#2A0800")
            mBalance = str(round(row[3], 2))
            mbalanceLength = len(mBalance) + (8 - len(mBalance))  # 8 x 7 = 56
            mBalance = mBalance.rjust(mbalanceLength)
            self.reportWin.create_text(273, cline, anchor=tk.NW, text=mBalance, fill="#2A0800")

            # get liabilities
        # get liability block       
        blockAcct = AccountDB.getBalSheetAccounts(self, (500, 599))
        expenseTotal = 0.0
        # reset cline to top right
        cline = 78
        for row in blockAcct:
            expenseTotal = expenseTotal + float(row[3])
            cline = cline + 13
            maccount = str(row[0])
            maccountLength = len(maccount) + (4 - len(maccount))  # 4 x 7 =28
            maccount = maccount.ljust(maccountLength)
            self.reportWin.create_text(354, cline, anchor=tk.NW, text=maccount, fill="#2A0800")
            mDescription = row[1]
            descLength = len(mDescription) + (30 - len(mDescription))
            mDescription = mDescription.ljust(descLength)
            self.reportWin.create_text(415, cline, anchor=tk.NW, text=mDescription, fill="#2A0800")
            mBalance = str(round(row[3], 2))
            mbalanceLength = len(mBalance) + (8 - len(mBalance))  # 8 x 7 = 56
            mBalance = mBalance.rjust(mbalanceLength)
            self.reportWin.create_text(605, cline, anchor=tk.NW, text=mBalance, fill="#2A0800")

        retainedEarnings = revenueTotal - expenseTotal

        cline = cline + 33
        self.reportWin.create_line(10, cline, 670, cline, fill="blue")
        cline = cline + 3
        self.reportWin.create_line(10, cline, 670, cline, fill="blue")
        cline = cline + 13
        # Revenue total
        mlTotal = str(round(revenueTotal, 2))
        mlTotalLength = len(mlTotal) + (10 - len(mlTotal))  # 8 x 7 = 56
        mlTotal = mlTotal.rjust(mlTotalLength)
        self.reportWin.create_text(265, cline, anchor=tk.NW, text=mlTotal, fill="#2A0800")
        # expense total
        mrTotal = str(round(expenseTotal, 2))
        mrTotalLength = len(mrTotal) + (10 - len(mrTotal))  # 8 x 7 = 56
        mrTotal = mrTotal.rjust(mrTotalLength)
        self.reportWin.create_text(598, cline, anchor=tk.NW, text=mrTotal, fill="#2A0800")

        cline = cline + 39
        '''maccount = str(399)        
        maccountLength = len(maccount)+(4-len(maccount))    # 4 x 7 =28
        maccount = maccount.ljust(maccountLength)
        self.reportWin.create_text(12,cline,anchor=tk.NW, text=maccount)'''
        mDescription = "NET INCOME"
        descLength = len(mDescription) + (30 - len(mDescription))
        mDescription = mDescription.ljust(descLength)
        self.reportWin.create_text(63, cline, anchor=tk.NW, text=mDescription, fill="#2A0800")
        mBalance = str(round(retainedEarnings, 2))
        mbalanceLength = len(mBalance) + (8 - len(mBalance))  # 8 x 7 = 56
        mBalance = mBalance.rjust(mbalanceLength)
        self.reportWin.create_text(273, cline, anchor=tk.NW, text=mBalance, fill="#2A0800")

    def do_reptBalSheet(self):
        '''
        '''
        # Fetch all Account Balances

        # Do trial Balances of each account, notify if any balances do not 
        #    agree with Chart of Account balances

        # Make and display the Balance Sheet
        self.reportWin.delete("all")
        self.reportWin.create_text(335, 12, text='BALANCE SHEET' , font=("TimesNewRoman",20))
        self.reportWin.create_text(150, 38, anchor=tk.NW, text='ASSETS'.upper(),font=("Times 10 bold",9),fill='blue')
        self.reportWin.create_text(460, 38, anchor=tk.NW, text='LIABILITIES'.upper(),font=("Times 10 bold",9), fill='blue')
        self.reportWin.create_text(12, 55, anchor=tk.NW, text='Account'.upper(), fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(80, 55, anchor=tk.NW, text='Name'.upper(), fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(273, 55, anchor=tk.NW, text='Balance'.upper(), fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(344, 55, anchor=tk.NW, text='Account'.upper(), fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(410, 55, anchor=tk.NW, text='Name'.upper(), fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(605, 55, anchor=tk.NW, text='Balance'.upper(), fill='blue',font=("Times 10 bold",9))
        cline = 55
        cline = cline + 20
        self.reportWin.create_line(10, cline, 670, cline, fill="blue")
        cline = cline + 3
        self.reportWin.create_line(10, cline, 670, cline, fill="blue")
        # get assets block       
        blockAcct = AccountDB.getBalSheetAccounts(self, (100, 199))
        assetTotal = 0.0
        for row in blockAcct:
            assetTotal = assetTotal + float(row[3])
            cline = cline + 13
            maccount = str(row[0])
            maccountLength = len(maccount) + (4 - len(maccount))  # 4 x 7 =28
            maccount = maccount.ljust(maccountLength)
            self.reportWin.create_text(20, cline, anchor=tk.NW, text=maccount, fill="#2A0800")
            mDescription = row[1]
            descLength = len(mDescription) + (30 - len(mDescription))
            mDescription = mDescription.ljust(descLength)
            self.reportWin.create_text(80, cline, anchor=tk.NW, text=mDescription, fill="#2A0800")
            mBalance = str(round(row[3], 2))
            mbalanceLength = len(mBalance) + (8 - len(mBalance))  # 8 x 7 = 56
            mBalance = mBalance.rjust(mbalanceLength)
            self.reportWin.create_text(273, cline, anchor=tk.NW, text=mBalance, fill="#2A0800")

        cline = cline + 20
        self.reportWin.create_line(265, cline, 325, cline, fill="blue")
        cline = cline + 13
        mTotal = str(round(assetTotal, 2))
        mTotalLength = len(mTotal) + (10 - len(mTotal))  # 8 x 7 = 56
        mTotal = mTotal.rjust(mTotalLength)
        self.reportWin.create_text(265, cline, anchor=tk.NW, text=mTotal, fill="#2A0800")

        # get liabilities
        # get liability block       
        blockAcct = AccountDB.getBalSheetAccounts(self, (200, 299))
        liabilityTotal = 0.0
        # reset cline to top right
        cline = 78
        for row in blockAcct:
            liabilityTotal = liabilityTotal + float(row[3])
            cline = cline + 13
            maccount = str(row[0])
            maccountLength = len(maccount) + (4 - len(maccount))  # 4 x 7 =28
            maccount = maccount.ljust(maccountLength)
            self.reportWin.create_text(354, cline, anchor=tk.NW, text=maccount, fill="#2A0800")
            mDescription = row[1]
            descLength = len(mDescription) + (30 - len(mDescription))
            mDescription = mDescription.ljust(descLength)
            self.reportWin.create_text(410, cline, anchor=tk.NW, text=mDescription, fill="#2A0800")
            mBalance = str(round(row[3], 2))
            mbalanceLength = len(mBalance) + (8 - len(mBalance))  # 8 x 7 = 56
            mBalance = mBalance.rjust(mbalanceLength)
            self.reportWin.create_text(605, cline, anchor=tk.NW, text=mBalance, fill="#2A0800")

        cline = cline + 20
        self.reportWin.create_line(598, cline, 663, cline, fill="blue")
        cline = cline + 13
        msTotal = str(round(liabilityTotal, 2))
        msTotalLength = len(msTotal) + (10 - len(msTotal))  # 8 x 7 = 56
        msTotal = msTotal.rjust(msTotalLength)
        self.reportWin.create_text(598, cline, anchor=tk.NW, text=msTotal, fill="#2A0800")

        cline = cline + 33
        self.reportWin.create_text(467, cline, anchor=tk.NW, text='Equity'.upper(),font=("Purisa",12) , fill='blue')

        cline = cline + 20
        self.reportWin.create_line(335, cline, 670, cline, fill="blue")
        cline = cline + 3
        self.reportWin.create_line(335, cline, 670, cline, fill="blue")

        # get income block total       
        blockAcct = AccountDB.getBalSheetAccounts(self, (400, 499))
        incomeTotal = 0.0
        for row in blockAcct:
            incomeTotal = incomeTotal + float(row[3])
            # get expense block total
        blockAcct = AccountDB.getBalSheetAccounts(self, (500, 599))
        expenseTotal = 0.0
        for row in blockAcct:
            expenseTotal = expenseTotal + float(row[3])
        retainedEarnings = incomeTotal - expenseTotal

        # get equity block       
        blockAcct = AccountDB.getBalSheetAccounts(self, (300,399))
        equityTotal = 0.0
        for row in blockAcct:
            equityTotal = equityTotal + float(row[3])
        # reset cline to top right
        cline = cline + 13
        maccount = str(blockAcct[0][0])
        maccountLength = len(maccount) + (4 - len(maccount))  # 4 x 7 =28
        maccount = maccount.ljust(maccountLength)
        self.reportWin.create_text(354, cline, anchor=tk.NW, text=maccount, fill="#2A0800")
        mDescription = blockAcct[0][1].upper()
        descLength = len(mDescription) + (30 - len(mDescription))
        mDescription = mDescription.ljust(descLength)
        self.reportWin.create_text(410, cline, anchor=tk.NW, text=mDescription, fill="#2A0800")
        TotalEquity = retainedEarnings+equityTotal
        mBalance = str(round(TotalEquity, 2))
        mbalanceLength = len(mBalance) + (8 - len(mBalance))  # 8 x 7 = 56
        mBalance = mBalance.rjust(mbalanceLength)
        self.reportWin.create_text(605, cline, anchor=tk.NW, text=mBalance, fill="#2A0800")

        cline = cline + 13
        '''maccount = str(399)        
        maccountLength = len(maccount)+(4-len(maccount))    # 4 x 7 =28
        maccount = maccount.ljust(maccountLength)
        self.reportWin.create_text(344,cline,anchor=tk.NW, text=maccount)'''

        cline = cline + 20
        self.reportWin.create_line(598, cline, 663, cline, fill="blue")
        cline = cline + 13
        msTotal = str(round(TotalEquity, 2))

        msTotalLength = len(msTotal) + (10 - len(msTotal))
        msTotal = msTotal.rjust(msTotalLength)
        self.reportWin.create_text(598, cline, anchor=tk.NW, text=msTotal, fill="#2A0800")

        cline = cline + 20
        self.reportWin.create_line(598, cline, 663, cline, fill="blue")

        cline = cline + 43
        self.reportWin.create_line(10, cline, 670, cline, fill="blue")
        cline = cline + 3
        self.reportWin.create_line(10, cline, 670, cline, fill="blue")
        cline = cline + 13

        self.reportWin.create_text(265, cline, anchor=tk.NW, text=mTotal, fill="#2A0800")
        mrTotal = str(TotalEquity + liabilityTotal)
        mrTotalLength = len(mrTotal) + (10 - len(mrTotal))
        miTotal = mrTotal.rjust(mrTotalLength)
        self.reportWin.create_text(598, cline, anchor=tk.NW, text=miTotal, fill="#2A0800")

    def do_reptTrialBalance(self):
        '''
        '''
        # Fetch revenue accounts
        # Fetch Expense accounts
        # Get Balance totals for each account        
        # Display the Revenue and Expense accounts in a table        
        self.reportWin.delete("all")
        self.reportWin.create_text(335, 12, text='TRIAL BALANCE',font=("Times 10 bold",16))
        self.reportWin.create_text(150, 38, anchor=tk.NW, text='DEBITS', fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(460, 38, anchor=tk.NW, text='CREDITS', fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(12, 55, anchor=tk.NW, text='Account'.upper(), fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(90, 55, anchor=tk.NW, text='Name'.upper(), fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(273, 55, anchor=tk.NW, text='Balance'.upper(), fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(344, 55, anchor=tk.NW, text='Account'.upper(), fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(420, 55, anchor=tk.NW, text='Name'.upper(), fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(605, 55, anchor=tk.NW, text='Balance'.upper(), fill='blue',font=("Times 10 bold",9))
        cline = 55
        # -------------------------------------------------------------
        cline = cline + 20
        self.reportWin.create_line(10, cline, 670, cline, fill="blue")
        cline = cline + 3
        self.reportWin.create_line(10, cline, 670, cline, fill="blue")
        # -------------------------------------------------------------
        # -------------------------------------------------------------
        # Get Debits
        # get assets block       
        blockAcct = AccountDB.getBalSheetAccounts(self, (100, 199))
        assetsTotal = 0.0
        for row in blockAcct:
            account = row[0]
            ldgrAccount = AccountDB.getLedgerAccount(self, account)
            acctTotal = 0.0
            for mtransact in ldgrAccount:
                acctTotal = acctTotal + mtransact[2]
            assetsTotal = assetsTotal + float(acctTotal)
            cline = cline + 13
            maccount = str(row[0])
            maccountLength = len(maccount) + (4 - len(maccount))  # 4 x 7 =28
            maccount = maccount.ljust(maccountLength)
            self.reportWin.create_text(22, cline, anchor=tk.NW, text=maccount, fill="#2A0800")
            mDescription = row[1]
            descLength = len(mDescription) + (30 - len(mDescription))
            mDescription = mDescription.ljust(descLength)
            self.reportWin.create_text(90, cline, anchor=tk.NW, text=mDescription, fill="#2A0800")
            mBalance = str(round(acctTotal, 2))
            mbalanceLength = len(mBalance) + (8 - len(mBalance))  # 8 x 7 = 56
            mBalance = mBalance.rjust(mbalanceLength)
            self.reportWin.create_text(273, cline, anchor=tk.NW, text=mBalance, fill="#2A0800")

        cline = cline + 20
        self.reportWin.create_line(265, cline, 325, cline, fill="blue")
        cline = cline + 13
        mTotal = str(round(assetsTotal, 2))
        mTotalLength = len(mTotal) + (10 - len(mTotal))  # 8 x 7 = 56
        mTotal = mTotal.rjust(mTotalLength)
        self.reportWin.create_text(265, cline, anchor=tk.NW, text=mTotal, fill="#2A0800")
        cline = cline + 13

        # -------------------------------------------------------------
        # get Expense block       
        blockAcct = AccountDB.getBalSheetAccounts(self, (500, 599))
        expenseTotal = 0.0
        # reset cline to top right
        for row in blockAcct:
            account = row[0]
            ldgrAccount = AccountDB.getLedgerAccount(self, account)
            acctTotal = 0.0
            for mtransact in ldgrAccount:
                acctTotal = acctTotal + mtransact[2]
            expenseTotal = expenseTotal + float(acctTotal)
            cline = cline + 13
            maccount = str(row[0])
            maccountLength = len(maccount) + (4 - len(maccount))  # 4 x 7 =28
            maccount = maccount.ljust(maccountLength)
            self.reportWin.create_text(22, cline, anchor=tk.NW, text=maccount, fill="#2A0800")
            mDescription = row[1]
            descLength = len(mDescription) + (30 - len(mDescription))
            mDescription = mDescription.ljust(descLength)
            self.reportWin.create_text(90, cline, anchor=tk.NW, text=mDescription, fill="#2A0800")
            mBalance = str(round(acctTotal, 2))
            mbalanceLength = len(mBalance) + (8 - len(mBalance))  # 8 x 7 = 56
            mBalance = mBalance.rjust(mbalanceLength)
            self.reportWin.create_text(273, cline, anchor=tk.NW, text=mBalance, fill="#2A0800")

        cline = cline + 20
        self.reportWin.create_line(265, cline, 325, cline, fill="blue")
        cline = cline + 13
        mlTotal = str(round(expenseTotal, 2))
        mlTotalLength = len(mlTotal) + (10 - len(mlTotal))  # 8 x 7 = 56
        mlTotal = mlTotal.rjust(mlTotalLength)
        self.reportWin.create_text(265, cline, anchor=tk.NW, text=mlTotal, fill="#2A0800")
        cline = cline + 13
        lcline = cline

        # -------------------------------------------------------------
        # -------------------------------------------------------------    
        # get Credits
        # get Liabilities and Equity block       
        blockAcct = AccountDB.getBalSheetAccounts(self, (200, 399))
        liabilitiesTotal = 0.0
        # reset cline to top right
        cline = 78
        for row in blockAcct:
            account = row[0]
            ldgrAccount = AccountDB.getLedgerAccount(self, account)
            acctTotal = 0.0
            for mtransact in ldgrAccount:
                acctTotal = acctTotal + mtransact[2]
            liabilitiesTotal = liabilitiesTotal + float(acctTotal)
            cline = cline + 13
            maccount = str(row[0])
            maccountLength = len(maccount) + (4 - len(maccount))  # 4 x 7 =28
            maccount = maccount.ljust(maccountLength)
            self.reportWin.create_text(358, cline, anchor=tk.NW, text=maccount, fill="#2A0800")
            mDescription = row[1]
            descLength = len(mDescription) + (30 - len(mDescription))
            mDescription = mDescription.ljust(descLength)
            self.reportWin.create_text(420, cline, anchor=tk.NW, text=mDescription, fill="#2A0800")
            mBalance = str(round(acctTotal, 2))
            mbalanceLength = len(mBalance) + (8 - len(mBalance))  # 8 x 7 = 56
            mBalance = mBalance.rjust(mbalanceLength)
            self.reportWin.create_text(612, cline, anchor=tk.NW, text=mBalance, fill="#2A0800")

        cline = cline + 20
        self.reportWin.create_line(598, cline, 663, cline, fill="blue")
        cline = cline + 13
        mrTotal = str(round(liabilitiesTotal, 2))
        mrTotalLength = len(mrTotal) + (10 - len(mrTotal))  # 8 x 7 = 56
        mrTotal = mrTotal.rjust(mrTotalLength)
        self.reportWin.create_text(598, cline, anchor=tk.NW, text=mrTotal, fill="#2A0800")

        # -------------------------------------------------------------
        # get revenue block  
        cline = cline + 13
        blockAcct = AccountDB.getBalSheetAccounts(self, (400, 499))
        revenueTotal = 0.0
        for row in blockAcct:
            account = row[0]
            ldgrAccount = AccountDB.getLedgerAccount(self, account)
            acctTotal = 0.0
            for mtransact in ldgrAccount:
                revenueTotal = revenueTotal + mtransact[2]
            assetsTotal = assetsTotal + float(acctTotal)
            cline = cline + 13
            maccount = str(row[0])
            maccountLength = len(maccount) + (4 - len(maccount))  # 4 x 7 =28
            maccount = maccount.ljust(maccountLength)
            self.reportWin.create_text(358, cline, anchor=tk.NW, text=maccount, fill="#2A0800")
            mDescription = row[1]
            descLength = len(mDescription) + (30 - len(mDescription))
            mDescription = mDescription.ljust(descLength)
            self.reportWin.create_text(420, cline, anchor=tk.NW, text=mDescription, fill="#2A0800")
            mBalance = str(round(row[3], 2))
            mbalanceLength = len(mBalance) + (8 - len(mBalance))  # 8 x 7 = 56
            mBalance = mBalance.rjust(mbalanceLength)
            self.reportWin.create_text(612, cline, anchor=tk.NW, text=mBalance, fill="#2A0800")

        cline = cline + 20
        self.reportWin.create_line(598, cline, 663, cline, fill="blue")

        cline = cline + 13
        mrTotal = str(round(revenueTotal, 2))
        mrTotalLength = len(mrTotal) + (10 - len(mrTotal))  # 8 x 7 = 56
        mrTotal = mrTotal.rjust(mrTotalLength)
        self.reportWin.create_text(598, cline, anchor=tk.NW, text=mrTotal, fill="#2A0800")
        cline = cline + 13
        rcline = cline
        # -------------------------------------------------------------
        # check which column is longer and use it
        if lcline > rcline:
            cline = lcline
        else:
            cline = rcline
        cline = cline + 26
        self.reportWin.create_line(10, cline, 670, cline, fill="blue")
        cline = cline + 3
        self.reportWin.create_line(10, cline, 670, cline, fill="blue")
        cline = cline + 26
        debitTotal = assetsTotal + expenseTotal
        self.reportWin.create_text(90, cline, anchor=tk.NW, text="Total Debits".upper(), fill="#2A0800")
        self.reportWin.create_text(273, cline, anchor=tk.NW, text=debitTotal, fill="#2A0800")
        creditTotal = liabilitiesTotal + revenueTotal
        self.reportWin.create_text(420, cline, anchor=tk.NW, text="Total Credits".upper(), fill="#2A0800")
        self.reportWin.create_text(598, cline, anchor=tk.NW, text=creditTotal, fill="#2A0800")

    def do_reptPostClosing(self):
        '''
        '''
        # Fetch revenue accounts
        # Fetch Expense accounts
        # Get Balance totals for each account        
        # Display the Revenue and Expense accounts in a table

        chartAcct = AccountDB.getclosingentries(self, (400, 501))
        drawing = chartAcct[0][0] - abs(chartAcct[2][0])

        self.reportWin.delete("all")
        self.reportWin.create_text(335, 12, text='POST CLOSING TRIAL BALANCE',font=("Times 10 bold",16))
        self.reportWin.create_text(150, 38, anchor=tk.NW, text='DEBITS', fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(460, 38, anchor=tk.NW, text='CREDITS', fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(12, 55, anchor=tk.NW, text='Account', fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(63, 55, anchor=tk.NW, text='Name', fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(273, 55, anchor=tk.NW, text='Balance', fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(344, 55, anchor=tk.NW, text='Account', fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(395, 55, anchor=tk.NW, text='Name', fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(605, 55, anchor=tk.NW, text='Balance', fill='blue',font=("Times 10 bold",9))
        cline = 55
        # -------------------------------------------------------------
        cline = cline + 20
        self.reportWin.create_line(10, cline, 670, cline, fill="blue")
        cline = cline + 3
        self.reportWin.create_line(10, cline, 670, cline, fill="blue")
        # -------------------------------------------------------------
        # -------------------------------------------------------------
        # Get Debits
        # get assets block       
        blockAcct = AccountDB.getBalSheetAccounts(self, (100, 199))
        assetsTotal = 0.0
        for row in blockAcct:
            account = row[0]
            ldgrAccount = AccountDB.getLedgerAccount(self, account)
            acctTotal = 0.0
            for mtransact in ldgrAccount:
                acctTotal = acctTotal + mtransact[2]
            assetsTotal = assetsTotal + float(acctTotal)
            cline = cline + 13
            maccount = str(row[0])
            maccountLength = len(maccount) + (4 - len(maccount))  # 4 x 7 =28
            maccount = maccount.ljust(maccountLength)
            self.reportWin.create_text(12, cline, anchor=tk.NW, text=maccount, fill="#2A0800")
            mDescription = row[1]
            descLength = len(mDescription) + (30 - len(mDescription))
            mDescription = mDescription.ljust(descLength)
            self.reportWin.create_text(63, cline, anchor=tk.NW, text=mDescription, fill="#2A0800")
            mBalance = str(round(acctTotal, 2))
            mbalanceLength = len(mBalance) + (8 - len(mBalance))  # 8 x 7 = 56
            mBalance = mBalance.rjust(mbalanceLength)
            self.reportWin.create_text(273, cline, anchor=tk.NW, text=mBalance, fill="#2A0800")

        cline = cline + 20
        self.reportWin.create_line(265, cline, 325, cline, fill="blue")
        cline = cline + 13
        mTotal = str(round(assetsTotal, 2))
        mTotalLength = len(mTotal) + (10 - len(mTotal))  # 8 x 7 = 56
        mTotal = mTotal.rjust(mTotalLength)
        self.reportWin.create_text(265, cline, anchor=tk.NW, text=mTotal, fill="#2A0800")
        cline = cline + 13

        cline = cline + 13
        lcline = cline

        # -------------------------------------------------------------
        # -------------------------------------------------------------    
        # get Credits
        # get Liabilities and Equity block
        blockAcct = AccountDB.getBalSheetAccounts(self, (200, 299))
        liabilitiesTotal = 0.0
        # reset cline to top right
        cline = 78
        for row in blockAcct:
            account = row[0]
            ldgrAccount = AccountDB.getLedgerAccount(self, account)
            acctTotal = 0.0
            for mtransact in ldgrAccount:
                acctTotal = acctTotal + mtransact[2]
            chartAcct = AccountDB.getclosingentries(self, (400, 501))
            income = chartAcct[0][0] - chartAcct[2][0] - abs(chartAcct[1][0])
            liabilitiesTotal = liabilitiesTotal + float(acctTotal)
            cline = cline + 13
            maccount = str(row[0])
            maccountLength = len(maccount) + (4 - len(maccount))  # 4 x 7 =28
            maccount = maccount.ljust(maccountLength)
            self.reportWin.create_text(344, cline, anchor=tk.NW, text=maccount, fill="#2A0800")
            mDescription = row[1]
            descLength = len(mDescription) + (30 - len(mDescription))
            mDescription = mDescription.ljust(descLength)
            self.reportWin.create_text(395, cline, anchor=tk.NW, text=mDescription, fill="#2A0800")
            mBalance = str(round(acctTotal, 2))
            mbalanceLength = len(mBalance) + (8 - len(mBalance))  # 8 x 7 = 56
            mBalance = mBalance.rjust(mbalanceLength)
            self.reportWin.create_text(612, cline, anchor=tk.NW, text=mBalance, fill="#2A0800")
        cline = cline + 20
        blockAcct = AccountDB.getBalSheetAccounts(self, (300, 300))
        equityTotal = 0.0
        # reset cline to top right
        maccount = str(blockAcct[0][0])
        maccountLength = len(maccount) + (4 - len(maccount))  # 4 x 7 =28
        maccount = maccount.ljust(maccountLength)
        self.reportWin.create_text(344, cline, anchor=tk.NW, text=maccount, fill="#2A0800")
        mDescription = blockAcct[0][1]
        descLength = len(mDescription) + (30 - len(mDescription))
        mDescription = mDescription.ljust(descLength)
        self.reportWin.create_text(395, cline, anchor=tk.NW, text=mDescription, fill="#2A0800")
        blockAcct = AccountDB.getBalSheetAccounts(self, (400, 499))
        incomeTotal = 0.0
        for row in blockAcct:
            incomeTotal = incomeTotal + float(row[3])
            # get expense block total
        blockAcct = AccountDB.getBalSheetAccounts(self, (500, 599))
        expenseTotal = 0.0
        for row in blockAcct:
            expenseTotal = expenseTotal + float(row[3])
        retainedEarnings = incomeTotal - expenseTotal

        # get equity block
        blockAcct = AccountDB.getBalSheetAccounts(self, (300, 399))
        equityTotal = 0.0
        for row in blockAcct:
            equityTotal = equityTotal + float(row[3])
        TotalEquity=retainedEarnings+equityTotal
        mBalance = str(round(TotalEquity, 2))
        mbalanceLength = len(mBalance) + (8 - len(mBalance))  # 8 x 7 = 56
        mBalance = mBalance.rjust(mbalanceLength)
        self.reportWin.create_text(612, cline, anchor=tk.NW, text=mBalance, fill="#2A0800")

        cline = cline + 13
        '''maccount = str(399)        
        maccountLength = len(maccount)+(4-len(maccount))    # 4 x 7 =28
        maccount = maccount.ljust(maccountLength)
        self.reportWin.create_text(344,cline,anchor=tk.NW, text=maccount)'''

        cline = cline + 20
        self.reportWin.create_line(598, cline, 663, cline, fill="blue")
        cline = cline + 13
        liabilitiesTotal = liabilitiesTotal + TotalEquity
        mrTotal = str(round(liabilitiesTotal, 2))
        mrTotalLength = len(mrTotal) + (10 - len(mrTotal))  # 8 x 7 = 56
        mrTotal = mrTotal.rjust(mrTotalLength)
        self.reportWin.create_text(598, cline, anchor=tk.NW, text=mrTotal, fill="#2A0800")
        cline = cline + 13
        rcline = cline

        # -------------------------------------------------------------
        # check which column is longer and use it
        if lcline > rcline:
            cline = lcline
        else:
            cline = rcline
        cline = cline + 26
        self.reportWin.create_line(10, cline, 670, cline, fill="blue")
        cline = cline + 3
        self.reportWin.create_line(10, cline, 670, cline, fill="blue")
        cline = cline + 26
        debitTotal = assetsTotal  # + expenseTotal
        self.reportWin.create_text(63, cline, anchor=tk.NW, text="Total Debits", fill="#2A0800")
        self.reportWin.create_text(265, cline, anchor=tk.NW, text=debitTotal, fill="#2A0800")
        creditTotal = liabilitiesTotal
        self.reportWin.create_text(395, cline, anchor=tk.NW, text="Total Credits", fill="#2A0800")
        self.reportWin.create_text(598, cline, anchor=tk.NW, text=creditTotal, fill="#2A0800")

    def do_reptequitystatement(self):
        self.reportWin.delete("all")
        self.reportWin.create_text(335, 12, text='OWNER\'S EQUITY STATEMENT',font=("Times 10 bold",16))
        self.reportWin.create_text(20, 55, anchor=tk.NW, text='Account'.upper(), fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(103, 55, anchor=tk.NW, text='Name'.upper(), fill='blue',font=("Times 10 bold",9))
        self.reportWin.create_text(283, 55, anchor=tk.NW, text='Balance'.upper(), fill='blue',font=("Times 10 bold",9))
        cline = 55
        cline = cline + 20
        self.reportWin.create_line(10, cline, 670, cline, fill="blue")
        cline = cline + 6
        self.reportWin.create_line(10, cline, 670, cline, fill="blue")
        # get assets block
        blockAcct = AccountDB.getBalSheetAccounts(self, (300, 399))
        TotalEquity = 0.0
        for row in blockAcct:
            cline = cline + 13
            maccount = str(row[0])
            maccountLength = len(maccount) + (4 - len(maccount))  # 4 x 7 =28
            maccount = maccount.ljust(maccountLength)
            self.reportWin.create_text(30, cline, anchor=tk.NW, text=maccount, fill="#2A0800")
            mDescription = row[1]
            descLength = len(mDescription) + (30 - len(mDescription))
            mDescription = mDescription.ljust(descLength)
            self.reportWin.create_text(103, cline, anchor=tk.NW, text=mDescription, fill="#2A0800")
            mBalance = str(round(row[3], 2))
            TotalEquity = TotalEquity + row[3]
            mbalanceLength = len(mBalance) + (8 - len(mBalance))  # 8 x 7 = 56
            mBalance = mBalance.rjust(mbalanceLength)
            self.reportWin.create_text(283, cline, anchor=tk.NW, text=mBalance)
        blockAcct = AccountDB.getBalSheetAccounts(self, (400, 499))
        revenueTotal = 0.0
        for row in blockAcct:
            revenueTotal = revenueTotal + float(row[3])
        blockAcct = AccountDB.getBalSheetAccounts(self, (500, 599))
        ExpenseTotal = 0.0
        for row in blockAcct:
            ExpenseTotal = ExpenseTotal + float(row[3])
        chartAcct = AccountDB.getclosingentries(self, (400, 501))
        income = revenueTotal - ExpenseTotal
        cline = cline + 13
        mDescription = "NET INCOME"
        descLength = len(mDescription) + (30 - len(mDescription))
        mDescription = mDescription.ljust(descLength)
        self.reportWin.create_text(103, cline, anchor=tk.NW, text=mDescription, fill="#2A0800")
        mBalance = str(round(income, 2))
        TotalEquity = TotalEquity + income
        mbalanceLength = len(mBalance) + (8 - len(mBalance))  # 8 x 7 = 56
        mBalance = mBalance.rjust(mbalanceLength)
        self.reportWin.create_text(283, cline, anchor=tk.NW, text=mBalance, fill="#2A0800")
        cline = cline + 30
        self.reportWin.create_line(10, cline, 670, cline, fill="blue")
        cline = cline + 20
        mDescription = "Owner\'s Capital"
        descLength = len(mDescription) + (30 - len(mDescription))
        mDescription = mDescription.ljust(descLength)
        self.reportWin.create_text(103, cline, anchor=tk.NW, text=mDescription.upper(), fill="#2A0800")
        self.reportWin.create_text(283, cline, anchor=tk.NW, text=TotalEquity, fill="#2A0800")
