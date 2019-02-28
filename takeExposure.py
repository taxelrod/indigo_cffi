#!/usr/bin/env python

import indigo
import time

if __name__ == "__main__":

    # Start up the indigo instanc
    
    indpy = indigo.indigoPy('takeExposure')

    indpy.start()

    indpy.printProperties()
    
    # sequence of commands

    indpy.sendXml("<getProperties version='2.0'>")
    time.sleep(5)
    indpy.sendXml("<newSwitchVector device='Imager Agent' name='FILTER_CCD_LIST' state='Ok'> <oneSwitch name='None'>Off</oneSwitch> <oneSwitch name='ZWO ASI1600MM Pro #0'>On</oneSwitch></newSwitchVector>")
    time.sleep(5)
    indpy.sendXml("<newSwitchVector device='ZWO ASI1600MM Pro #0' name='CONNECTION' state='Ok'> <oneSwitch name='DISCONNECTED'>Off</oneSwitch> <oneSwitch name='CONNECTED'>On</oneSwitch></newSwitchVector>")
    time.sleep(5)
    indpy.sendXml("<newSwitchVector device='Imager Agent' name='CCD_UPLOAD_MODE' state='Ok'><oneSwitch name='CLIENT'>Off</oneSwitch><oneSwitch name='LOCAL'>On</oneSwitch><oneSwitch name='BOTH'>Off</oneSwitch><oneSwitch name='PREVIEW'>On</oneSwitch> <oneSwitch name='PREVIEW_LOCAL'>Off</oneSwitch></newSwitchVector>")
#    indpy.sendXml("<newTextVector device='Imager Agent' name='CCD_LOCAL_MODE'> <oneText name='DIR'>'/home/taxelrod/tmp'</oneText></newTextVector>")
    time.sleep(5)
    indpy.sendXml("<newNumberVector device='Imager Agent' name='CCD_EXPOSURE'> <oneNumber name='EXPOSURE'>1</oneNumber></newNumberVector>")

    # Disconnect server

    time.sleep(5)

    indpy.stop()
