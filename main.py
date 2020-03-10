import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot, QSize, Qt
from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
from Qt_Main import Ui_Form
from structure import Ui_structure
import numpy as np
import pandas as pd

"""
20200302
写入了write方法，主要用于写入操作
20200310
添加了材料列表，使用了pandas
"""

class main_interface(QtWidgets.QMainWindow, Ui_Form):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    @pyqtSlot()
    def on_Structure_clicked(self):
        """
        打开结构模块
        """
        bookinfo = Structure()
        bookinfo.show()
        sys.exit(bookinfo.exec_())
    #     r = bookinfo.exec_()
    #     if r > 0:
    #         self.showtable()
    # #bookinfo.show()
#结构模块：

class Structure(QtWidgets.QDialog,Ui_structure):
    def __init__(self, parent=None):
        super(Structure, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.open)
        self.pushButton_2.clicked.connect(self.material_setting)

        self.pushButton_3.clicked.connect(self.write)
        self.open_filename = []
        mode = common_method(self.open_filename)
        self.comboBox_2.addItems(mode.material_list())



    def open(self):
        """
        打开mesh文件,获取路径path（self.open_filename），并且将求解器类型打印到窗口
        """
        self.open_filename = QFileDialog.getOpenFileName(self, "choose file")
        print(self.open_filename[0])
        # 输出求解器类型
        mesh_file = common_method(self.open_filename)
        self.label_5.setText( mesh_file.solver_type())

    def material_setting(self):
        """
        设置材料和属性
        :return:

        """
        pass



    def write(self):
        """
        solver button 的方法定义,模态模块
        :return:
        """
        print(self.lineEdit.text())
        self.mode_target = self.lineEdit.text()
        try :
            self.mode_target = float(self.mode_target)
        except Exception:
            QMessageBox.information(self, 'message', 'Please input a number')
        #写模态文件,需要加self吗？
        self.mode = write_method(self.open_filename)
        self.mode.Mode(self.mode_target)

    # @pyqtSlot()
    # def on_pushButton3_clicked(self):
    #     print(self.lineEdit.text())


    #self.textBrowser.setText(mesh_file.solver_type())

    # @pyqtSlot()
    # def textBrowser_init(self):
    #     self.textBrowser.textChanged.connect(self.on_pushButton_clicked)
#结构模块结束

class common_method():
    '''
    该类主要争对网格文件进行识别，包括求解类型，零部件数量，set节点列表
    '''
    def __init__(self,path):
        self.component_number1 = []
        self.component_number2 = []
        self.set = []
        self.path = path

    def open_solver(self):
        """
        打开网格文件
        :param path:
        :return:
        """
        self.solver_file = open(r'{}'.format(self.path[0]), 'r')

    def solver_type(self):
        """
        根据文件路径，获取求解器类型。改进：针对无后缀或作不是别后缀做出警告。
        """
        self.path = self.path[0]
        solver = {'fem': 'Optistruct', 'inp': 'ABAQUS', 'bdf': 'NASTRAN'}
        solver1 = [self.path]
        solver_type = solver[solver1[0][-3:]]
        return solver_type
        #print(solver_type)

    def component_number(self):
        """
        获取component number,仅支持nastran格式,返回值是零件数量
        """
        #solver_file = open(self.on_pushButton_clicked.solver_type)
        self.open_solver()
        for i in self.solver_file.readlines():
            if i[:6] == 'CQUAD4' or 'CTETRA':
                self.component_number1.append(int(i[20:24].strip()))
        self.component_number2 = common_method.remove_duplication(self.component_number1)
        print('com number:', self.component_number2)
        return len(self.component_number2)

    def get_set(self):
        '''
        获取求解文件set，返回值是set列表
        :return:
        '''
        self.open_solver()
        for i in self.solver_file.readlines():
            if i[0:3] == 'SET':
                self.set.append(i.split('=')[1].strip()[:-1])
        self.solver_file.close()
        return self.set

    def material_list(self):
        """
        获取材料列表
        :return:
        """
        material_list = pd.read_csv(open(r'D:\python_study\python_study\PYTHON\Python\material.csv'))
        Material_Name_list = list(material_list['Material_Name'])

        return Material_Name_list
    @classmethod
    def remove_duplication(cls, list1):
        """
        去除列表中的重复项
        :param list1:
        :return:
        """
        list2 = []
        for i in list1:
            if i not in list2:
                list2.append(i)
        return list2

    def is_number(self,s):
        """
        判断输入是否为数字
        :param s:
        :return:
        """
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False

class write_method(common_method):
    def __init__(self,path):
        super().__init__(path)
        self.spc = []
        self.load_id = [3,4,5,6,7,8,9,10]#
        self.a = []  #spcd
        self.b = []  #spc
        self.freedom = [1,2,3,4,5,6]


    def Material(selfmaterial,Material):

        pass

    def Static(self):
        pass
#Moode,FR = frequency
    def Mode(self, target_FR):
        """
        SUBCASE        1
        LABEL modal
        ANALYSIS MODES
        METHOD(STRUCTURE) =        1
        BEGIN BULK
        INCLUDE '**********'
        PSHELL         1       10.1            1               1        0.0
        MAT1           1210000.0        0.3     7.85-9
        EIGRL          1           200.0                                    MASS
        ENDDATA
        """
        self.fixed = self.get_set()
        self.target_FR = target_FR
        self.key_words ="""
SUBCASE        1
LABEL modal
ANALYSIS MODES
METHOD(STRUCTURE) =        1
BEGIN BULK
INCLUDE '{}'
PSHELL         1       10.1            1               1        0.0
MAT1           1210000.0        0.3     7.85-9
EIGRL,1,,{},,,,,MASS
ENDDATA
        """
        print(self.key_words)
        with open(r'C:\Users\MIKE\Desktop\simulation_test\Frequency_solver','w') as mode:
            mode.write(self.key_words.format(self.path[0], self.target_FR))




#vibration
    def Vibration(self,acc):
        self.acc = acc
        self.ACC = ''
        #获取spc集合点
        if len(self.get_set()) == 1:
            self.spc = list(map(int, self.get_set()[0].split(',')))
        else:
            pass
        #SPCD id 4-6
        for j in range(0,3):
            for i in range(len(self.spc)):
                self.a.append( 'SPCD, '+ str(self.load_id[i+1])+','+ str(self.spc[i])+',' +str(self.freedom[j])+ ',1.0')
        #SPC id 3
        for i in range(len(self.spc)):
            self.b.append( 'SPC, ' + str(self.load_id[0]) + ',' + str(self.spc[i]) + ',' + '123456' + ',0.0')

        #加速度 id 7

        self.ACC = 'TABLED1 7 LINEAR LINEAR /n +, 0.0, '+ str(self.acc*9810)+',1000.0,'+ str(self.acc*9810)+', ENDT'

        #rload
        self.rload = '''
        RLOAD1         8       4                       7       0    ACCE
        RLOAD1         9       5                       7       0    ACCE
        RLOAD1        10       6                       7       0    ACCE'''

        return self.a ,self.b


    def others(self):
        eigrl_freqi = '''
        FREQ1          2     1.0     1.0    1000
        EIGRL          1                      20  '''
        pass



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv) #qt必须有的 其中 sys.argv是要传递参数,sys.argv是一个外部的参数传入列表
    app.setStyle('Fusion')
    main_interface = main_interface()
    main_interface.show()
    sys.exit(app.exec_())
# if __name__ == '__main__':
#     test1 = common_method()
#     #test2 = test1.component_number()
#     test3 = test1.get_set()
#     test4 = write_method(5)
#     print(test4.load())
#     print(test3)
