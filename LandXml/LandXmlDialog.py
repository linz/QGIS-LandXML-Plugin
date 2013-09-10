# -*- coding: utf-8 -*-
#
################################################################################
#
# Copyright 2013 Crown copyright (c)
# Land Information New Zealand and the New Zealand Government.
# All rights reserved
#
# This program is released under the terms of the new BSD license. See the 
# LICENSE file for more information.
#
################################################################################


from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import sys
import os.path
import string
import math
from shapely.geometry import MultiPolygon

from LandXml import LandXml
from Ui_LandXmlDialog import Ui_LandXmlDialog


class LandXmlDialog(QDialog, Ui_LandXmlDialog):

    browsePathSetting="/plugins/LandXml/BrowsePath"

    def __init__(self, iface):
        QDialog.__init__(self)
        self._iface = iface

        settings = QSettings()
        self._home = settings.value(LandXmlDialog.browsePathSetting).toString()

        # Set up the user interface from Designer.
        self.setupUi(self)
        #Signals
        QObject.connect(self.uBrowseXmlFile, SIGNAL("clicked()"), self._browseXmlFile)
        QObject.connect(self.uButtonBox, SIGNAL("accepted()"), self._accept)

    def _browseXmlFile(self):
        filename = QFileDialog.getOpenFileName(self,"Select LandXml file",
            self._home, "LandXml files (*.xml);;All files (*.*)")
        if filename:
            self.uXmlFile.setText(filename)


    def _accept(self):
        filename = str(self.uXmlFile.text())
        homedir = os.path.dirname(filename)
        settings = QSettings()
        settings.setValue(LandXmlDialog.browsePathSetting,homedir)
        if not filename:
            QMessageBox.information(self,"LandXml error","You must specify a LandXml file to import")
            return
        if not os.path.exists(filename):
            QMessageBox.information(self,"LandXml error","Cannot open " + filename)
            return

        try:
            data = LandXml(filename)
            if self.uImportParcels.isChecked():
                self._createParcelLayer(data)
            if self.uImportMarks.isChecked():
                self._createMarkLayer(data)
            if self.uImportObs.isChecked():
                self._createObsLayer(data)
        except:
            # raise
            message = str(sys.exc_info()[1])
            QMessageBox.information(self,"LandXml error","Problem importing xml\n"+message)


    def _createMarkLayer(self,landxml):
        name = "LandXml_marks"
        vl = QgsVectorLayer("Point",name,"memory")
        # Need to do something about crs()
        pr = vl.dataProvider()
        pr.addAttributes( [
            QgsField("mrk_id", QVariant.Int, "Int"),
            QgsField("name",QVariant.String,"String"),
            QgsField("description",QVariant.String,"String"),
            QgsField("type",QVariant.String,"String"),
            QgsField("beacon",QVariant.String,"String"),
            QgsField("protection",QVariant.String,"String"),
            QgsField("state",QVariant.String,"String"),
            QgsField("condition",QVariant.String,"String"),
            QgsField("crd_order",QVariant.String,"String")
            ])
        for mark in landxml.monuments():
            (x,y) = mark.point().coords()

            fet = QgsFeature()
            fet.setGeometry(QgsGeometry.fromPoint(QgsPoint(x,y)))
            fet.setAttributeMap( { 
                0 : QVariant(mark.lolid()),
                1 : QVariant(mark.name()),
                2 : QVariant(mark.description()),
                3 : QVariant(mark.type()),
                4 : QVariant(mark.beacon()),
                5 : QVariant(mark.protection()),
                6 : QVariant(mark.state()),
                7 : QVariant(mark.condition()),
                8 : QVariant(mark.point().order())
                } )
            pr.addFeatures( [ fet ] )

        vl.updateFieldMap()
        vl.updateExtents()
        vl.commitChanges()
        QgsMapLayerRegistry.instance().addMapLayer(vl)

    def _createParcelLayer(self, landxml):
        name = "LandXml_parcels"
        vl = QgsVectorLayer("MultiPolygon",name,"memory")
        pr = vl.dataProvider()
        pr.addAttributes( [
            QgsField("lolid", QVariant.Int, "Int"),
            QgsField("name",QVariant.String,"String"),
            QgsField("description",QVariant.String,"String"),
            QgsField("type",QVariant.String,"String"),
            QgsField("class", QVariant.String, "String"),
            QgsField("state",QVariant.String,"String"),
            QgsField("area", QVariant.Double, "Double"),
            ] )
        for parcel in landxml.parcels():
            fet = QgsFeature()
            fet.setGeometry(QgsGeometry.fromWkt(QString(MultiPolygon(parcel.coords()).to_wkt())))
            fet.setAttributeMap( { 
                0 : QVariant(parcel.lolid()), 
                1 : QVariant(parcel.name()), 
                2 : QVariant(parcel.description()), 
                3 : QVariant(parcel.type()), 
                4 : QVariant(parcel.pclass()), 
                5 : QVariant(parcel.state()), 
                6 : QVariant(parcel.area()), 
                } )
            pr.addFeatures( [ fet ] )
        vl.updateFieldMap()
        vl.updateExtents()
        vl.commitChanges()
        QgsMapLayerRegistry.instance().addMapLayer(vl)

