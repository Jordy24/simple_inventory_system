#!/usr/bin/python

import os,sys,time
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class administration(QWidget):
    def __init__(self,conn=None,):
        super(administration,self).__init__()

        try:
            self.conn = conn
            self.cur = self.conn.cursor()
        except Exception, e:
            QMessageBox.information(self,"Database Error","Error in get connection:\n"+str(e))

        self.product_added = []

        ###
        self.db_data = self.getproducts()
        ###
        self.header_lbl = QLabel("Product Details",self)
        self.header_lbl.setGeometry(10,10,620,30)
        self.header_lbl.setStyleSheet("background-color: brown;border-radius: 14px")
        self.header_lbl.setAlignment(Qt.AlignCenter)

        self.pname_lbl = QLabel("Product Name: ",self)
        self.pname_lbl.setGeometry(20,50,140,30)

        self.buyprice_lbl = QLabel("Buying Price: ",self)
        self.buyprice_lbl.setGeometry(20,90,140,30)

        self.sellprice_lbl = QLabel("Selling Price: ",self)
        self.sellprice_lbl.setGeometry(20,130,140,30)

        ## Displaying labels
        self.pname_input = QLineEdit(self)
        self.pname_input.setGeometry(160,50,160,30)

        self.buyprice_input = QLineEdit(self)
        self.buyprice_input.setGeometry(160,90,160,30)

        self.sellprice_input = QLineEdit(self)
        self.sellprice_input.setGeometry(160,130,160,30)

        self.plist_lst = QListWidget(self)
        self.plist_lst.setGeometry(340,50,280,300)
        for val in self.db_data:
            self.plist_lst.addItem(val[1])

        self.plist_lst.itemClicked.connect(self.itemselected)

        ## Buttons
        self.add_product = QPushButton("ADD PRODUCT",self)
        self.add_product.setGeometry(120,180,120,30)
        self.add_product.clicked.connect(self.addproduct)

        self.cancel_btn = QPushButton("CANCEL",self)
        self.cancel_btn.setGeometry(120,220,120,30)
        self.cancel_btn.clicked.connect(self.cancel)

        self.edit_btn = QPushButton("EDIT",self)
        self.edit_btn.setGeometry(120,260,120,30)
        self.edit_btn.clicked.connect(self.edit)

        self.update_btn = QPushButton("UPDATE",self)
        self.update_btn.setGeometry(120,300,120,30)
        self.update_btn.clicked.connect(self.update)

        self.done_btn = QPushButton("DONE",self)
        self.done_btn.setGeometry(500,370,120,30)
        self.done_btn.clicked.connect(self.quit)
        ####

        self.setWindowTitle("Administrative Section")
        self.setGeometry(300,300,640,420)

    def getproducts(self):
        query = "select * from products;"
        try:
            self.cur.execute("select * from products;")
            result = self.cur.fetchall()
            return result
        except Exception, e:
            QMessageBox.information(self,"Database Error","Failed to get products: "+ str(e))
            return []

    def itemselected(self):
        self.old_pname = self.plist_lst.currentItem().text()
        for val in self.db_data:
            if str(self.old_pname) == val[1]:
                self.pname_input.setText(str(self.old_pname))
                self.pname_input.setReadOnly(True)
                self.buyprice_input.setText(str(val[2]))
                self.buyprice_input.setReadOnly(True)
                self.sellprice_input.setText(str(val[3]))
                self.sellprice_input.setReadOnly(True)
                break


    def addproduct(self):
        self.data_lst = []
        if str(self.pname_input.text()) == '':
            QMessageBox.information(self,"Input value error","Name can not be empty")
            return
        if str(self.buyprice_input.text()) == '':
            QMessageBox.information(self,"Input value error","Buying price can not be empty: ")
            return
        if str(self.sellprice_input.text()) == '':
            QMessageBox.information(self,"Input value error","Selling price can not be empty")
            return

        try:
            self.buying_p = int(str(self.buyprice_input.text()).strip())  
            self.selling_p = int(str(self.sellprice_input.text()).strip())
        except:
            QMessageBox.information(self,"Input value error","Price values have to be numbers only")
            return

        self.pname = str(self.pname_input.text()).lower().strip()
        if self.db_data != []:
            for val in self.db_data:
                if self.pname == val[1]:
                    QMessageBox.information(self,"Value exists","The product name already exists, enter another name ")
                    return

        query = "insert into products(pname,buy_price,sell_price) values(%s,%s,%s);"
        self.data_lst = [self.pname,self.buying_p,self.selling_p]
        try:
            self.cur.execute(query,self.data_lst)
            self.conn.commit()
            self.plist_lst.addItem(self.pname)
            self.product_added.append(self.pname)
            QMessageBox.information(self,"Addition of data","Successfully added the product ")
        except Exception, e:
            QMessageBox.information(self,"Database Error","Failed to add product "+ str(e))
            self.conn.rollback()
            return
        
        try:
            self.cur.execute("select p_id from products where pname like %s",[self.pname])
            result = self.cur.fetchall()
            self.product_id = result[0][0]
        except Exception, e:
            QMessageBox.information(self,"Database Error","Could not get required product id "+ str(e))
            return


        query = "insert into daily_records(quantity_available, date, p_id) values(%s,%s,%s);"
        self.data = [0, time.strftime('%Y-%m-%d'), self.product_id]

        try:
            self.cur.execute(query,self.data)
            self.conn.commit()
        except Exception, e:
            QMessageBox.information(self,"Database Error","Failed to add daily records "+ str(e))
            self.conn.rollback()
            return

    def cancel(self):
        self.pname_input.clear()
        self.buyprice_input.clear()
        self.sellprice_input.clear()

        self.edit()

    def edit(self):
        self.pname_input.setReadOnly(False)
        self.buyprice_input.setReadOnly(False)
        self.sellprice_input.setReadOnly(False)

    def update(self):
        self.data_lst = []
        if str(self.pname_input.text()) == '':
            QMessageBox.information(self,"Input value Error","Name can not be empty")
            return
        if str(self.buyprice_input.text()) == '':
            QMessageBox.information(self,"Input value Error","Buying price can not be empty")
            return
        if str(self.sellprice_input.text()) == '':
            QMessageBox.information(self,"Input value Error","Selling price can not be empty")
            return

        try:
            self.buying_p = int(str(self.buyprice_input.text()).strip())  
            self.selling_p = int(str(self.sellprice_input.text()).strip())
        except:
            QMessageBox.information(self,"Input value Error","Prices have to be numbers only")
            return

        self.pname = str(self.pname_input.text()).lower().strip()

        query = "update products set pname=%s ,buy_price=%s, sell_price=%s where pname like %s;"
        self.data_lst = [self.pname,self.buying_p,self.selling_p,str(self.old_pname)]
        try:
            self.cur.execute(query,self.data_lst)
            self.conn.commit()
            sel_item = self.plist_lst.selectedItems()
            for item in sel_item:
                item.setText(self.pname)
        except Exception, e:
            QMessageBox.information(self,"Database Error","Failed to update daily records\n"+str(e))
            self.conn.rollback()
            return

    def added_products(self):
        return self.product_added

    def quit(self):
        try:
            self.close()
        except Exception, e:
            QMessageBox.information(self,"Exit Error","During exit: "+str(e))

# For Debugging this form
'''
app = QApplication(sys.argv)
admin = administration()
admin.show()
sys.exit(app.exec_())
'''
