# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_LandXmlDialog.ui'
#
# Created: Thu Apr 30 13:09:50 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_LandXmlDialog(object):
    def setupUi(self, LandXmlDialog):
        LandXmlDialog.setObjectName(_fromUtf8("LandXmlDialog"))
        LandXmlDialog.setWindowModality(QtCore.Qt.NonModal)
        LandXmlDialog.resize(476, 130)
        LandXmlDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtGui.QVBoxLayout(LandXmlDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.uXmlFileLabel = QtGui.QLabel(LandXmlDialog)
        self.uXmlFileLabel.setEnabled(True)
        self.uXmlFileLabel.setObjectName(_fromUtf8("uXmlFileLabel"))
        self.horizontalLayout.addWidget(self.uXmlFileLabel)
        self.uXmlFile = QtGui.QLineEdit(LandXmlDialog)
        self.uXmlFile.setEnabled(False)
        self.uXmlFile.setReadOnly(True)
        self.uXmlFile.setObjectName(_fromUtf8("uXmlFile"))
        self.horizontalLayout.addWidget(self.uXmlFile)
        self.uBrowseXmlFile = QtGui.QPushButton(LandXmlDialog)
        self.uBrowseXmlFile.setObjectName(_fromUtf8("uBrowseXmlFile"))
        self.horizontalLayout.addWidget(self.uBrowseXmlFile)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(LandXmlDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.uImportMarks = QtGui.QCheckBox(LandXmlDialog)
        self.uImportMarks.setChecked(True)
        self.uImportMarks.setObjectName(_fromUtf8("uImportMarks"))
        self.horizontalLayout_2.addWidget(self.uImportMarks)
        self.uImportParcels = QtGui.QCheckBox(LandXmlDialog)
        self.uImportParcels.setChecked(True)
        self.uImportParcels.setObjectName(_fromUtf8("uImportParcels"))
        self.horizontalLayout_2.addWidget(self.uImportParcels)
        self.uImportObs = QtGui.QCheckBox(LandXmlDialog)
        self.uImportObs.setEnabled(True)
        self.uImportObs.setChecked(False)
        self.uImportObs.setObjectName(_fromUtf8("uImportObs"))
        self.horizontalLayout_2.addWidget(self.uImportObs)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.uButtonBox = QtGui.QDialogButtonBox(LandXmlDialog)
        self.uButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.uButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.uButtonBox.setObjectName(_fromUtf8("uButtonBox"))
        self.verticalLayout.addWidget(self.uButtonBox)
        self.uXmlFileLabel.setBuddy(self.uXmlFile)
        self.label.setBuddy(self.uImportMarks)

        self.retranslateUi(LandXmlDialog)
        QtCore.QObject.connect(self.uButtonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), LandXmlDialog.accept)
        QtCore.QObject.connect(self.uButtonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), LandXmlDialog.close)
        QtCore.QMetaObject.connectSlotsByName(LandXmlDialog)
        LandXmlDialog.setTabOrder(self.uXmlFile, self.uBrowseXmlFile)
        LandXmlDialog.setTabOrder(self.uBrowseXmlFile, self.uImportMarks)
        LandXmlDialog.setTabOrder(self.uImportMarks, self.uImportParcels)
        LandXmlDialog.setTabOrder(self.uImportParcels, self.uImportObs)
        LandXmlDialog.setTabOrder(self.uImportObs, self.uButtonBox)

    def retranslateUi(self, LandXmlDialog):
        LandXmlDialog.setWindowTitle(_translate("LandXmlDialog", "Import LandXml data", None))
        self.uXmlFileLabel.setText(_translate("LandXmlDialog", "LandXml file", None))
        self.uBrowseXmlFile.setText(_translate("LandXmlDialog", "Browse", None))
        self.label.setText(_translate("LandXmlDialog", "Features to import:", None))
        self.uImportMarks.setText(_translate("LandXmlDialog", "Marks", None))
        self.uImportParcels.setText(_translate("LandXmlDialog", "Parcels", None))
        self.uImportObs.setText(_translate("LandXmlDialog", "Observations", None))

