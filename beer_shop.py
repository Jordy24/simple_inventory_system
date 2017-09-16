#!/usr/bin/python

import os,sys,time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import psycopg2

from report import *
from data_report import *
from administration import *


class mainwindow(QMainWindow):
    def __init__(self):
        super(mainwindow,self).__init__()

        try:
            self.conn = psycopg2.connect("dbname=green_view user=postgres host=localhost password=password")
            #self.cur = self.conn.cursor()
            self.statusBar().showMessage("Database Online")
        except Exception,e:
            self.statusBar().showMessage("Failed to connect to database...Please check your database connection!!" + str(e))
            return


        self.report = report(self.conn)
        self.mainpage = combined(self.conn)
        self.admin = administration(self.conn)

        self.menu_bar = self.menuBar()

        self.file = self.menu_bar.addMenu("File")
        self.product = self.menu_bar.addMenu("Products")

        exit = QAction("Exit",self)
        exit.setShortcut("Ctrl+q")
        self.file.addAction(exit)

        self.file.triggered[QAction].connect(self.quitapp)

        p_details = QAction("Product Details",self)
        p_details.setShortcut("Ctrl+p")
        self.product.addAction(p_details)

        self.product.triggered[QAction].connect(self.processtriger)

        self.tab_vals = QTabWidget(self)
        self.tab_vals.addTab(self.mainpage,"DAILY RECODS")
        self.tab_vals.addTab(self.report,"REPORTS")

        self.admin.done_btn.clicked.connect(self.getadded)

        self.setCentralWidget(self.tab_vals)
        #self.statusBar().showMessage('ready')
        self.setWindowTitle("BEER  SHOP")
        self.setGeometry(100,0,1170,670)

    def getadded(self):
        if self.admin.added_products() != []:
            self.mainpage.product_name_combo.addItems(self.admin.added_products())

    def quitapp(self,value):
        if value.text() == "Exit":
            self.close()

    def processtriger(self,value):
        self.admin.show()
        

app = QApplication(sys.argv)
mw = mainwindow()
mw.show()
sys.exit(app.exec_())

