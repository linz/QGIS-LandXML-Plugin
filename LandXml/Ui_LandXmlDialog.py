# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_LandXmlDialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LandXmlDialog(object):
    def setupUi(self, LandXmlDialog):
        LandXmlDialog.setObjectName("LandXmlDialog")
        LandXmlDialog.setWindowModality(QtCore.Qt.NonModal)
        LandXmlDialog.resize(476, 130)
        LandXmlDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(LandXmlDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.uXmlFileLabel = QtWidgets.QLabel(LandXmlDialog)
        self.uXmlFileLabel.setEnabled(True)
        self.uXmlFileLabel.setObjectName("uXmlFileLabel")
        self.horizontalLayout.addWidget(self.uXmlFileLabel)
        self.uXmlFile = QtWidgets.QLineEdit(LandXmlDialog)
        self.uXmlFile.setEnabled(False)
        self.uXmlFile.setReadOnly(True)
        self.uXmlFile.setObjectName("uXmlFile")
        self.horizontalLayout.addWidget(self.uXmlFile)
        self.uBrowseXmlFile = QtWidgets.QPushButton(LandXmlDialog)
        self.uBrowseXmlFile.setObjectName("uBrowseXmlFile")
        self.horizontalLayout.addWidget(self.uBrowseXmlFile)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(LandXmlDialog)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.uImportMarks = QtWidgets.QCheckBox(LandXmlDialog)
        self.uImportMarks.setChecked(True)
        self.uImportMarks.setObjectName("uImportMarks")
        self.horizontalLayout_2.addWidget(self.uImportMarks)
        self.uImportParcels = QtWidgets.QCheckBox(LandXmlDialog)
        self.uImportParcels.setChecked(True)
        self.uImportParcels.setObjectName("uImportParcels")
        self.horizontalLayout_2.addWidget(self.uImportParcels)
        self.uImportObs = QtWidgets.QCheckBox(LandXmlDialog)
        self.uImportObs.setEnabled(True)
        self.uImportObs.setChecked(False)
        self.uImportObs.setObjectName("uImportObs")
        self.horizontalLayout_2.addWidget(self.uImportObs)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.uButtonBox = QtWidgets.QDialogButtonBox(LandXmlDialog)
        self.uButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.uButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.uButtonBox.setObjectName("uButtonBox")
        self.verticalLayout.addWidget(self.uButtonBox)
        self.uXmlFileLabel.setBuddy(self.uXmlFile)
        self.label.setBuddy(self.uImportMarks)

        self.retranslateUi(LandXmlDialog)
        self.uButtonBox.accepted.connect(LandXmlDialog.accept)
        self.uButtonBox.rejected.connect(LandXmlDialog.close)
        QtCore.QMetaObject.connectSlotsByName(LandXmlDialog)
        LandXmlDialog.setTabOrder(self.uXmlFile, self.uBrowseXmlFile)
        LandXmlDialog.setTabOrder(self.uBrowseXmlFile, self.uImportMarks)
        LandXmlDialog.setTabOrder(self.uImportMarks, self.uImportParcels)
        LandXmlDialog.setTabOrder(self.uImportParcels, self.uImportObs)
        LandXmlDialog.setTabOrder(self.uImportObs, self.uButtonBox)

    def retranslateUi(self, LandXmlDialog):
        _translate = QtCore.QCoreApplication.translate
        LandXmlDialog.setWindowTitle(_translate("LandXmlDialog", "Import LandXml data"))
        self.uXmlFileLabel.setText(_translate("LandXmlDialog", "LandXml file"))
        self.uBrowseXmlFile.setText(_translate("LandXmlDialog", "Browse"))
        self.label.setText(_translate("LandXmlDialog", "Features to import:"))
        self.uImportMarks.setText(_translate("LandXmlDialog", "Marks"))
        self.uImportParcels.setText(_translate("LandXmlDialog", "Parcels"))
        self.uImportObs.setText(_translate("LandXmlDialog", "Observations"))

