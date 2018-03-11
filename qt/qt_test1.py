# my Qt test file
#
# песочница на примере заполнения в GUI параметров для создания конфига

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import *
import sys
import time

def tmstamp():
    return  time.ctime(time.time())

def echo_mantra():
    print('Ом Намах Шивайя! %s' %tmstamp())

def items_add():
    try:
        bd = ('neighbor:\t ' + window.textEdit_BD.toPlainText())
        iface_type = window.comboBox_Iface.currentText()
        iface = window.textEdit_Iface.toPlainText()
        iface_full = ('interface:\t ' + iface_type + iface)
        neighbor = ('neighbor: \t' + window.textEdit_Neigh.toPlainText())
        neighbor2 = ('neighbor2:\t ' + window.textEdit_Neigh2.toPlainText())
        speed = ('speed:\t ' + window.comboBox_Speed.currentText())
        vlan = ('vlan:\t ' + window.textEdit_Vlan.toPlainText())
        vpn = ('vpn:\t ' + window.textEdit_Vpn.toPlainText())

        window.listWidget_Wind1.addItem(bd) if bd else window.listWidget_Wind1.addItem(echo_mantra())
        window.listWidget_Wind1.addItem(iface_full) if iface else window.listWidget_Wind1.addItem(echo_mantra())
        window.listWidget_Wind1.addItem(neighbor) if iface else window.listWidget_Wind1.addItem(echo_mantra())
        window.listWidget_Wind1.addItem(neighbor2) if iface else window.listWidget_Wind1.addItem(echo_mantra())
        window.listWidget_Wind1.addItem(speed) if iface else window.listWidget_Wind1.addItem(echo_mantra())
        window.listWidget_Wind1.addItem(vlan) if iface else window.listWidget_Wind1.addItem(echo_mantra())
        window.listWidget_Wind1.addItem(vpn) if iface else window.listWidget_Wind1.addItem(echo_mantra())
    except Exception as e:
        print(e)


# создаем объект класса
app = QtWidgets.QApplication(sys.argv)
window = uic.loadUi('test_form.ui')

# вешаем связку сигнал-слот
#window.pushOk1.clicked.connect(echo_mantra)
window.pushButton_Commit.clicked.connect(items_add)

# показываем форму
window.show()
sys.exit(app.exec_())
