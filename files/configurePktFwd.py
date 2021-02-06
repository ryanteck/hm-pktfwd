#Configure Packet Forwarder Program
#Configures the packet forwarder based on the YAML File and Env Variables
import os
import subprocess
import json
from pprint import pprint
from shutil import copyfile

from time import sleep
regionID = str(os.environ['REGION'])
#moduleId = 0

print("Sleeping 10 seconds")
sleep(10)

#Region dictionary
regionList = {
    "AS923" : "AS-global_conf.json",
    "AU915" : "AU-global_conf.json",
    "CN470" : "CN-global_conf.json",
    "EU868" : "EU-global_conf.json",
    "IN865" : "IN-global_conf.json",
    "KR920" : "KR-global_conf.json",
    "RU864" : "RU-global_conf.json",
    "US915" : "US-global_conf.json"
}

#Configuration function

def writeRegionConfSx1301(regionId):
    regionconfFile = "/opt/iotloragateway/packet_forwarder/sx1301/lora_templates_sx1301/"+regionList[regionId]
    with open(regionconfFile) as regionconfJFile:
        newGlobal = json.load(regionconfJFile)
    globalPath = "/opt/iotloragateway/packet_forwarder/sx1301/global_conf.json"

    with open(globalPath, 'w') as jsonOut:
        json.dump(newGlobal, jsonOut)

def writeRegionConfSx1302(regionId):
    regionconfFile = "/opt/iotloragateway/packet_forwarder/sx1302/lora_templates_sx1302/"+regionList[regionId]
    globalPath = "/opt/iotloragateway/packet_forwarder/sx1302/packet_forwarder/global_conf.json"

    copyfile(regionconfFile,globalPath)





#If HAT Enabled


with open("/var/pktfwd/diagnostics", 'w') as diagOut:
    diagOut.write("true")
failTimes = 0

#Reset on pin 38
while True:


    euiTest = os.popen('/opt/iotloragateway/packet_forwarder/sx1302/util_chip_id/chip_id -d /dev/spidev1.2').read()


    print("Starting")
    os.system("./reset-38.sh")
    sleep(2)

    if "concentrator EUI:" in euiTest:
        print("SX1302")
        print("Frequency " + regionID)
        writeRegionConfSx1302(regionID)
        os.system("/opt/iotloragateway/packet_forwarder/sx1302/packet_forwarder/lora_pkt_fwd")
        print("Software crashed, restarting")
        failTimes += 1


    else:
        print("SX1301")
        print("Frequency " + regionID)
        writeRegionConfSx1301(regionID)
        os.system("/opt/iotloragateway/packet_forwarder/sx1301/lora_pkt_fwd")
        print("Software crashed, restarting")
        failTimes += 1

    if(failTimes == 5):
        with open("/var/pktfwd/diagnostics", 'w') as diagOut:
            diagOut.write("false")





#Sleep forever