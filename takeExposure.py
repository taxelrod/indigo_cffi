#!/usr/bin/env python

import sys
import time
import socket

from _indigo import ffi, lib
from _indigo.lib import indigo_connect_server
from _indigo.lib import indigo_disconnect_server
from _indigo.lib import indigo_start
from _indigo.lib import indigo_build_client
from _indigo.lib import print_property_string

@ffi.def_extern()
def attach_cb(client):
    print('attach client: ', client)
    return 0

@ffi.def_extern()
def define_property_cb(client, device, property, message):
    prop = property[0]  # dereference pointer
    print('define_property: ', ffi.string(prop.device), ffi.string(prop.name))
    print_property_string(property, message)
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

def sendXml(xml, sock):
    print('------------- Sending: ', xml)
    sock.send(bytes(xml, 'utf-8'))
    time.sleep(3)

if __name__ == "__main__":

    # Start up the needed thread
    
    res = indigo_start()

    print('start...')
    if res != lib.INDIGO_OK:
        print('indigo_start failed', res)
        sys.exit(res)

    # build the client with callbacks connected; change the signature to return result, pass it a client *

    print('build client')
    client = indigo_build_client(b"propTool", lib.attach_cb, lib.define_property_cb, lib.update_property_cb, lib.delete_property_cb, lib.send_message_cb, lib.detach_cb)

    # Connect to the indigo server

    serverp = ffi.new("indigo_server_entry * *")  # Note that the indigo_server_entry is serverp[0][0]

    print('server connect')
    res = indigo_connect_server(b"localhost",b"localhost",7624,serverp)

    if res != lib.INDIGO_OK:
        print('indigo_connect_server failed', res)
        sys.exit(res)

    time.sleep(3)

    # get server socket

    server = serverp[0][0]
    fd=server.socket
    sock = socket.fromfd(fd,socket.AF_INET,socket.SOCK_STREAM)

    # sequence of commands

    sendXml("<getProperties version='2.0'>", sock)
    sendXml("<setSwitchVector device='Imager Agent' name='FILTER_CCD_LIST'> <oneSwitch name='ZWO ASI1600MM Pro #0'>On</oneSwitch></setSwitchVector>", sock)
    sendXml("<setSwitchVector device='Imager Agent' name='CONNECTION'> <oneSwitch name='CONNECTED'>On</oneSwitch></setSwitchVector>", sock)
    sendXml("<setSwitchVector device='Imager Agent' name='CCD_UPLOAD_MODE'> <oneSwitch name='PREVIEW'>On</oneSwitch></setSwitchVector>", sock)
    sendXml("<setTextVector device='Imager Agent' name='CCD_LOCAL_MODE'> <oneText name='DIR'>'/home/taxelrod/tmp'</oneText></setTextVector>", sock)
    sendXml("<setNumberVector device='Imager Agent' name='CCD_EXPOSURE'> <oneNumber name='EXPOSURE'>1</oneNumber></setNumberVector>", sock)

    # Disconnect server

    time.sleep(5)
    res = indigo_disconnect_server(serverp[0])

    if res != lib.INDIGO_OK:
        print('indigo_disconnect_server failed', res)
        sys.exit(res)
