#!/usr/bin/python

import os,sys,time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
#import psycopg2

class report(QWidget):
    def __init__(self,conn=None):
        super(report,self).__init__()

        try:
            self.conn = conn
            self.cur = self.conn.cursor()
        except Exception,e:
            QMessageBox.information(self,"Database Error","An error creating database connection: "+str(e))

        self.head_lbl = QLabel("REPORT",self)
        self.head_lbl.setGeometry(10,10,720,30)
        self.head_lbl.setStyleSheet("color: black; background-color: gray;border-radius:14px")
        self.head_lbl.setFont(QFont("SansSerif",18,QFont.Bold))
        self.head_lbl.setAlignment(Qt.AlignCenter)
                
        self.date_lbl = QLabel("Date :",self)
        self.date_lbl.setGeometry(260,50,100,30)
        self.date_lbl.setStyleSheet("color: black")
        self.date_lbl.setAlignment(Qt.AlignCenter)
        self.date_lbl.setFont(QFont("Times",18))

        ## Display labels        
        self.date_input = QDateEdit(self)
        self.date_input.setGeometry(360,50,120,30)
        self.date_input.setDateTime(QDateTime.currentDateTime())
        self.date_input.setDisplayFormat('yyyy-MM-dd')
        self.date_input.setCalendarPopup(True)
        #self.date_input.setStyleSheet("color: black; background-color: red")
        
        self.table_headers = ["Name","Opening Stock","Added","Sold","Closing Stock","Date"]
        self.information_table = QTableWidget(self)
        self.information_table.setGeometry(50,100,650,430)
        self.information_table.setRowCount(0)
        self.information_table.setAlternatingRowColors(True)
        self.information_table.setStyleSheet("alternate-background-color: gray; background-color: white")
        self.information_table.setColumnCount(len(self.table_headers))
        for i in range(len(self.table_headers)):
            self.information_table.setHorizontalHeaderItem(i,QTableWidgetItem(self.table_headers[i]))

        ### Buttons
        self.search_btn = QPushButton("SEARCH",self)
        self.search_btn.setGeometry(550,50,100,30)
        self.search_btn.clicked.connect(self.showresults)

        self.clear_btn = QPushButton("CLEAR",self)
        self.clear_btn.setGeometry(550,550,100,30)
        self.clear_btn.clicked.connect(self.cleartable)

        self.setGeometry(100,100,740,600)
        self.setWindowTitle("REPORTS")


    def cleartable(self):
        self.information_table.setRowCount(0)


    def showresults(self):
        self.information_table.setRowCount(0)
        self.search_date = str(self.date_input.date().toPyDate())
        self.search_date_lst = self.search_date.split('-')

        query = "select opening_stock, quantity_add, quantity_sold, closing_stock, p_id from sales where extract(year from sale_date) = %s and extract(month from sale_date) = %s and extract(day from sale_date) = %s"
        self.data = [self.search_date_lst[0], self.search_date_lst[1], self.search_date_lst[2]]

        try:
            self.cur.execute(query,self.data)
            results = self.cur.fetchall()
        except Exception,e:
            QMessageBox.information(self,"Database Error","Error: "+str(e))
            return

        disp_lst = []
        if results != []:
            for val in results:
                lst = []
                try:
                    self.cur.execute("select pname from products where p_id = %s",[val[4]])
                    re = self.cur.fetchone()
                    lst.append(re[0])
                    lst.insert(1,val[0])
                    lst.insert(2,val[1])
                    lst.insert(3,val[2])
                    lst.insert(4,val[3])
                    lst.insert(5,self.search_date)
                except Exception,e:
                    QMessageBox.information(self,"Database Error","Error: "+str(e))
                    return
                disp_lst.append(lst)

            self.information_table.setRowCount(len(disp_lst))
            for row in range(len(disp_lst)):
                for col in range(6):
                    self.information_table.setItem(row,col,QTableWidgetItem(str(disp_lst[row][col])))

        else:
            pass

# For debugging 
'''
app = QApplication(sys.argv)
gen_report = report()
gen_report.show()
sys.exit(app.exec_())
'''
