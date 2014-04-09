# -*- coding: utf-8 -*-

# Resource object code
#
# Created: Tue Apr 8 21:05:57 2014
#      by: The Resource Compiler for PySide (Qt v4.8.5)
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore

qt_resource_data = "\x00\x00\x01<<?xml version=\x221.0\x22 encoding=\x22UTF-8\x22?>\x0a<svg xmlns=\x22http://www.w3.org/2000/svg\x22 width=\x22497\x22 height=\x22470\x22>\x0a<g stroke=\x22#f00\x22 stroke-width=\x2220\x22 fill=\x22none\x22>\x0a<path d=\x22M140,20C\x0a73,20 20,74 20,140\x0a20,275 156,310 248,443\x0a336,311 477,270 477,140\x0a477,74 423,20 357,20\x0a309,20 267,48 248,89\x0a229,48 188,20 140,20Z\x22/>\x0a</g>\x0a</svg>\x0a"
qt_resource_name = "\x00\x09\x08\x97\x87\xa7\x00h\x00e\x00a\x00r\x00t\x00.\x00s\x00v\x00g"
qt_resource_struct = "\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00"
def qInitResources():
    QtCore.qRegisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
