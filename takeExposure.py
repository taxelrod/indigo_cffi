#!/usr/bin/env python

import indigo
import time

if __name__ == "__main__":

    # Start up the indigo instanc
    
    indpy = indigo.indigoPy('takeExposure')

    indpy.start()
    
    # sequence of commands

    indpy.sendXml("<getProperties version='2.0'>")
    indpy.sendXml("<newSwitchVector device='Imager Agent' name='FILTER_CCD_LIST'> <oneSwitch name='ZWO ASI1600MM Pro #0'>On</oneSwitch></newSwitchVector>")
#    indpy.sendXml("<newSwitchVector device='Imager Agent' name='CONNECTION'> <oneSwitch name='CONNECTED'>On</oneSwitch></newSwitchVector>")
    indpy.sendXml("<newSwitchVector device='Imager Agent' name='CCD_UPLOAD_MODE'> <oneSwitch name='PREVIEW'>On</oneSwitch></newSwitchVector>")
#    indpy.sendXml("<newTextVector device='Imager Agent' name='CCD_LOCAL_MODE'> <oneText name='DIR'>'/home/taxelrod/tmp'</oneText></newTextVector>")
    indpy.sendXml("<newNumberVector device='Imager Agent' name='CCD_EXPOSURE'> <oneNumber name='EXPOSURE'>1</oneNumber></newNumberVector>")

    # Disconnect server

    time.sleep(5)

    indpy.stop()
