from _indigo import ffi, lib
from _indigo.lib import indigo_build_client

@ffi.def_extern()
def attach_cb(client):
    print('client: ', client)
    return 0

def doit(name):
    client = indigo_build_client(name, lib.attach_cb)
    return client
