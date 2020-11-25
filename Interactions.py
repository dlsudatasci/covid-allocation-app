# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 15:04:30 2020

@author: tapiaj
"""


import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from MainWindow import *
import vacmodel as vm

class VAC_App(QMainWindow):
   
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Add_Group.clicked.connect(self.add)
        self.ui.Solve_Model.clicked.connect(self.solve)
        self.Group =[]
        
    def add(self):
        self.Group.append(self.ui.GroupName.text())
        self.ui.Group_List.addItem(self.ui.GroupName.text())
        CRrc = self.ui.ContactRate.rowCount()
        CRrc_2 = self.ui.ContactRate.columnCount()
        CRrc_3 = self.ui.Pop_PerGroup.rowCount()
        CRrc_4 = self.ui.Pop_PerGroup.rowCount()
        self.ui.ContactRate.insertRow(CRrc)
        self.ui.ContactRate.insertColumn(CRrc_2)
        self.ui.ContactRate.setHorizontalHeaderLabels(self.Group)
        self.ui.ContactRate.setVerticalHeaderLabels(self.Group)
        self.ui.Pop_PerGroup.insertRow(CRrc_3)
        self.ui.Pop_PerGroup.setVerticalHeaderLabels(self.Group)
        self.ui.GroupName.setText('')
        self.ui.GroupName.setFocus()
        

    def solve(self):
        #store Groups
        vm.Group=self.Group
    
        #store Contact Rate Data
        CR_data = []
        for i in range(self.ui.ContactRate.rowCount()):
            for j in range(self.ui.ContactRate.columnCount()):
                CR_data.append(float(self.ui.ContactRate.item(i,j).text()))
        vm.Kmatval = CR_data
        
        #store Population Data
        Pop_data = []
        for i in range(self.ui.Pop_PerGroup.rowCount()):
            Pop_data.append(int(self.ui.Pop_PerGroup.item(i,0).text()))
        vm.N0=dict(zip(vm.Group, Pop_data))
        vm.fn0 ={k:0.5 for k in vm.Group}
        
        #store Vaccine Efficacy
        vm.H = self.ui.efficacy_value.value()
                
        #run model
        solution = vm.model_setup()
        
        #store value in Widgets
        qtresult = MyTableModel([solution[0]])
        self.ui.tableView.setModel(qtresult)
        
if __name__=="__main__":
    app = QApplication(sys.argv)
    w = VAC_App()
    w.show()
    sys.exit(app.exec_())