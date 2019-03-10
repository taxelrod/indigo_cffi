# This file is part of indigo_cffi.
#
# Developed for the LSST Telescope and Site Systems.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Classes to deal with indigo properties
"""

import _indigo
from _indigo import ffi, lib

import logging

class textItem:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self):
        return(f"textItem {self.name} = {self.value}")

class numberItem:
    def __init__(self, name, format, min, max, step, value, target):
        self.name = name
        self.format = format
        self.min = min
        self.max = max
        self.step = step
        self.value = value
        self.target = target
    def __repr__(self):
        return(f"numberItem {self.name} = {self.value} (min, max, step, target) = ({self.min}, {self.max}, {self.step}. {self.target})")

class switchItem:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self):
        return(f"switchItem {self.name} = {self.value}")

class lightItem:                      # this is light as in indicator light
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self):
        return(f"lightItem {self.name} = {self.value}")

class blobItem:
    def __init__(self, name, format, url, size, value):
        self.name = name
        self.format = format
        self.url = url
        self.size = size
        self.value = value
    def __repr__(self):
        return(f"blobItem {self.name} {self.format} {self.url} {self.size}")

def buildPropDictItem(propPtr):

    property = propPtr[0]
    devName = ffi.string(property.device)
    devPropName = ffi.string(property.name)
    propCount = property.count
    propItems = property.items
    propType = property.type
    propPerm = property.perm
    propState = property.state

    dictKey = f"{devName}.{devPropName}"

    propItemList = []

    for i in range(propCount):
        item = propItems[i]
        if propType == lib.INDIGO_TEXT_VECTOR:
            propItemList.append(textItem(ffi.string(item.name), ffi.string(item.text.value)))
        elif propType == lib.INDIGO_NUMBER_VECTOR:
            propItemList.append(numberItem(ffi.string(item.name), ffi.string(item.number.format), item.number.min, item.number.max, item.number.step, item.number.value, item.number.target))
        elif propType == lib.INDIGO_SWITCH_VECTOR:
            propItemList.append(switchItem(ffi.string(item.name), item.sw.value))
        elif propType == lib.INDIGO_LIGHT_VECTOR:
            propItemList.append(lightItem(ffi.string(item.name), item.light.value))
        elif propType == lib.INDIGO_BLOB_VECTOR:
            propItemList.append(blobItem(ffi.string(item.name), ffi.string(item.blob.format), ffi.string(item.blob.url), item.blob.size, item.blob.value))
        else:
            raise RuntimeError(f"Illegal property type {propType} for {dictkey}")
        

    dictValue = [propType, propCount, propPerm, propState, propItemList]

    return (dictKey, dictValue)
    
def printPropDictEntry(pdKey, pdEntry, logLevel=logging.INFO):
    propType = pdEntry[0]
    propCount = pdEntry[1]
    propPerm = pdEntry[2]
    propState = pdEntry[3]
    propItemList = pdEntry[4]

    logging.log(logLevel, "%s", pdKey)
    for i in range(propCount):
        item = propItemList[i]
        logging.log(logLevel, "\t%s", repr(item))
        
    
