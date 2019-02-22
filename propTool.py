#!/usr/bin/env python

import sys
import time
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

    time.sleep(1)
    # Process args

    # Disconnect server

    res = indigo_disconnect_server(serverp[0])

    if res != lib.INDIGO_OK:
        print('indigo_disconnect_server failed', res)
        sys.exit(res)
