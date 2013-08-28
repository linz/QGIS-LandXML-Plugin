# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Documents and Settings\ccrook\.qgis\python\plugins\LandXml\Ui_LandXmlDialog.ui'
#
# Created: Wed Mar 10 09:56:15 2010
#      by: PyQt4 UI code generator 4.5.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_LandXmlDialog(object):
    def setupUi(self, LandXmlDialog):
        LandXmlDialog.setObjectName("LandXmlDialog")
        LandXmlDialog.setWindowModality(QtCore.Qt.NonModal)
        LandXmlDialog.resize(476, 130)
        LandXmlDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtGui.QVBoxLayout(LandXmlDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.uXmlFileLabel = QtGui.QLabel(LandXmlDialog)
        self.uXmlFileLabel.setEnabled(True)
        self.uXmlFileLabel.setObjectName("uXmlFileLabel")
        self.horizontalLayout.addWidget(self.uXmlFileLabel)
        self.uXmlFile = QtGui.QLineEdit(LandXmlDialog)
        self.uXmlFile.setEnabled(False)
        self.uXmlFile.setReadOnly(True)
        self.uXmlFile.setObjectName("uXmlFile")
        self.horizontalLayout.addWidget(self.uXmlFile)
        self.uBrowseXmlFile = QtGui.QPushButton(LandXmlDialog)
        self.uBrowseXmlFile.setObjectName("uBrowseXmlFile")
        self.horizontalLayout.addWidget(self.uBrowseXmlFile)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtGui.QLabel(LandXmlDialog)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.uImportMarks = QtGui.QCheckBox(LandXmlDialog)
        self.uImportMarks.setChecked(True)
        self.uImportMarks.setObjectName("uImportMarks")
        self.horizontalLayout_2.addWidget(self.uImportMarks)
        self.uImportParcels = QtGui.QCheckBox(LandXmlDialog)
        self.uImportParcels.setChecked(True)
        self.uImportParcels.setObjectName("uImportParcels")
        self.horizontalLayout_2.addWidget(self.uImportParcels)
        self.uImportObs = QtGui.QCheckBox(LandXmlDialog)
        self.uImportObs.setEnabled(False)
        self.uImportObs.setChecked(False)
        self.uImportObs.setObjectName("uImportObs")
        self.horizontalLayout_2.addWidget(self.uImportObs)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.uButtonBox = QtGui.QDialogButtonBox(LandXmlDialog)
        self.uButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.uButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.uButtonBox.setObjectName("uButtonBox")
        self.verticalLayout.addWidget(self.uButtonBox)
        self.uXmlFileLabel.setBuddy(self.uXmlFile)
        self.label.setBuddy(self.uImportMarks)

        self.retranslateUi(LandXmlDialog)
        QtCore.QObject.connect(self.uButtonBox, QtCore.SIGNAL("accepted()"), LandXmlDialog.accept)
        QtCore.QObject.connect(self.uButtonBox, QtCore.SIGNAL("rejected()"), LandXmlDialog.close)
        QtCore.QMetaObject.connectSlotsByName(LandXmlDialog)
        LandXmlDialog.setTabOrder(self.uXmlFile, self.uBrowseXmlFile)
        LandXmlDialog.setTabOrder(self.uBrowseXmlFile, self.uImportMarks)
        LandXmlDialog.setTabOrder(self.uImportMarks, self.uImportParcels)
        LandXmlDialog.setTabOrder(self.uImportParcels, self.uImportObs)
        LandXmlDialog.setTabOrder(self.uImportObs, self.uButtonBox)

    def retranslateUi(self, LandXmlDialog):
        LandXmlDialog.setWindowTitle(QtGui.QApplication.translate("LandXmlDialog", "Import LandXml data", None, QtGui.QApplication.UnicodeUTF8))
        self.uXmlFileLabel.setText(QtGui.QApplication.translate("LandXmlDialog", "LandXml file", None, QtGui.QApplication.UnicodeUTF8))
        self.uBrowseXmlFile.setText(QtGui.QApplication.translate("LandXmlDialog", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("LandXmlDialog", "Features to import:", None, QtGui.QApplication.UnicodeUTF8))
        self.uImportMarks.setText(QtGui.QApplication.translate("LandXmlDialog", "Marks", None, QtGui.QApplication.UnicodeUTF8))
        self.uImportParcels.setText(QtGui.QApplication.translate("LandXmlDialog", "Parcels", None, QtGui.QApplication.UnicodeUTF8))
        self.uImportObs.setText(QtGui.QApplication.translate("LandXmlDialog", "Observations", None, QtGui.QApplication.UnicodeUTF8))

