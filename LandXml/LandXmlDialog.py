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


from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from qgis.core import *

import sys
import os.path
import string
import math
from shapely.geometry import MultiPolygon,MultiLineString
import shapely.wkt

from .LandXml import LandXml
from .Ui_LandXmlDialog import Ui_LandXmlDialog


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
        self.uBrowseXmlFile.clicked.connect(self._browseXmlFile)
        self.uButtonBox.accepted.connect(self._accept)

    def _browseXmlFile(self):
        filename = QFileDialog.getOpenFileName(self,"Select LandXml file",
            self._home, "LandXml files (*.xml);;All files (*.*)")[0]
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
        uri="Point?"+"&".join(['field='+x for x in (
            'mrk_id:int',
            'pnt_id:string',
            'name:string',
            'description:string',
            'type:string',
            'beacon:string',
            'protection:string',
            'state:string',
            'condition:string',
            'crd_order:string',
            'purpose:string')])
        epsg = landxml.coordSysEpsgId()
        if epsg:
            uri += '&crs=epsg:'+str(epsg)
        vl = QgsVectorLayer(uri,name,"memory")
        # Need to do something about crs()
        vl.startEditing()
        fields=vl.fields()
        pr=vl.dataProvider()
        for mark in landxml.monuments():
            (x,y) = mark.point().coords()
            fet = QgsFeature(fields)
            fet.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(x,y)))
            fet['mrk_id']=mark.lolid()
            fet['pnt_id']=mark.point().id()
            fet['name']=mark.name()
            fet['description']=mark.description()
            fet['type']=mark.type()
            fet['beacon']=mark.beacon()
            fet['protection']=mark.protection()
            fet['state']=mark.state()
            fet['condition']=mark.condition()
            fet['crd_order']=mark.point().order()
            fet['purpose']=mark.purpose()
            pr.addFeatures([fet])
        vl.updateExtents()
        vl.commitChanges()
        QgsProject.instance().addMapLayer(vl)

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
            uri += '&crs=epsg:'+str(epsg)

        for parcel in landxml.parcels():
            try:
                gtype=parcel.geomtype()
                if not gtype in parcel_layers:
                    raise RuntimeError("Cannot handle parcel geometry type "+str(gtype))
                glayer=parcel_layers[gtype]
                if glayer['layer'] is None:
                    glayer['layer']=QgsVectorLayer(gtype+"?"+uri,glayer['name'],'memory')
                vl=glayer['layer']
                fields=vl.fields()
                pr=vl.dataProvider()
                fet = QgsFeature(fields)
                geomwkt=shapely.wkt.dumps(glayer['geomfunc'](parcel.coords()))
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
                raise RuntimeError("Parcel "+parcel.name()+": "+str(e))

        for glayer in list(parcel_layers.values()):
            vl=glayer['layer']
            if vl is not None:
                vl.updateExtents()
                vl.commitChanges()
                QgsProject.instance().addMapLayer(vl)
    
    def _createObsLayer(self,landxml):
        name = "LandXml_observations"
        uri="LineString?"+"&".join(['field='+x for x in (
            'from:string',
            'to:string',
            'distance:double',
            'disttype:string',
            'distclass:string',
            'distsurvey:string',
            'azimuth:string',
            'azdegrees:double',
            'arcradius:double',
            'arctype:string',
            'aztype:string',
            'azclass:string',
            'azsurvey:string',
            'equipment:string',
            'date:string',
            )])
        epsg = landxml.coordSysEpsgId()
        if epsg:
            uri += '&crs=epsg:'+str(epsg)
        vl = QgsVectorLayer(uri,name,"memory")
        # Need to do something about crs()
        vl.startEditing()
        fields=vl.fields()
        pr=vl.dataProvider()
        for obs in landxml.observations():
            fet = QgsFeature(fields)
            fet.setGeometry(QgsGeometry.fromPolyline(
                [QgsPoint(x,y) for x,y in obs.coords()]))
            fet['from']=obs.mntfrom()
            fet['to']=obs.mntto()
            fet['distance']=obs.distance()
            fet['disttype']=obs.disttype()
            fet['distclass']=obs.distclass()
            fet['distsurvey']=obs.distsurvey()
            fet['azimuth']=obs.azimuth()
            fet['azdegrees']=obs.azdegrees()
            fet['arcradius']=obs.arcradius()
            fet['arctype']=obs.arctype()
            fet['aztype']=obs.aztype()
            fet['azclass']=obs.azclass()
            fet['azsurvey']=obs.azsurvey()
            fet['equipment']=obs.equipment()
            fet['date']=obs.date()
            pr.addFeatures([fet])
        vl.updateExtents()
        vl.commitChanges()
        QgsProject.instance().addMapLayer(vl)
