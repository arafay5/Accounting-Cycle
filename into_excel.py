import sqlite3
from xlsxwriter.workbook import Workbook
from splash import splashScreen


class dbtoexcel:

    def all_worksheets(self):
        workbook = Workbook('accounting.xlsx')
        worksheet = workbook.add_worksheet()    # journal
        worksheet1 = workbook.add_worksheet()      # adjusted journal
        worksheet2 = workbook.add_worksheet()

        # journal
        conn=sqlite3.connect(splashScreen.filename[0])
        c=conn.cursor()
        c.execute("select * from chart")
        mysel=c.execute("select * from chart ")
        for i, row in enumerate(mysel):
            for j, value in enumerate(row):
                worksheet.write(i, j, value)

        # adjusted journal
        c.execute("select * from journal")
        mysel1 = c.execute("select * from journal")
        for i, row in enumerate(mysel1):
            for j, value in enumerate(row):
                worksheet1.write(i, j, value)

        # unadjusted trial balance
        c.execute("select * from ledger")
        mysel2 = c.execute("select * from ledger")
        for i, row in enumerate(mysel2):
            for j, value in enumerate(row):
                worksheet2.write(i, j, value)

        workbook.close()

    def worksheet0(self):
        workbook = Workbook('accounting.xlsx')
        worksheet = workbook.add_worksheet()  # journal
        conn = sqlite3.connect(splashScreen.filename[0])
        c = conn.cursor()
        c.execute("select * from journal")
        mysel = c.execute("select * from journal ")
        for i, row in enumerate(mysel):
            for j, value in enumerate(row):
                worksheet.write(i, j, value)


    def worksheet1(self):
        workbook = Workbook('accounting.xlsx')
        worksheet = workbook.add_worksheet()  # journal

        conn = sqlite3.connect(splashScreen.filename[0])
        c = conn.cursor()
        c.execute("select * from chart")
        mysel = c.execute("select * from chart ")
        for i, row in enumerate(mysel):
            for j, value in enumerate(row):
                worksheet.write(i, j, value)

    def worksheet2(self):
        workbook = Workbook('accounting.xlsx')
        worksheet = workbook.add_worksheet()  # journal


        # journal
        conn = sqlite3.connect(splashScreen.filename[0])
        c = conn.cursor()
        c.execute("select * from ledger")
        mysel = c.execute("select * from ledger")
        for i, row in enumerate(mysel):
            for j, value in enumerate(row):
                worksheet.write(i, j, value)

