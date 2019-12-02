'''
    File name: OPC-R1_Logger_1.py
    Author: Vedanta Jha
    Date created: 2/12/2019
    Python Version: 3.6
'''

import serial, time, struct, csv, datetime, os

from usbiss.spi import SPI
import opc
#import opc_r1
from time import sleep

def logfilename():
    now = datetime.datetime.now()
    return 'OPC_R1_%0.4d-%0.2d-%0.2d_%0.2d-%0.2d-%0.2d.csv' % \
                (now.year, now.month, now.day,
                 now.hour, now.minute, now.second)


try:
    path = str(os.environ['outputPath_opc'])
except:
    print("could not find env variable ")
    path = ""

debug = 1
writeLog = 1


# Build the connector
#spi = SPI("COM22")
spi = SPI("/dev/serial/by-id/usb-Devantech_Ltd._USB-ISS._00045299-if00")

print("------------------------------------")
print("open serial port and connect to SPIt")
print("------------------------------------")

# Set the SPI mode and clock speed
spi.mode = 1
spi.max_speed_hz = 500000
alpha = opc.OPCR1(spi, firmware=[17,0])


print(alpha.read_firmware)

sleep(1)

sleep(5)

#alpha.toggle_fan(True)
IsOn = False
while IsOn is False:
    IsOn = alpha.toggle_Peripheral(True)
    print("the opc is now " + str(IsOn))
    sleep(0.5)

sleep(5)


print("------------------------------------")
print("create csv file")
print("------------------------------------")

if writeLog:

    csv_file = os.path.join(path, logfilename())
    csv_file = open(csv_file, mode='w')

    fieldnames = ["time","Bin 0", "Bin 1", "Bin 2", "Bin 3", "Bin 4", "Bin 5",
                "Bin 6", "Bin 7", "Bin 8", "Bin 9", "Bin 10", "Bin 11",
                "Bin 12", "Bin 13", "Bin 14", "Bin 15",
                "Bin1 MToF", "Bin3 MToF", "Bin5 MToF", "Bin7 MToF",
                "SFR", "Temperature", "Relative humidity",
                "Sampling Period", "Reject count Glitch", "Reject count Long",
                "PM1", "PM2.5", "PM10", "Checksum"]


    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    csv_file.flush()


print("------------------------------------")
print("starting reading loop")
print("------------------------------------")

buffer = []
readLoop = True
index = 0

while readLoop:

    data = alpha.histogram()

    if debug and len(data) != 0:
        # read the information string
        #print(repr(alpha.read_info_string()))
        # Read the histogram
        print(data)
        print(len(data))
    sleep(0.5)

    index += 1

    if writeLog and len(data) != 0:

        if debug: print("writing data to csv file!")

        writer.writerow({'time':str(datetime.datetime.now()),
                        'Bin 0':data["Bin 0"], 'Bin 1':data["Bin 1"], 'Bin 2':data["Bin 2"], 'Bin 3':data["Bin 3"], 'Bin 4':data["Bin 4"], 'Bin 5':data["Bin 5"],
                        'Bin 6':data["Bin 6"], 'Bin 7':data["Bin 7"], 'Bin 8':data["Bin 8"], 'Bin 9':data["Bin 9"], 'Bin 10':data["Bin 10"],
                        'Bin 11':data["Bin 11"], 'Bin 12':data["Bin 12"], 'Bin 13':data["Bin 13"], 'Bin 14':data["Bin 14"], 'Bin 15':data["Bin 15"],
                        'Bin1 MToF':data["Bin1 MToF"], 'Bin3 MToF':data["Bin3 MToF"], 'Bin5 MToF':data["Bin5 MToF"], 'Bin7 MToF':data["Bin7 MToF"], 'SFR':data["SFR"],
                        'Temperature':data["Temperature"], 'Relative humidity':data['Relative humidity'], 'Sampling Period':data["Sampling Period"],
                        'PM1':data["PM1"], 'PM2.5':data["PM2.5"], 'PM10':data["PM10"],
                        'Checksum':data["Checksum"], 'Reject count Glitch':data["Reject count Glitch"], 'Reject count Long':data["Reject count Long"]})


        csv_file.flush()


    if index == 60*45*2:
        readLoop = False


# Turn the device off
alpha.off()

