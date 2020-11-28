from genie.testbed import load
import json
from datetime import datetime
import requests

file_list = ['Layer1.txt', 'L1.txt']
now = datetime.now().strftime("%Y-%m-%d %H:%M")
for file in file_list:
    with open(file, 'w') as f:
        f.write("[" + str(now) + "]\n")

tb = load('h.yml')

for device in tb:

   dev = device

   if dev.os == 'ios':

      dev.connect()
    
      ios_status = dev.parse('show int status')
      ios_bundle = dev.parse('show etherchannel summary')
      ios_errors = dev.parse('show interfaces')

      with open('L1.txt', 'a') as f:
       f.write("IOS device:" + " " + "[" + str(dev) + "]" + "  INTERFACES STATUS EXCEPTIONS: \n \n")
       
      
      for interface in (ios_status['interfaces'].keys()):
        r = ios_status['interfaces'][interface]['status']
        r1 = ios_status['interfaces'][interface]['duplex_code']
        r2 = ios_status['interfaces'][interface]['port_speed']
           
        if r != 'connected':
           with open('L1.txt', 'a') as f:
             f.write(interface + " " + " " + "status is " + r  + " \n")
        if r1 != 'a-full':
           with open('L1.txt', 'a') as f:
             f.write(interface + " " + " " + "duplex  is " + r1  + " \n")
        if r2 != 'a-1000':
           with open('L1.txt', 'a') as f:
             f.write(interface + " " + " " + "speed is " + r2  + " \n \n")
      
      with open('L1.txt', 'a') as f:
        f.write("\n IOS device:" + " " + "[" + str(dev) + "]" + " ETHERCHANNEL ISSUES: \n")

      for interface in (ios_bundle['interfaces'].keys()):
        k = ios_bundle['interfaces'][interface]['members']
        y = ios_bundle['interfaces'][interface]['name']

        with open('L1.txt', 'a') as f:
            f.write("On" + " " + "PortChannel" + " " + str(y) + "\n")

        for interface in k.keys():
         k1 = k[interface]['flags']

        if k1 != "U":

           with open('L1.txt', 'a') as f:
             f.write("Member" + " " + str(interface) + " " + "has flags" +  "  " + str(k1) + " " + "\n")       

      for interface, details in ios_errors.items():
        s = (details["counters"]['in_errors'])
        s1 = (details["counters"]['in_crc_errors'])
        s2 = (details["counters"]['out_errors'])                       
        
        if s != 0 or s1 != 0 or s2 != 0:
           with open('L1.txt', 'a') as f:
              f.write(interface + " " + " " + "has " + str(s)  + "input errors," + " " + str(s1) + "CRC errors," + " " + str(s2) + "Output errors" " \n")


   if dev.os == 'nxos':

      dev.connect()

      nxos_status = dev.parse('show int status')
      nxos_bundle = dev.parse('show feature')
      nxos_errors = dev.parse('show interface')
   
      with open('Layer2.txt', 'a') as f:
       f.write("\n NXOS device:" + " " + "[" + str(dev) + "]" + "  INTERFACES STATUS EXCEPTIONS: \n \n")
      
      for interface in nxos_errors:
         if interface != 'mgmt0':
           try:
            s = nxos_errors[interface]['counters']['in_errors']
            s1 = nxos_errors[interface]['counters']['in_crc_errors']         
            s2 = nxos_errors[interface]['counters']['out_errors']
           except:
             pass

             if s == 0 or s1 == 0 or s2 == 0 :
               with open('Layer2.txt', 'a') as f:
                  f.write(interface + " " + " " + "has " + str(s)  + "input errors," + " " + str(s1) + "CRC errors," + " " + str(s2) + "Output errors" " \n")




