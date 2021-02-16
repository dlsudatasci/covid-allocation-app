# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 15:04:30 2020

@author: tapiaj
"""

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from MainWindow import *
import Model as model
import json

import xlwt 
from xlwt import Workbook 

class VAC_App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Add_Group.clicked.connect(self.add)
        self.ui.Solve_Model.clicked.connect(self.solve)
        self.ui.actionSave_Data.triggered.connect(self.saveFile)
        self.ui.actionSave_As.triggered.connect(self.saveFileAs)
        self.ui.actionLoad_Data.triggered.connect(self.loadFile)
        self.Group =[]

        self.file = None

    def reset(self):
        self.Group =[]
        self.ui.Pop_PerGroup.setRowCount(0)
        self.ui.Pop_PerGroup.setColumnCount(1)
        self.ui.ContactRate.setRowCount(0)
        self.ui.ContactRate.setColumnCount(0)
        self.ui.efficacy_value.setValue(0)
        while self.ui.Group_List.count() != 0:
            self.ui.Group_List.takeItem(0)

    def loadFile(self):
        self.file = self.ui.open()
        self.reset()

        with open(self.file) as json_file:
            data = json.load(json_file)
            print(data)

            pop_groups = data['population_groups']
            for grp in pop_groups:
                self.add(grp['name'])

            self.ui.efficacy_value.setValue(data['vaccine_efficacy'])

            for i in range(self.ui.Pop_PerGroup.rowCount()):
                val = pop_groups[i]['size']
                self.ui.Pop_PerGroup.setItem(i,0,QTableWidgetItem(str(val)))

            groups = [grp['name'] for grp in pop_groups]
            for cr in data['contact_rates']:
                col = groups.index(cr['col'])
                row = groups.index(cr['row'])
                val = cr['val']
                self.ui.ContactRate.setItem(row,col,QTableWidgetItem(str(val)))
        
    def saveFileAs(self):
        self.file = None
        self.saveFile()

    def saveFile(self):
        if self.file is None:
            self.file = self.ui.saveAs()

        data = self.retrieveData()
        print(data)
        errors = data['errors']
        ve = data['ve']
        groups = data['groups']
        Pop_data = data['Pop_data']
        CR_data = data['CR_data']

        if len(errors) != 0:
            return

        toSave = {}
        toSave["vaccine_efficacy"] = ve
        toSave["population_groups"] = []
        toSave["contact_rates"] = []

        for i, group in enumerate(groups):
            toSave["population_groups"].append({
                "name":group,
                "size":Pop_data[i]
                })

        cur = 0
        for i, row in enumerate(groups):
            for j, col in enumerate(groups):
                print(row)
                print(col)
                print("----")
                toSave["contact_rates"].append({
                    "col":col,
                    "row":row,
                    "val":CR_data[cur]
                })
                cur += 1


        ext = '.json' if '.json' not in self.file else ''
        with open(self.file+ext, 'w') as outfile:
            json.dump(toSave, outfile)

        
    def add(self, name=None):
        groupname = name if name else self.ui.GroupName.text()
        print(groupname)
        if (groupname == ''):
            print("Groupname cannot be empty")
            return
        self.Group.append(groupname)
        self.ui.Group_List.addItem(groupname)
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

    def retrieveData(self):
        errors = []

        # retrieve data from the UI
        # retrieve contact rate data
        CR_data = []
        for i in range(self.ui.ContactRate.rowCount()):
            for j in range(self.ui.ContactRate.columnCount()):
                try:
                    cell = self.ui.ContactRate.item(i,j).text()
                    CR_data.append(float(cell))
                except Exception as e:
                    e = str(e)
                    err = ''
                    if ('NoneType' in e):
                        err = "Value cannot be empty"
                    if ('convert' in e):
                        err = "Value cannot be string"
                    errors.append(err)
                    print(e + ": "+err)
                
        # retrieve population data
        Pop_data = []
        for i in range(self.ui.Pop_PerGroup.rowCount()):
            try:
                Pop_data.append(int(self.ui.Pop_PerGroup.item(i,0).text()))
            except Exception as e:
                e = str(e)
                err = ''
                if ('NoneType' in e):
                    err = "Value cannot be empty"
                if ('convert' in e):
                    err = "Value cannot be string"
                errors.append(err)
                print(e + ": "+err)
            
        # retrieve vaccine efficiency value
        ve = self.ui.efficacy_value.value()

        # retrieve list of groups
        groups = self.Group

        return {'errors':errors,'ve':ve,'groups':groups,'Pop_data':Pop_data,'CR_data':CR_data}


    def solve(self):
        data = self.retrieveData()
        errors = data['errors']
        ve = data['ve']
        groups = data['groups']
        Pop_data = data['Pop_data']
        CR_data = data['CR_data']

        # saving to excel
        if len(errors) == 0:
            wb = Workbook() 

            # add_sheet is used to create sheet. 
            sheet1 = wb.add_sheet('Groups') 

            for i in range(0,len(groups)):
                cur_group = groups[i]
                cur_pop = Pop_data[i]
                sheet1.write(i, 0, cur_group) 
                sheet1.write(i, 1, cur_pop) 
            sheet1.write(len(groups), 0, "Vaccine Efficacy") 
            sheet1.write(len(groups), 1, ve) 

            sheet2 = wb.add_sheet('Contact Rates') 
            for i in range(0,len(CR_data)):
                cur_cr = CR_data[i]
                sheet2.write(i,0,cur_cr)
            wb.save('sample.xls') 

        #store Groups
        # vm.Group=self.Group
    
        # #store Contact Rate Data
        # CR_data = []
        # for i in range(self.ui.ContactRate.rowCount()):
        #     for j in range(self.ui.ContactRate.columnCount()):
        #         CR_data.append(float(self.ui.ContactRate.item(i,j).text()))
        # vm.Kmatval = CR_data
        
        # #store Population Data
        # Pop_data = []
        # for i in range(self.ui.Pop_PerGroup.rowCount()):
        #     Pop_data.append(int(self.ui.Pop_PerGroup.item(i,0).text()))
        # vm.N0=dict(zip(vm.Group, Pop_data))
        
        # #store Vaccine Efficacy
        # vm.H = self.ui.efficacy_value.value()
                
        # #run model
        # solution = vm.model_setup()
        
        # #store value in Widgets
        # qtresult = MyTableModel([solution[0]])
        # self.ui.tableView.setModel(qtresult)

        #Print out data grabbed from View
        fn0 ={k:0.5 for k in groups}
        N0=dict(zip(groups, Pop_data))
        Kmatval = CR_data
        H = ve
        print('Groups:',groups)
        print('Pop. Data:',Pop_data)
        print('fn0:',fn0)
        print('Contact Rates:',CR_data)
        print('Vaccine Efficiency:',ve)

        solution = model.run('vac',groups,N0,fn0,Kmatval,H)
        print(solution)