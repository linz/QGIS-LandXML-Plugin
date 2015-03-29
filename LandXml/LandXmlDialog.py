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
from shapely.geometry import MultiPolygon,MultiLineString

from LandXml import LandXml
from Ui_LandXmlDialog import Ui_LandXmlDialog


class LandXmlDialog(QDialog, Ui_LandXmlDialog):

    browsePathSetting="/plugins/LandXml/BrowsePath"

    def __init__(self, iface):
        QDialog.__init__(self)
        self._iface = iface

        settings = QSettings()
        self._home = settings.value(LandXmlDialog.browsePathSetting,'')

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
        filename = unicode(self.uXmlFile.text())
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
            message = unicode(sys.exc_info()[1])
            QMessageBox.information(self,"LandXml error","Problem importing xml\n"+message)
    
    def _createMarkLayer(self,landxml):
        name = "LandXml_marks"
        uri="Point?"+"&".join(['field='+x for x in (
            'mrk_id:int',
            'name:string',
            'description:string',
            'type:string',
            'beacon:string',
            'protection:string',
            'state:string',
            'condition:string',
            'crd_order:string')])
        epsg = landxml.coordSysEpsgId()
        if epsg:
            uri += '&crs=epsg:'+unicode(epsg)
        vl = QgsVectorLayer(uri,name,"memory")
        # Need to do something about crs()
        vl.startEditing()
        fields=vl.pendingFields()
        pr=vl.dataProvider()
        for mark in landxml.monuments():
            (x,y) = mark.point().coords()
            fet = QgsFeature(fields)
            fet.setGeometry(QgsGeometry.fromPoint(QgsPoint(x,y)))
            fet['mrk_id']=mark.lolid()
            fet['name']=mark.name()
            fet['description']=mark.description()
            fet['type']=mark.type()
            fet['beacon']=mark.beacon()
            fet['protection']=mark.protection()
            fet['state']=mark.state()
            fet['condition']=mark.condition()
            fet['crd_order']=mark.point().order()
            pr.addFeatures([fet])
        vl.updateExtents()
        vl.commitChanges()
        QgsMapLayerRegistry.instance().addMapLayer(vl)

    def _createParcelLayer(self, landxml):
        parcel_layers={
            'MultiPolygon':{'name':'LandXml_parcels','layer':None,'geomfunc':MultiPolygon},
            'MultiLineString':{'name':'LandXml_linear_parcels','layer':None,'geomfunc':MultiLineString},
            }

        uri='&'.join(['field='+x for x in (
            'lolid:int',
            'name:string',
            'description:string',
            'type:string',
            'class:string',
            'state:string',
            'area:double',
            )])
        epsg = landxml.coordSysEpsgId()
        if epsg:
            uri += '&crs=epsg:'+unicode(epsg)

        for parcel in landxml.parcels():
            try:
                gtype=parcel.geomtype()
                if not gtype in parcel_layers:
                    raise RuntimeError("Cannot handle parcel geometry type "+unicode(gtype))
                glayer=parcel_layers[gtype]
                if glayer['layer'] is None:
                    glayer['layer']=QgsVectorLayer(gtype+"?"+uri,glayer['name'],'memory')
                vl=glayer['layer']
                fields=vl.pendingFields()
                pr=vl.dataProvider()
                fet = QgsFeature(fields)
                geomwkt=glayer['geomfunc'](parcel.coords()).to_wkt()
                fet.setGeometry(QgsGeometry.fromWkt(geomwkt))
                fet['lolid']=parcel.lolid()
                fet['name']=parcel.name() 
                fet['description']=parcel.description() 
                fet['type']=parcel.type() 
                fet['class']=parcel.pclass() 
                fet['state']=parcel.state() 
                fet['area']=parcel.area() 
                pr.addFeatures([fet])
            except Exception as e:
                raise RuntimeError("Parcel "+parcel.name()+": "+unicode(e))

        for glayer in parcel_layers.values():
            vl=glayer['layer']
            if vl is not None:
                vl.updateExtents()
                vl.commitChanges()
                QgsMapLayerRegistry.instance().addMapLayer(vl)

