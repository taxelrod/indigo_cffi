#!/usr/bin/env python
from _indigo import ffi, lib
from _indigo.lib import indigo_connect_server
from _indigo.lib import indigo_disconnect_server
from _indigo.lib import indigo_start
from _indigo.lib import indigo_build_client

@ffi.def_extern()
def attach_cb(client):
    print('attach client: ', client)
    return 0

@ffi.def_extern()
def define_property_cb(client, device, property, message):
    prop = property[0]  # dereference pointer
    print('define_property: ', ffi.string(prop.device), ffi.string(prop.name))
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

    # build the client with callbacks connected
    
    client = indigo_build_client(b"propTool", lib.attach_cb, lib.define_property_cb, lib.update_property_cb, lib.delete_property_cb, lib.send_message_cb, lib.detach_cb)

    # Connect to the indigo server

    serverp = ffi.new("indigo_server_entry * *")  # Note that the indigo_server_entry is serverp[0][0]
    indigo_connect_server(b"localhost",b"localhost",7624,serverp)

    # Process args

    # Disconnect server

    indigo_disconnect_server(serverp[0])
