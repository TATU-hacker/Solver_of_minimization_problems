# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog

class Ui_bandwidthDialog(QDialog):

    def setupUi(self, bandwidthDialog):
        bandwidthDialog.setObjectName("BandwidthDialog")
        bandwidthDialog.resize(400, 300)

        self.retranslateUi(bandwidthDialog)
        QtCore.QMetaObject.connectSlotsByName(bandwidthDialog)

    def retranslateUi(self, bandwidthDialog):
        _translate = QtCore.QCoreApplication.translate
        bandwidthDialog.setWindowTitle(_translate("BandwidthDialog", "Dialog"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    bandwidthDialog = QtWidgets.QDialog()
    ui = Ui_bandwidthDialog()
    ui.setupUi(bandwidthDialog)
    bandwidthDialog.show()
    sys.exit(app.exec_())
