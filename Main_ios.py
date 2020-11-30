
# Import libraries required for the script (Genie - testbed for loading the testbed file , datetime for timestamps on the output files)

from genie.testbed import load
from datetime import datetime
from unicon.core.errors import TimeoutError,StateMachineError,ConnectionError

# Creates the text file that the results are stored with the current date and time

file_list = ['L1_IOS.txt']
now = datetime.now().strftime("%Y-%m-%d %H:%M")
for file in file_list:
    with open(file, 'w') as f:
        f.write("Health Check Execution time is" + "  " + "[" + str(now) + "]\n")

# Load the list of devices created in the testbed file and assign it to an object "tb"

tb = load('hosts.yml')

# iterate over the list of target devices within the testbed variable tb, and assign each device to "dev"  

for device in tb:

   dev = device

# Identify the device ios type (either ios,ioxe or nxos), and connect to the device
# Incorporate error handling so that if any device fails to connect by giving any of the exception errors, the code terminates.

   if dev.os == 'ios' or dev.os == 'iosxe':
    try:
      dev.connect()
    except (TimeoutError, StateMachineError, ConnectionError):
      print("\n Health Check is unable to connect to all of the devices")
      break
    else:
    

# using pyats parsers, run the Layer1 check IOS commands and parse the output into the various dictionaries.

      ios_status = dev.parse('show int status')
      ios_bundle = dev.parse('show etherchannel summary')
      ios_errors = dev.parse('show interfaces')

# Opens the text file created for the results and appends a header for each device for the first command output run

      with open('L1_IOS.txt', 'a') as f:
       f.write("IOS device:" + " " + "[" + str(dev) + "]" + "  INTERFACES STATUS EXCEPTIONS: \n \n")
       
# Iterates over each interface captured in the "show int status" command, identifies the status, duplex and port_speed
# Checks for interfaces that are not up, as well as interfaces with less than 1Gb link speeds and Full duplex.
      
      for interface in (ios_status['interfaces'].keys()):
        r = ios_status['interfaces'][interface]['status']
        r1 = ios_status['interfaces'][interface]['duplex_code']
        r2 = ios_status['interfaces'][interface]['port_speed']
        
        if r != 'connected' or r1 != 'full' or r2 != '1000':
           with open('L1_IOS.txt', 'a') as f:
             f.write(interface + " " + " " + "status is " + r  + " ," + "duplex is" + " " + r1 + " ," + " " + "speed is" + "  " + r2 + " \n") 

# Opens the text file created for the results and appends a header for each device for the second command output run      
      with open('L1_IOS.txt', 'a') as f:
        f.write("\nIOS device:" + " " + "[" + str(dev) + "]" + " ETHERCHANNEL ISSUES: \n")

      # Iterates over each interface captured in the "show etherchannel summary" command and captures the state of the flags
      # Checks each of the identified states for non-operational status such as down or suspended and writes the results to a text file 
      
      for interface in (ios_bundle['interfaces'].keys()):
        k = ios_bundle['interfaces'][interface]['members']
        y = ios_bundle['interfaces'][interface]['name']

        for interface in k.keys():
           k1 = k[interface]['flags']

           if k1 == 'P':

            with open('L1_IOS.txt', 'a') as f:
             f.write("On " + " " + str(y) + " " + " Interface" + " " + str(interface) + " " + "has flags" +  "  " + str(k1) + " " + "\n")       

      
      # Opens the text file and appends a header for each device for the third command output run
            
      with open('L1_IOS.txt', 'a') as f:
        f.write("\nIOS device:" + " " + "[" + str(dev) + "]" + " ERROR COUNTERS: \n")
      
      # Iterates over each interface captured in the "show etherchannel summary" command and captures the state of the flags
      # Checks each of the identified states for non-operational status such as down or suspended and writes the results to a text file 
      
      for interface, details in ios_errors.items():
        try:
         s = (details["counters"]['in_errors'])
         s1 = (details["counters"]['in_crc_errors'])
         s2 = (details["counters"]['out_errors'])                       
        except:
          print("Some interfaces were skipped for this command")
          pass
        else:
        
         if s == 0 or s1 == 0 or s2 == 0:
           with open('L1_IOS.txt', 'a') as f:
              f.write(interface + " " + " " + "has " + " " + str(s)  + " " +  "input errors," + " " + str(s1) + " " + "CRC errors," + " " + str(s2) + " " +  "Output errors" " \n")
  

