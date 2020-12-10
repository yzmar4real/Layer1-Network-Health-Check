from genie.testbed import load
from genie.utils import Dq
import json
from datetime import datetime
import requests
from unicon.core.errors import TimeoutError,StateMachineError,ConnectionError

# Creates the text file that the results are stored with the current date and time

file_list = ['Errors.txt', 'L1.txt']
now = datetime.now().strftime("%Y-%m-%d %H:%M")
for file in file_list:
    with open(file, 'w') as f:
        f.write("\nHealth Check Execution time is" + "  " + "[" + str(now) + "]\n")

# Loads the testbed file "hosts.yml" which has all logon credentials

tb = load('hosts.yml')

# iterate over the list of target devices within the testbed variable tb, and assign each device to "dev"  

for device in tb:

   dev = device

# Identify the device ios type (either ios,ioxe or nxos), and connect to the device
# Incorporate error handling so that if any device fails to connect by giving any of the exception errors, the name of the device is stored in "Errors.txt"
# After each error, script automatically re-iterates into the next device within the file.

   if dev.os == 'ios' or dev.os == 'iosxe':
    try:
      dev.connect()
    except (TimeoutError, StateMachineError, ConnectionError):
      print("\n Health Check is unable to connect to all of the devices")
      with open('Errors.txt', 'a') as f:
       f.write("\n\nIOS device:" + " " + "[" + str(dev) + "]" + "  is not available: \n \n")
      #pass
    else:

# using pyats parsers, run the Layer1 check IOS commands and parse the output into the various dictionaries.
# Dq API is used to ensure that only interfaces "notconnected" are stored in the variable
# Error handling is included to ensure that if the command is not supported, it stores the name of the device into the "Errors.txt" file

     try:
      ios_status = dev.parse('show int status')
     
      for interface in ios_status['interfaces'].keys():
       out = ios_status.q.contains('notconnect').get_values('interfaces')
       
      with open('L1.txt', 'a') as f:
       f.write("\nOn " + " " + str(dev) + " " + "the following ports are down:" + "\n" + str(out) + " " + "\n")
     except:
         with open('Errors.txt', 'a') as f:
          f.write("On " + "[" + str(dev) + "]" + " command SHOW INT STATUS is not supported: \n \n")
     else:
      print("Code will now continue to run")

# using pyats parsers, run the Layer1 check IOS commands and parse the output into the various dictionaries.

     try:
      ios_bundle = dev.parse('show etherchannel summary')
      
      for interface in ios_bundle['interfaces'].keys():
       out1 = ios_bundle.q.contains('D').get_values('members')
      
      with open('L1.txt', 'a') as f:
       f.write("On " + " " + str(dev) + " " + "Member" + " " + str(interface) + " " + "has flags" +  "  " + str(out1) + " " + "\n \n")
     except:
         with open('Errors.txt', 'a') as f:
          f.write("On " + "[" + str(dev) + "]" + " command SHOW ETHERCHANNEL SUMMARY is not supported: \n \n")
     else:
      print("Code will now continue to run")

# using pyats parsers, run the Layer1 check IOS commands and parse the output into the various dictionaries.

     try:
      ios_errors = dev.parse('show interfaces')
          
      for interface, details in ios_errors.items():
        try:
         s = (details["counters"]['in_errors'])
         s1 = (details["counters"]['in_crc_errors'])
         s2 = (details["counters"]['out_errors'])                       
        except:
          print("Some interfaces were skipped for this command")
          #pass
        else:
        
         if s != 0 or s1 != 0 or s2 != 0:
           with open('L1.txt', 'a') as f:
              f.write("On Device" + " " + str(dev) + " " + interface + " " + " " + "has " + " " + str(s)  + " " +  "input errors," + " " + str(s1) + " " + "CRC errors," + " " + str(s2) + " " +  "Output errors" " \n")
     except:
        with open('Errors.txt', 'a') as f:
          f.write("On " + "[" + str(dev) + "]" + " command SHOW INTERFACES is not supported: \n \n")
     else:
        print('End of the Code Run')


# Identify the device ios type (either ios,ioxe or nxos), and connect to the device
# Incorporate error handling so that if any device fails to connect by giving any of the exception errors, the name of the device is stored in "Errors.txt"
# After each error, script automatically re-iterates into the next device within the file.

   if dev.os == 'nxos':
    try:
      dev.connect()
    except (TimeoutError, StateMachineError, ConnectionError):
      print("\n Health Check is unable to connect to all of the devices")
      with open('Errors.txt', 'a') as f:
       f.write("\n\nNXOS device:" + " " + "[" + str(dev) + "]" + "  is not available: \n \n")
      #pass
    else:

# using pyats parsers, run the Layer1 check IOS commands and parse the output into the various dictionaries.
     try:
      nxos_status = dev.parse('show int status')
     
      for interface in nxos_status['interfaces'].keys():
       out = nxos_status.q.contains('notconnec').get_values('interfaces')
       
      with open('L1.txt', 'a') as f:
       f.write("\nOn " + " " + str(dev) + " " + "the following ports are down:" + "\n" + str(out) + " " + "\n\n")
     except:
         with open('Errors.txt', 'a') as f:
          f.write("On " + "[" + str(dev) + "]" + " command SHOW INT STATUS is not supported: \n \n")
     else:
      print("Code will now continue to run")

# using pyats parsers, run the Layer1 check IOS commands and parse the output into the various dictionaries.

     try:
      nxos_bundle = dev.parse('show port-channel summary')
      
      for interface in nxos_bundle['interfaces'].keys():
        k = nxos_bundle['interfaces'][interface]['members']
        k0 = interface
        
        for interface in k.keys():
         k1 = k[interface]['flags']

         if k1 != "P":

           with open('L1.txt', 'a') as f:
             f.write("On" + " " + str(dev) + " " + str(k0) + " , " + "member" + " " + str(interface) + " " + "has flags" +  "  " + str(k1) + " " + "\n")
      #with open('L1_NXOS.txt', 'a') as f:
        #f.write("On " + " " + str(dev) + " " + "Member" + " " + str(interface) + " " + "has flags" +  "  " + str(out1) + " " + "\n \n")
     except:
         with open('Errors.txt', 'a') as f:
          f.write("\nOn " + "[" + str(dev) + "]" + " command SHOW ETHERCHANNEL SUMMARY is not supported: \n \n")
     else:
      print("Code will now continue to run")

# using pyats parsers, run the Layer1 check IOS commands and parse the output into the various dictionaries.

     try:
      nxos_errors = dev.parse('show interface')
          
      for interface, details in nxos_errors.items():
        try:
         s = (details["counters"]['in_errors'])
         s1 = (details["counters"]['in_crc_errors'])
         s2 = (details["counters"]['out_errors'])                       
        except:
          print("Some interfaces were skipped for this command")
          pass
        else:
        
         if s != 0 or s1 != 0 or s2 != 0:
           with open('L1.txt', 'a') as f:
              f.write("On Device" + " " + str(dev) + " " + interface + " " + " " + "has " + " " + str(s)  + " " +  "input errors," + " " + str(s1) + " " + "CRC errors," + " " + str(s2) + " " +  "Output errors" " \n")
     except:
        with open('Errors.txt', 'a') as f:
          f.write("On " + "[" + str(dev) + "]" + " command SHOW INTERFACES is not supported: \n \n")
     else:
        print('End of the Code Run')
   
