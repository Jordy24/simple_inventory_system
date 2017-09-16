#!/usr/bin/python

import os,sys,time
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class combined(QWidget):
    def __init__(self,conn=None):
        super(combined,self).__init__()
        try:
            self.conn = conn
            self.cur = self.conn.cursor()
        except Exception, e:
            QMessageBox.information(self,"Database Error","Failed to connect database "+str(e))

        ##
        self.db_data = self.getproducts()
        ###

        #QMessageBox.information(self,"Hello","hey")

        self.head_lbl = QLabel("BEER   STORE",self)
        self.head_lbl.setGeometry(10,10,1130,30)
        self.head_lbl.setStyleSheet("color: black; background-color: gray; border-radius: 14px")
        self.head_lbl.setAlignment(Qt.AlignCenter)
        self.head_lbl.setFont(QFont("SansSerif",18,QFont.Bold))

        self.product_name_lbl = QLabel("Product Name:",self)
        self.product_name_lbl.setGeometry(10,50,100,30)
        self.product_name_lbl.setStyleSheet("color: black; background-color: silver")

        self.opening_stock_lbl = QLabel("Open Stock:",self)
        self.opening_stock_lbl.setGeometry(10,90,100,30)
        self.opening_stock_lbl.setStyleSheet("color: black; background-color: silver")

        self.added_stock_lbl = QLabel("Added: ",self)
        self.added_stock_lbl.setGeometry(10,130,100,30)
        self.added_stock_lbl.setStyleSheet("color: black; background-color: silver")

        self.sold_stock_lbl = QLabel("Sold: ",self)
        self.sold_stock_lbl.setGeometry(10,170,100,30)
        self.sold_stock_lbl.setStyleSheet("color: black; background-color: silver")

        '''
        self.closing_stock_lbl = QLabel("Closing Stock:",self)
        self.closing_stock_lbl.setGeometry(10,210,100,30)
        self.closing_stock_lbl.setStyleSheet("color: black; background-color: silver")
        '''

        self.total_stock_lbl = QLabel("Available: ",self)
        self.total_stock_lbl.setGeometry(10,210,100,30)
        self.total_stock_lbl.setStyleSheet("color: black; background-color: silver")

        self.date_lbl = QLabel("Date: ",self)
        self.date_lbl.setGeometry(10,250,100,30)
        self.date_lbl.setStyleSheet("color: black; background-color: silver")

        ## Input values
        self.product_name_combo = QComboBox(self)
        self.product_name_combo.setGeometry(110,50,150,30)
        for val in self.db_data:
            self.product_name_combo.addItem(val[1])
        self.product_name_combo.currentIndexChanged.connect(self.productselected)

        #self.opening_stock_input = QLineEdit(self)
        #self.opening_stock_input.setGeometry(110,90,150,30)  
        #self.opening_stock_input.textChanged.connect(self.check)

        self.opening_lbl = QLabel(self)
        #self.opening_lbl.setText("300")
        self.opening_lbl.setGeometry(110,90,150,30)  
        self.opening_lbl.setStyleSheet("color: brown")
        self.opening_lbl.setFont(QFont("Times",18))
        self.opening_lbl.setAlignment(Qt.AlignCenter)

        self.added_stock_input = QLineEdit(self)
        self.added_stock_input.setGeometry(110,130,150,30) 
        self.added_stock_input.textChanged.connect(self.check)

        self.sold_stock_input = QLineEdit(self)
        self.sold_stock_input.setGeometry(110,170,150,30) 
        self.sold_stock_input.textChanged.connect(self.closevalue)

        #self.closing_stock_input = QLineEdit(self)
        #self.closing_stock_input.setGeometry(110,210,150,30) 

        '''
        self.closing_lbl = QLabel(self)
        self.closing_lbl.setText("390")
        self.closing_lbl.setGeometry(110,210,150,30) 
        self.closing_lbl.setFont(QFont("Times",20))
        self.closing_lbl.setStyleSheet("color: blue")
        self.closing_lbl.setAlignment(Qt.AlignCenter)
        '''

        self.availabel_lbl = QLabel(self)
        #self.availabel_lbl.setText("450")
        self.availabel_lbl.setGeometry(110,210,150,30) 
        self.availabel_lbl.setStyleSheet("color: green")
        self.availabel_lbl.setFont(QFont("Times",18))
        self.availabel_lbl.setAlignment(Qt.AlignCenter)

        self.date_input = QDateEdit(self)
        self.date_input.setGeometry(110,250,150,30)
        self.date_input.setDateTime(QDateTime.currentDateTime())
        self.date_input.setDisplayFormat('yyyy-M-dd')
        self.date_input.setCalendarPopup(True)

        self.added_products_list = QListWidget(self)
        self.added_products_list.setGeometry(20,350,220,220)

        self.data_dict = {}
        self.rmlst = []

        ## Buttons
        self.add_item = QPushButton("Add Item",self)
        self.add_item.setGeometry(260,380,100,30)
        self.add_item.clicked.connect(self.addtolist)

        self.remove_item = QPushButton("Remove",self)
        self.remove_item.setGeometry(260,420,100,30)
        self.remove_item.clicked.connect(self.removefromlist)

        self.save = QPushButton("Save",self)
        self.save.setGeometry(260,460,100,30)
        self.save.clicked.connect(self.savechanges)

	######## Second section #########
        
        self.table_headers = ["Name","Opening Stock","Added","Sold","Closing Stock","Date"]
        self.information_table = QTableWidget(self)
        self.information_table.setGeometry(380,50,620,180)
        #self.information_table.setRowCount(3)
        self.information_table.setAlternatingRowColors(True)
        self.information_table.setStyleSheet("alternate-background-color: gray; background-color: white")
        self.information_table.setColumnCount(len(self.table_headers))
        for i in range(len(self.table_headers)):
            self.information_table.setHorizontalHeaderItem(i,QTableWidgetItem(self.table_headers[i]))
        self.setWindowTitle("Data Stocks")
        self.setGeometry(100,100,900,600)

        
        self.table2_headers = ["Name","Bought","Sold","B_Price","S_Price","Profit","Month"]
        self.information_table2 = QTableWidget(self)
        self.information_table2.setGeometry(380,330,750,240)
        #self.information_table2.setRowCount(3)
        self.information_table2.setAlternatingRowColors(True)
        self.information_table2.setStyleSheet("alternate-background-color: gray; background-color: white")
        self.information_table2.setColumnCount(len(self.table2_headers))
        for i in range(len(self.table2_headers)):
            self.information_table2.setHorizontalHeaderItem(i,QTableWidgetItem(self.table2_headers[i]))

        self.total_amount_lbl = QLabel("Total Profit : ",self)
        self.total_amount_lbl.setGeometry(380,280,120,30)
        self.total_amount_lbl.setStyleSheet("color: black")
        self.total_amount_lbl.setFont(QFont("Times",16))

        self.total_disp_lbl = QLabel(self)
        self.total_disp_lbl.setGeometry(500,280,140,30)
        self.total_disp_lbl.setStyleSheet("color: blue")
        self.total_disp_lbl.setAlignment(Qt.AlignCenter)
        self.total_disp_lbl.setFont(QFont("Times",16))
        
        #### Search filters monthly 
        self.month_dict = {"January":1 ,"February":2 ,"March":3 ,"April":4 ,"May":5 ,"June":6 ,"July":7 ,"August":8 ,"September":9 ,"October":10 ,"November":11,"December":12}
        months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
        self.month_combo = QComboBox(self)
        self.month_combo.setGeometry(700,280,120,30)
        self.month_combo.addItems(months)

        self.year_input = QLineEdit(self)
        self.year_input.setGeometry(840,280,100,30)

        self.show_btn = QPushButton("Show Summary",self)
        self.show_btn.setGeometry(980,280,140,30)
        self.show_btn.clicked.connect(self.showsummary)
        self.pressed = 0

        self.setWindowTitle("Data Stocks")
        self.setGeometry(100,80,1150,640)

    def getproducts(self):
        query = "select * from products;"
        try:
            self.cur.execute("select * from products;")
            result = self.cur.fetchall()
            return result
        except Exception, e:
            QMessageBox.information(self,"Database Error","Failed to get products "+str(e))
            return []

    def productselected(self,name):
        self.cur_prod = self.product_name_combo.currentText()

        try:
            self.cur.execute("select p_id from products where pname like %s;",[str(self.cur_prod)])
            result = self.cur.fetchall()
            self.product_id = result[0][0]
        except Exception, e:
            QMessageBox.information(self,"Database Error","Failed to get product id "+str(e))
            return

        try:
            self.cur.execute("select * from daily_records where p_id = %s;",[self.product_id])
            result = self.cur.fetchall()
            self.daily_sale = result
            self.opening_lbl.setText(str(self.daily_sale[0][1]))
            self.availabel_lbl.setText(str(self.daily_sale[0][1]))
        except Exception,e:
            QMessageBox.information(self,"Database Error","Failed to get Daily records "+str(e))
            return


    def check(self,new):
        try:
            new = int(new)
        except Exception,e:
            if new == '':
                self.availabel_lbl.setText(str(int(self.opening_lbl.text()) + 0))  
                self.availabel_val = int(self.availabel_lbl.text())
            else:
                QMessageBox.information(self,"Input Value Error","Value has to be a number ")
            return
        self.availabel_lbl.setText(str(int(self.opening_lbl.text()) + new)) 
        self.availabel_val = int(self.availabel_lbl.text())

    def closevalue(self,new):
        try:
            new = int(new)
        except Exception,e:
            if new == '':
                self.availabel_lbl.setText(str( self.availabel_val - 0))
                self.availabel_val = int(self.availabel_lbl.text())
            else:
                QMessageBox.information(self,"Input Value Error","Value has to be a number ") 
            return
        self.availabel_lbl.setText(str( self.availabel_val - new))        


    def showsummary(self):
        self.information_table2.setRowCount(0)
        self.monthval = str(self.month_combo.currentText())
        self.yearval = str(self.year_input.text()).strip()

        if self.yearval == '':
            QMessageBox.information(self,"Input Value Error","Make sure Year is provided.. Enter Year to continue")
            return

        if len(self.yearval) != 4:
            QMessageBox.information(self,"Input Value Error","Please Enter 4 digits for the year")
            return

        try:
            self.yearval = int(self.yearval)
        except Exception,e:
            QMessageBox.information(self,"Input Value Error","The year value has to be a number") 
            return


        query = "select sum(quantity_add), sum(quantity_sold) , sales.p_id from sales where extract(month from sale_date) = %s and extract(year from sale_date) = %s group by p_id;"


        self.data = [self.month_dict[self.monthval],self.yearval]

        try:
            self.cur.execute(query,self.data)
            result = self.cur.fetchall()
        except Exception,e:
            QMessageBox.information(self,"Database Error","Could not get sales data "+str(e))
            return

        display = []
        if result != []:
            for val in result:
                disp_item = []
                try:
                    self.cur.execute("select pname, buy_price, sell_price from products where p_id = %s",[val[2]])
                    prod_res = self.cur.fetchall()
                    if prod_res != []:
                        for i in prod_res[0]:
                            disp_item.append(i)
                        disp_item.insert(1,val[0])
                        disp_item.insert(2,val[1])
                        display.append(disp_item)
                except Exception,e:
                    QMessageBox.information(self,"Database Error",str(e))
                    return
            
            total_p = 0
            fin_lst = []
            for val in display:
                profit = (val[4] - val[3]) * val[2]
                total_p += profit
                val.insert(5,int(profit))
                val.insert(6,self.monthval)

                fin_lst.append(val)

            self.total_disp_lbl.setText(str(total_p))
            self.information_table2.setRowCount(len(fin_lst))

            
            for row in range(len(fin_lst)):
                for col in range(7):
                    self.information_table2.setItem(row,col,QTableWidgetItem(str(fin_lst[row][col])))
        else:
            pass


    def addtolist(self):
        self.pname =  str(self.product_name_combo.currentText())
        self.openstock = str(self.opening_lbl.text()).strip() 
        self.addedval = str(self.added_stock_input.text()).strip()
        self.soldval = str(self.sold_stock_input.text()).strip()
        self.closestock = str(self.availabel_lbl.text()).strip()
        self.dateval = self.date_input.date().toPyDate()

        if self.openstock == '' and self.addedval == '' and  self.soldval == '' and self.closestock == '':
            self.openstock = 0
            self.addedval = 0
            self.soldval = 0
            self.closestock = 0
        elif self.addedval == '' and self.soldval == '':
            self.addedval = 0
            self.soldval = 0
        elif self.addedval != '' and self.soldval == '':
            self.soldval = 0
        elif self.addedval == '' and self.soldval != '':
            self.addedval = 0
        elif self.closestock == '':
            self.closestock = 0
        else:
            pass


        if not self.data_dict.has_key(self.pname):
            self.data_dict[self.pname] = [self.openstock,self.addedval,self.soldval,self.closestock,str(self.dateval),self.product_id]
            self.added_products_list.addItem(self.pname)
            self.opening_lbl.setText(str(self.availabel_lbl.text())) 
            self.added_stock_input.clear()
            self.sold_stock_input.clear()
            self.availabel_lbl.clear()
        else:
            QMessageBox.information(self,"Repetition of content","Value you are trying to add is already added, value exists")

    def removefromlist(self):
        if self.added_products_list.count() < 1:
            pass
        else:
            self.remove_items = self.added_products_list.selectedItems()
            if not self.remove_items:
                QMessageBox.information(self,"Removing content","Nothing to remove")
                return

            del self.data_dict[str(self.added_products_list.currentItem().text())]

            for item in self.remove_items:
                self.added_products_list.takeItem(self.added_products_list.row(item))

    def savechanges(self):
        if self.added_products_list.count() < 1:
            pass
        else:
            lst = []
            for val in self.data_dict.keys():
                lst2 = []
                lst2.append(val)
                for item in self.data_dict[val]:
                    lst2.append(item)

                lst.append(lst2)

            query = "insert into sales(opening_stock , quantity_add , quantity_sold , closing_stock , sale_date , p_id) values(%s,%s,%s,%s,%s,%s);"
            query2 = "update daily_records set quantity_available=%s, date = %s where p_id = %s; "
            try:
                for val in lst:
                    self.data = [val[1],val[2],val[3],val[4],val[5],val[6]]
                    self.data2 = [val[4],val[5],val[6]]
                    try:
                        self.cur.execute(query,self.data)
                        self.cur.execute(query2,self.data2)
                        self.conn.commit()
                        QMessageBox.information(self,"Adding Data","Successfully Saved the data")
                    except Exception,e:
                        QMessageBox.information(self,"Database Error","Data was NOT SAVED "+str(e)) 
                        self.conn.rollback()
                        return
            except Exception,e:
                QMessageBox.information(self,"Database Error","An error occured "+str(e)) 
                return

            self.information_table.setRowCount(len(lst))
 
            for row in range(len(lst)):
                for col in range(6):
                    self.information_table.setItem(row,col,QTableWidgetItem(lst[row][col]))

            self.added_products_list.clear()
            self.data_dict.clear()



'''
app = QApplication(sys.argv)
comb = combined()
comb.show()
sys.exit(app.exec_())
'''
