"""
Classes to deal with indigo properties
"""

import _indigo
from _indigo import ffi, lib

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

class blobItem:
    def __init__(self, name, format, url, size, value):
        self.name = name
        self.format = format
        self.url = url
        self.size = size
        self.value = value

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
            propItemList.append(numberItem(textItem(ffi.string(item.name), ffi.string(item.number.format), item.number.min, item.number.max, item.number.step, item.number.value, item.number.target)))
        elif propType == lib.INDIGO_SWITCH_VECTOR:
            propItemList.append(switchItem(ffi.string(item.name), item.sw.value))
        elif propType == lib.INDIGO_LIGHT_VECTOR:
            propItemList.append(lightItem(ffi.string(item.name))) # XXX
        elif propType == lib.INDIGO_BLOB_VECTOR:
            propItemList.append(blobItem(ffi.string(item.name))) # XXX
        else:
            raise RuntimeError(f"Illegal property type {propType} for {dictkey}")
        

    dictValue = [propType, propCount, propPerm, propState, propItemList]

    return (dictKey, dictValue)
    
def printPropDictEntry(pdKey, pdEntry):
    propType = pdEntry[0]
    propCount = pdEntry[1]
    propPerm = pdEntry[2]
    propState = pdEntry[3]
    propItemList = pdEntry[4]

    print(pdKey)
    for i in range(propCount):
        item = propItemList[i]
        print("\t", repr(item))
        
    
