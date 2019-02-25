"""
Python classes to interface to indigo.

Because of the way callbacks are defined inside the indigo C, the callbacks cannot be passed an indigoPy class pointer,
so indigoPy is implemented as a singleton, with activeIndigoPy being the active instance.
"""
import sys
import time
import socket

from _indigo import ffi, lib
from _indigo.lib import indigo_connect_server
from _indigo.lib import indigo_disconnect_server
from _indigo.lib import indigo_start
from _indigo.lib import indigo_build_client

activeIndigoPy = None

# Module data

class indigoPy:

    indigoProperties = {}
    indigoHost = None
    indigoPort = None
    indigoDeviceName = None
    indigoClientPtr = None
    indigoSocket = None

    serverDelay = 1

    indigoServerPtr = None
    indigoServer = None
    
    def __init__(self, deviceName, serverHost=None, serverPort=None):
        self.indigoDeviceName = deviceName
        if serverHost is not None:
            self.indigoHost = serverHost
        else:
            self.indigoHost = "localhost"

        if serverPort is not None:
            self.indigoPort = serverPort
        else:
            self.indigoPort = 7624

    def start(self):
        global activeIndigoPy

        if activeIndigoPy is not None:
            raise RuntimeError(f"An indigoPy instance is already active ")
            
        activeIndigoPy = self
        
        result = indigo_start()
        if result != lib.INDIGO_OK:
            raise RuntimeError(f"indigo start failed with error {result}")

        # build the client with callbacks connected

        self.indigoClientPtr = indigo_build_client(b"indigoPy", lib.attach_cb, lib.define_property_cb, lib.update_property_cb, lib.delete_property_cb, lib.send_message_cb, lib.detach_cb)
        
        # Connect to the indigo server

        self.indigoServerPtr = ffi.new("indigo_server_entry * *")  # Note that the indigo_server_entry is serverPtr[0][0]

        result = indigo_connect_server(b"localhost",b"localhost",7624,self.indigoServerPtr)

        if result != lib.INDIGO_OK:
            raise RuntimeError(f"indigo_connect_server failed with error {result}")

        time.sleep(self.serverDelay)

        # get server socket

        self.indigoServer = self.indigoServerPtr[0][0]
        fd=self.indigoServer.socket
        self.indigoSocket = socket.fromfd(fd,socket.AF_INET,socket.SOCK_STREAM)


    def stop(self):
        global activeIndigoPy

        result = indigo_disconnect_server(self.indigoServerPtr[0])
        if result != lib.INDIGO_OK:
            raise RuntimeError(f"indigo_disconnect_server failed with error {result}")

        activeIndigoPy = None
        
    def sendXml(self, xmlString):
        print('------------- Sending: ', xmlString)
        self.indigoSocket.send(bytes(xmlString, 'utf-8'))
        time.sleep(self.serverDelay)

    def define_property(self, propPtr):
        property = propPtr[0]
        devName = ffi.string(property.device)
        devPropName = ffi.string(property.name)
        propCount = property.count
        propItems = property.items
        
        try:
            deviceDict =  self.indigoProperties[devName]
        except KeyError:
            self.indigoProperties[devName] = {}
            deviceDict =  self.indigoProperties[devName]

        try:
            itemDict = self.indigoProperties[devName][devPropName]
        except KeyError:
            self.indigoProperties[devName][devPropName] = {}

        for i in range(propCount):
            item = propItems[i]
            self.indigoProperties[devName][devPropName][item.name] = 'hmmm'

            
    def printProperties(self):
        for dev in self.indigoProperties.keys():
            print('Properties for ', dev)
            for name in self.indigoProperties[dev].keys():
                print('\tProperty name ', name)
                for item in self.indigoProperties[dev][name].keys():
                    print('\t\tItem: ', ffi.string(item))
            
        

# Callbacks

# Callbacks can access members of the (only) active indigoPy through activeIndigoPy

@ffi.def_extern()
def attach_cb(client):
    print('attach client: ', client, activeIndigoPy.indigoDeviceName)
    return 0
            
@ffi.def_extern()
def define_property_cb(client, device, propPtr, message):
    activeIndigoPy.define_property(propPtr)
    prop = propPtr[0]
    print('define_property: ', ffi.string(prop.device), ffi.string(prop.name))
#    print_property_string(property, message)
#    dev = device[0]  # this is now a device struct
#    print('device: ', ffi.string(dev.name), dev.version, dev.attach, dev.enumerate_properties)
    return 0

@ffi.def_extern()
def update_property_cb(client, device, property, message):
    print('update_property: ', client, device, property, message)
    return 0

@ffi.def_extern()
def delete_property_cb(client, device, property, message):
    print('delete_property: ', client, device, property, message)
    return 0

@ffi.def_extern()
def send_message_cb(client, device, message):
    print('send_message: ', client, device, message)
    return 0

@ffi.def_extern()
def detach_cb(client):
    print('detach client: ', client)
    return 0

