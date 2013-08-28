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

import re
import xml.etree.ElementTree as et

class LandXmlException( Exception ):

    def __init_(self,value):
        self._value = value

    def str(self):
        return self._value

class Point (object):

    def __init__(self,coords,id='',order='',type=''):
        self._coords = coords
        self._id = id
        self._order = order
        self._type = type

    def coords(self):
        return self._coords

    def id(self):
        return self._id

    def order(self):
        return self._order

    def type(self):
        return self._type


class Monument (object):

    def __init__(self,point,
        name='',
        lolid='',
        description='',
        type='',
        beacon='',
        protection='',
        state='',
        condition=''):
            self._point = point
            self._name = name
            self._lolid = lolid
            self._description = description
            self._type = type
            self._beacon = beacon
            self._protection = protection
            self._state = state
            self._condition = condition

    def point(self):
        return self._point

    def name(self):
        return self._name

    def lolid(self):
        return self._lolid

    def description(self):
        return self._description

    def type(self):
        return self._type

    def state(self):
        return self._state

    def condition(self):
        return self._condition

    def beacon(self):
        return self._beacon

    def protection(self):
        return self._protection

class Parcel:

    def __init__(self,
            coords,
            name,
            lolid='',
            description='',
            area=0.0,
            state='',
            pclass='',
            type=''):
        self._coords=coords
        self._name=name
        self._lolid=lolid
        self._description = description
        self._area = area
        self._state = state
        self._pclass = pclass
        self._type=type

    def coords(self):
        return self._coords

    def name(self):
        return self._name

    def lolid(self):
        return self._lolid

    def description(self):
        return self._description

    def type(self):
        return self._type

    def state(self):
        return self._state

    def area(self):
        return self._area

    def pclass(self):
        return self._pclass

class LandXml (object):

    def __init__(self,file):
        data = et.ElementTree()
        data.parse(file)
        root = data.find(".")
        ns = root.tag.split("}")[0]+"}"
        self._data = data
        self._root = root
        self._ns = ns
        self._parcels=[]
        self._points=[]
        self._pointIdx={}
        self._surveys=[]
        self._parse()

    def _parse(self):
        self._readPoints()
        # self._readMarks()
        # self._readParcels()
        self._readSurveys()

    def monuments(self):
        for m in self._readMarks():
            yield m

    def parcels(self):
        for p in self._readParcels():
            yield p

    def surveys(self):
        return self._surveys

    def _readPoints(self):
        ns = self._ns;
        points=self._data.findall("%sCgPoints/%sCgPoint"%(ns,ns))
        for p in points:
            oID = p.get('oID')
            order = p.get('surveyOrder','')
            id = p.get('name','')
            pntType = p.get('pntSurv','')
            coords = self._getCoords(p.text)
            point = Point(coords,id=id,order=order,type=pntType)
            self._points.append(point)
            self._pointIdx[oID] = point

    def _readMarks(self):
        ns = self._ns;
        monuments=self._data.findall("%sMonuments/%sMonument"%(ns,ns))
        for m in monuments:
            oID = m.get('oID')
            name,lolid = self._parseLolId(m.get('name'))
            desc = m.get('desc','')
            type = m.get('type','')
            state = m.get('state','')
            condition = m.get('condition','')
            beacon = m.get('beacon','')
            protection = m.get('beaconProtection','')
            pntref = m.get('pntRef')
            point = self._pointIdx[pntref]
            monument=Monument(point,name=name,lolid=lolid,description=desc,type=type,state=state,condition=condition,beacon=beacon,protection=protection)
            yield monument

    def _readParcels(self):
        ns = self._ns;
        parcels=self._data.findall("%sParcels/%sParcel"%(ns,ns))
        for p in parcels:
            cogo = p.find(ns+"CoordGeom");
            if not cogo:
                continue
            oID = p.get('oID')
            name,lolid = self._parseLolId(p.get('name'))
            desc = p.get('desc','')
            area = 0.0
            try:
                area = float(p.get('area','0.0'))
            except:
                pass
            state = p.get('state','')
            pclass = p.get('class','')
            type = p.get('parcelType','')
            coords = self._readCoGo(cogo)
            parcel = Parcel(coords,name,lolid=lolid,description=desc,area=area,
                state=state,pclass=pclass,type=type)
            yield parcel
            #self._parcels.append(parcel)

    def _readSurveys(self):
        pass

    def _parseLolId(self,name):
        lolid = 0
        match = re.search(r'\s+\[(\d+)\]\s*$',name)
        if match:
            lolid = int(match.group(1))
            name = name[:match.start()]
        return name,lolid

    def _getTag(self,element):
        return element.tag.replace(self._ns,'')

    def _readCoGo(self,cogo):
        ''' Read a CoordGeom element to build a multipolygon coord array.
        Assumes that:
            rings are identifiable by difference between endpoint of one segment
            and startpoint of the next
            segments of rings are in order
            inner rings immediately follow their outer ring
            inner rings coordinates are in opposite direction (clockwise/anticlockwise)
            to outer ring coordinates
        '''
        crdlist = []
        coords = None
        for c in cogo.getchildren():
            tag = self._getTag(c)
            line = None
            if tag == "Line":
                line = self._readLine(c)
            elif tag == "IrregularLine":
                line = self._readIrregularLine(c)
            elif tag == "Curve":
                line = self._readCurve(c)
            else:
                raise LandXmlException("CoordGeom " + tag + " type not handled")

            if line:
                if  coords==None or line[0] != coords[-1]:
                    coords=line
                    crdlist.append(coords)
                else:
                    coords.extend(line[1:])

        polylist = []
        inner = None
        mult = 1.0
        for c in crdlist:
            area = self._calcArea(c)
            if inner == None:
                mult = area
            area *= mult
            if area >= 0.0:
                inner = []
                polylist.append([c,inner])
            else:
                inner.append(c)
        return polylist

    def _getCoords(self,text):
        crds = text.split()
        return [float(crds[1]),float(crds[0])]

    def _readLine(self,c):
        return [self._readPointType(c,'Start'),self._readPointType(c,'End')]

    def _readPointType(self,c,tag):
        ns = self._ns
        pntref = c.find(ns+tag)
        if pntref == None:
            ctag = self._getTag(c)
            raise LandXmlException(tag + ' element missing in '+ctag)
        crds = []
        if pntref.text:
            crds = self._getCoords(pntref.text)
        else:
            ref = pntref.get("pntRef")
            crds = self._pointIdx[ref].coords()
        return crds

    def _readIrregularLine(self,c):
        crds = []
        pts = c.find(self._ns + 'PntList2D')
        dim = 2
        if pts == None:
            pts = c.find(self._ns+'PntList3D')
            dim = 3
        icrds = pts.text.split()
        for i in range(0,len(icrds),dim):
            crds.append([float(icrds[i+1]),float(icrds[i])])

        p0 = self._readPointType(c,'Start')
        if p0 != crds[0]:
            crds.insert(0,p0)

        p1 = self._readPointType(c,'End')
        if p1 != crds[-1]:
            crds.append(p1)
        return crds

    def _readCurve(self,c):
        ''' Haven't handled Curve elements - just return start and endpoints '''
        return self._readLine(c)

    def _calcArea(self,c):
        if len(c) < 3:
            return 0.0
        area = 0.0
        x = c[0][0]
        y = c[0][1]
        dx0 = 0
        dy0 = 0
        for crd in c[1:]:
            dx1 = crd[0]-x
            dy1 = crd[1]-y
            area += dx0*dy1-dx1*dy0
            dx0 = dx1
            dy0 = dy1
        return area

