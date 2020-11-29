
# Import libraries required for the script (Genie - testbed for loading the testbed file , datetime for timestamps on the output files)

from genie.testbed import load
from datetime import datetime
from unicon.core.errors import TimeoutError,StateMachineError,ConnectionError

# Creates the text file that the results are stored with the current date and time

file_list = ['Layer1.txt']
now = datetime.now().strftime("%Y-%m-%d %H:%M")
for file in file_list:
    with open(file, 'w') as f:
        f.write("Health Check Execution time is" + "  " + "[" + str(now) + "]\n")

# Load the list of devices created in the testbed file and assign it to an object "tb"

tb = load('h.yml')

# iterate over the list of target devices within the testbed variable tb, and assign each device to "dev"  

for device in tb:

   dev = device

# Identify the device ios type (either ios,ioxe or nxos), and connect to the device
# Incorporate error handling so that if any device fails to connect by giving any of the exception errors, the code terminates.

   if dev.os == 'ios':
    try:
      dev.connect()
    except (TimeoutError, StateMachineError, ConnectionError):
      print("\n Health Check is unable to connect to all of the devices")
    else:

# using pyats parsers, run the Layer1 check IOS commands and parse the output into the various dictionaries.
        
      ios_status = dev.parse('show int status')
      ios_bundle = dev.parse('show etherchannel summary')
      ios_errors = dev.parse('show interfaces')

# Opens the text file created for the results and appends a header for each device for the first command output run

      with open('Layer1.txt', 'a') as f:
       f.write("IOS device:" + " " + "[" + str(dev) + "]" + "  INTERFACES STATUS EXCEPTIONS: \n \n")
       
# Iterates over each interface captured in the "show int status" command, identifies the status, duplex and port_speed
# Checks for interfaces that are not up, as well as interfaces with less than 1Gb link speeds and Full duplex.
      
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

# Opens the text file created for the results and appends a header for each device for the second command output run      
      with open('L1.txt', 'a') as f:
        f.write("\n IOS device:" + " " + "[" + str(dev) + "]" + " ETHERCHANNEL ISSUES: \n")

# Iterates over each interface captured in the "show etherchannel summary" command and captures the state of the flags
# Checks each of the identified states for non-operational status such as down or suspended and writes the results to a text file 

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


# Iterates over each interface captured in the "show etherchannel summary" command and captures the state of the flags

   if dev.os == 'nxos':

      dev.connect()

      nxos_status = dev.parse('show int status')
      nxos_bundle = dev.parse('show feature')
      nxos_errors = dev.parse('show interface')
      
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




