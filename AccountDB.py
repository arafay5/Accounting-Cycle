
import sqlite3
import tkinter as tk
from tkinter import messagebox as mBox
import splash

#print(splashScreen().filename)

class AccountDB(object):


    def __init__(self):
        

        '''
        Constructor
        '''
    
    # #################################
    # Database Functions
    # ################################# 
    
      
    def createAccounts(self):
        '''
        Create New Database and Tables if not existing
        @summary: Creates a fully new accounting set-up. The System accounts are 
            fixed by accounting convention and may not be changed of reused for 
            other purposes.
        @warning: Will not allow overwriting so any old data tables should be moved from the directory.
        '''
        # Check that a fully new set-up is intended
        proceedAnswer = mBox.askyesno("Initial Set-up","This is The New System Set-up.\nThere should be no old data tables in directory,\n Proceed?")
        if (not proceedAnswer):
            print('aborted new setup')
            return
        # Some local, set-up related message boxes
        def setupError(self):
            mBox.showerror(title='Set-up Error', message='Chart of Accounts already populated, you may not overwrite')
        def setupInfo(self):
            mBox.showinfo('Set-up Information' , 'Adding System Accounts to Chart of Accounts.') 
        
        #If Not Existing, Create batabase, data tables and system ledger accounts  
        db = sqlite3.connect(self.filename)
        db.execute('''CREATE TABLE IF NOT EXISTS journal (
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
        
        db.execute('''CREATE TABLE IF NOT EXISTS ledger 
            (Account INTEGER     NOT NULL, 
            Transact INTEGER     KEY NOT NULL, 
            Amount REAL    NOT NULL, 
            Balance REAL    NOT NULL)''')
        
        db.execute('''CREATE TABLE IF NOT EXISTS chart 
            (Account INTEGER PRIMARY KEY    NOT NULL, 
            Name STRING(60)    NOT NULL, 
            Type STRING(10)    NOT NULL,
            Balance REAL       NOT NULL)''')
        
        # Check if Chart of Accounts already set-up, may not be overwritten
        count = db.execute("SELECT count(Account) FROM chart")
        for row in count:
            tableFull=bool(row[0])
        if (not tableFull):
            setupInfo(self)
            db.execute('''INSERT INTO chart VALUES (100, "ASSETS", "DEBIT", 0),
                (120, "RECEIVABLES","DEBIT",0),
                (200, "LIABILITIES","CREDIT",0), 
                (220, "PAYABLES","CREDIT",0), 
                (300, "EQUITY","CREDIT",0),
                (399, "RETAINED EARNINGS", "CREDIT",0),  
                (400, "REVENUE","CREDIT",0),
                (500, "EXPENSES","DEBIT",0)        
                ''')      
            db.commit()  
        else:
            setupError(self)
        
        db.close()
        
    def getChartAccounts(self):
        '''
        Return all Chart of Accounts
        '''
        chart = list() 
        db = sqlite3.connect(splash.splashScreen.filename[0])
        cursor = db.cursor()
        cursor.execute("SELECT * FROM chart ORDER BY Account")
        for row in cursor:            
            chart.append(row)        
        db.close()
        return chart
    def gettrasactionid(self):
        trans_id = list()
        db = sqlite3.connect(splash.splashScreen.filename[0])
        cursor = db.cursor()
        cursor.execute("SELECT Transact FROM journal")
        for row in cursor:
            trans_id.append(row[0])
        db.close()
        return trans_id
    def getchartaccts(self):
        chart = list()
        db = sqlite3.connect(splash.splashScreen.filename[0])
        cursor = db.cursor()
        cursor.execute("SELECT Account,Name FROM chart ORDER BY Account")
        for row in cursor:
            chart.append(row)
        db.close()
        return chart

    def get_transact_balance(self,account,transact):
        amount=[]
        db = sqlite3.connect(splash.splashScreen.filename[0])
        cursor = db.cursor()
        cursor.execute("SELECT Amount FROM ledger WHERE Account={} and Transact={}".format(account,transact))
        for row in cursor:
            amount.append(row)
        db.close()
        return amount

    
    def getBalSheetAccounts(self, accRange):
        '''
        Return a Block of Accounts
        '''
        accBlock = list() 
        db = sqlite3.connect(splash.splashScreen.filename[0])
        cursor = db.cursor()
        cursor.execute("SELECT * FROM chart WHERE Account >= {} AND Account <= {} ORDER BY Account".format(accRange[0], accRange[1]))
        for row in cursor:            
            accBlock.append(row)        
        db.close()
        return accBlock
    
    def existChartAccount(self, account):
        '''
        '''
        pass
    
    def getLedgerAccount(self,account):
        '''
        Return all entries for an account
        '''
        ledger = list() 
        db = sqlite3.connect(splash.splashScreen.filename[0])
        cursor = db.cursor()
        if int(account) == 0:
            cursor.execute("SELECT * FROM ledger ORDER BY Account")
        else:
            cursor.execute("SELECT * FROM ledger WHERE Account = {} ORDER BY Transact".format(account,))
        for row in cursor:            
            ledger.append(row)        
        db.close()
        return ledger
    
    def getJournalEntries(self, jDates):
        '''
        Return all of a journal date range
        '''
        journal = list() 
        db = sqlite3.connect(splash.splashScreen.filename[0])
        cursor = db.cursor()
        if jDates == (0,0):
            cursor.execute("SELECT * FROM journal ORDER BY Date DESC")
        else:
            cursor.execute("SELECT * FROM journal WHERE Date = {} ORDER BY Transact".format(jDates[0]))
        for row in cursor:            
            journal.append(row)        
        db.close()
        return journal
    
    def getJournalTransact(self, jTransact):
        '''
        Return a journal transaction
        '''
        transact = list() 
        db = sqlite3.connect(splash.splashScreen.filename[0])
        cursor = db.cursor()
        if int(jTransact) == 0:
            cursor.execute("SELECT * FROM journal ORDER BY Date DESC")
        else:
            cursor.execute("SELECT * FROM journal WHERE Transact = {} ORDER BY Date".format(jTransact))
        for row in cursor:            
            transact.append(row)        
        db.close()
        return transact

    
    def insertJournalEntry(self, jrow):
        '''
        Insert an entry into Journal
        '''
        db = sqlite3.connect(splash.splashScreen.filename[0])
        db.execute("INSERT INTO journal VALUES {}".format(jrow))
        db.commit()
        db.close()
        
    def insertLedgerEntry(self, lrow):
        '''
        Post journal debit or credit to Ledger
        '''
        db = sqlite3.connect(splash.splashScreen.filename[0])
        db.execute("INSERT INTO ledger VALUES {}".format(lrow))
        db.commit()
        db.close()
    
    def insertChartAccount(self, row):
        '''
        Update an Balance into Chart Account
        '''
        db = sqlite3.connect(splash.splashScreen.filename[0])
        db.execute("INSERT INTO chart VALUES {}".format(row))
        db.commit()
        db.close()

    def updateChartBalance(self, account, balance):  # Account balance in chart of accounts
        db = sqlite3.connect(splash.splashScreen.filename[0])
        cursor = db.cursor()
        cursor.execute("UPDATE Chart SET Balance = {} WHERE Account = {}".format(balance, account))
        db.commit()
        db.close()
        
    def getAccountNumbers(self, accrange, acctype):
        '''
        Get a list of account numbers from chart
        '''
        acctNos = list() 
        db = sqlite3.connect(splash.splashScreen.filename[0])
        if accrange == (0,0):
            if acctype == 'DEBIT':
                cursor = db.cursor()
                cursor.execute("SELECT Account FROM chart WHERE ActyType ='DEBIT' ORDER BY Account".format(accrange))
            else:                                    # AccType = CREDIT
                cursor = db.cursor()
                cursor.execute("SELECT * FROM chart WHERE ActyType = 'CREDIT' ORDER BY Account".format(accrange))
        else:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM chart WHERE Account > {} and Account < {} ORDER BY Account".format(accrange))                             
        for row in cursor:            
            acctNos.append(row)        
        db.close()
        return acctNos
        
    def getAccountType(self,laccount):
        '''
        Get LAST ledger balance for specified account
        '''
        atype = list() 
        db = sqlite3.connect(splash.splashScreen.filename[0])
        cursor = db.cursor()
        cursor.execute("SELECT ActyType FROM Chart WHERE Account = {}".format(laccount,))
        for row in cursor:            
            atype.append(row) 
        rtype = atype[0][0]     
        db.close()
        return rtype

    def getclosingentries(self,accRange):
        closing=[]
        db = sqlite3.connect(splash.splashScreen.filename[0])
        cursor = db.cursor()
        cursor.execute("SELECT Balance FROM chart WHERE Account >= {} AND Account <= {} ORDER BY Account".format(accRange[0], accRange[1]))
        for i in cursor:
            closing.append(i)
        return closing


    def getAccountBalance(self,laccount):
        '''
        Get LAST ledger balance for specified account
        '''
        balance = list() 
        db = sqlite3.connect("Accounts.db")
        cursor = db.cursor()
        cursor.execute("SELECT Balance FROM Chart WHERE Account = {}".format(laccount,))
        for row in cursor:            
            balance.append(row)
        oldBalance = balance[0][0]     
        db.close()
        return oldBalance

    def getsgnAdjust(self, laccount, txType):
        actyType = list()
        db = sqlite3.connect(splash.splashScreen.filename[0])
        cursor = db.cursor()
        cursor.execute("SELECT Type FROM Chart WHERE Account = {}".format(laccount,))
        for row in cursor:            
            actyType.append(row)
        aType = actyType[0][0]
        if (txType=='DEBIT' and aType=='DEBIT') or (txType=='CREDIT' and aType=='CREDIT' ):            
            db.close()
            return 1
        else:
            db.close()            
            return -1

    def highestaccount(self,small, greater):
        db = sqlite3.connect(splash.splashScreen.filename[0])
        cursor = db.cursor()
        cursor.execute("SELECT Account FROM chart WHERE Account >= {} AND Account <= {} ORDER BY Account".format(small,greater))
        higher=0
        for i in cursor:
            if int(i[0]) > higher:
                higher = int(i[0])

        return higher
        # return balance
        
    def packDatabase(self):
        db = sqlite3.connect(splash.splashScreen.filename[0])
        mBox.showinfo('Maintenance' , 'PACKING Database for Clean-up, Defragmentation and Improved Performance.')
        db.execute('VACUUM')        
        db.close()

a=AccountDB()
a.getAccountBalance(101)
