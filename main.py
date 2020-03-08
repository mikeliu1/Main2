import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot, QSize, Qt
from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
from Qt_Main import Ui_Form
from structure import Ui_structure
"""
20200302
写入了write方法，主要用于写入操作
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
        self.pushButton_3.clicked.connect(self.write)

    def open(self):
        """
        打开mesh文件,并且将求解器类型打印到窗口
        """
        open_filename = QFileDialog.getOpenFileName(self, "choose file")
        print(open_filename[0])
        mesh_file = common_method()
        #输出求解器类型
        self.label_5.setText( mesh_file.solver_type(open_filename))

    def write(self):
        """
        solver button 的方法定义
        :return:
        """
        print(self.lineEdit.text())
        a = self.lineEdit.text()
        try :
            a = float(a)
        except Exception:
            QMessageBox.information(self, 'message', 'Please input a number')

    # @pyqtSlot()
    # def on_pushButton3_clicked(self):
    #     print(self.lineEdit.text())


    #self.textBrowser.setText(mesh_file.solver_type())

    # @pyqtSlot()
    # def textBrowser_init(self):
    #     self.textBrowser.textChanged.connect(self.on_pushButton_clicked)
#结构模块结束

class common_method():
    def __init__(self):
        self.component_number1 = []
        self.component_number2 = []
        self.set = []


    def solver_type(self,path):
        """
        获取求解器类型
        """
        self.path = path[0]
        self.solver_file = open(r'{}'.format(path[0]), 'r')
        solver = {'fem': 'Optistruct', 'inp': 'ABAQUS', 'bdf': 'NASTRAN'}
        solver1 = [self.path]
        #solver_type = solver[self.on_pushButton_clicked.open_filename[0][-3:]]
        solver_type = solver[solver1[0][-3:]]
        return solver_type
        #print(solver_type)

    def component_number(self):
        """
        获取component number,仅支持nastran格式
        """
        #solver_file = open(self.on_pushButton_clicked.solver_type)

        for i in self.solver_file.readlines():
            if i[:6] == 'CQUAD4' or 'CTETRA':
                self.component_number1.append(int(i[20:24].strip()))
        self.component_number2 = common_method.remove_duplication(self.component_number1)
        print('com number:', self.component_number2)
        return len(self.component_number2)

    def get_set(self):
        '''
        获取求解文件set
        :return:
        '''
        for i in self.solver_file.readlines():
            if i[0:3] == 'SET':
                self.set.append(i.split('=')[1].strip()[:-1])
        return self.set

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
    def __init__(self):
        super(write_method, self).__init__()
        self.spc = []
        self.load_id = [3,4,5,6,7,8,9,10]#
        self.a = []  #spcd
        self.b = []  #spc
        self.freedom = [1,2,3,4,5,6]


    def material(self):
        pass

    def load(self,acc):
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
