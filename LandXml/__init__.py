#!/usr/bin/env python
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

from .LandXmlPlugin import LandXmlPlugin


def name():
    return "LandXml import plugin"

def description():
    return "Import parcels and nodes from a LandXml file"

def version():
    return "2.3"

def qgisMinimumVersion():
    return "3.0"

def authorName():
    return "Chris Crook"

def classFactory(iface):
    return LandXmlPlugin(iface)


