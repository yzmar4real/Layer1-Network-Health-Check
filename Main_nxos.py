
# Import libraries required for the script (Genie - testbed for loading the testbed file , datetime for timestamps on the output files)

from genie.testbed import load
from datetime import datetime
from unicon.core.errors import TimeoutError,StateMachineError,ConnectionError

# Creates the text file that the results are stored with the current date and time

file_list = ['L1_NXOS.txt']
now = datetime.now().strftime("%Y-%m-%d %H:%M")
for file in file_list:
    with open(file, 'w') as f:
        f.write("Health Check Execution time is" + "  " + "[" + str(now) + "]\n\n")

# Load the list of devices created in the testbed file and assign it to an object "tb"

tb = load('hosts.yml')

# iterate over the list of target devices within the testbed variable tb, and assign each device to "dev"  

for device in tb:

   dev = device

# Identify the device ios type (either ios,ioxe or nxos), and connect to the device
# Incorporate error handling so that if any device fails to connect by giving any of the exception errors, the code terminates.
   if dev.os == 'nxos':
     try:
      dev.connect()
     except (TimeoutError,StateMachineError,ConnectionError):
      print("\n Health Check is unable to connect to all of the devices")
      break
     else:

      # using pyats parsers, run the Layer1 check NXOS commands and parse the output into the various dictionaries.
      nxos_status = dev.parse('show int status')
      nxos_bundle = dev.parse('show port-channel summary')
      nxos_errors = dev.parse('show interface')

      # Opens the text file created for the results and appends a header for each device for the first command output run
      with open('L1_NXOS.txt', 'a') as f:
        f.write("NXOS device:" + " " + "[" + str(dev) + "]" + "  INTERFACES STATUS EXCEPTIONS: \n \n")

      # Iterates over each interface captured in the "show int status" command, identifies the status, duplex and port_speed
      # Checks for interfaces that are not up, as well as interfaces with less than 1Gb link speeds and Full duplex configuration.
      # writes the output for each of the exceptions into the text file under the Interfaces Status Exception section

      for interface in (nxos_status['interfaces'].keys()):
        r = nxos_status['interfaces'][interface]['status']
        r1 = nxos_status['interfaces'][interface]['duplex_code']
        r2 = nxos_status['interfaces'][interface]['port_speed']
           
        if r != 'connected' or r1 != 'full' or r2 != '1000':
           with open('L1_NXOS.txt', 'a') as f:
             f.write(interface + " " + " " + "status is " + r  + " ," + "duplex is" + " " + r1 + " ," + " " + "speed is" + "  " + r2 + " \n")
      
      # Opens the text file created for the results and appends a header for each device for the second command output run

      with open('L1_NXOS.txt', 'a') as f:
        f.write("\nNXOS device:" + " " + "[" + str(dev) + "]" + " ETHERCHANNEL ISSUES: \n")

      # Iterates over each portchannel captured in the "show port-channel summary" command, identifies the name of the interface.
      # Checks for states of the members that are not up, and captures the output in an object.
      # writes the output for each of the exceptions into the text file under the Etherchannel Issues.

      for interface in (nxos_bundle['interfaces'].keys()):
        if interface != 'mgmt0':
          k = nxos_bundle['interfaces'][interface]['members']
          k0 = interface

        for interface in k.keys():
         k1 = k[interface]['flags']

         if k1 != "P":

           with open('L1_NXOS.txt', 'a') as f:
             f.write("On PortChannel" + " " + str(k0) + " , " + "member" + " " + str(interface) + " " + "has flags" +  "  " + str(k1) + " " + "\n")      
             
      # Opens the text file created for the results and appends a header for each device for the third command output run

      with open('L1_NXOS.txt', 'a') as f:
        f.write("\nNXOS device:" + " " + "[" + str(dev) + "]" + " INTERFACES WITH ERRORS: \n \n")
      
      # Iterates over each interface captured in the "show interfaces" command, identifies the name of the interface.
      # Checks for input errors, crc_errors and output_errors and compares the values against an ideal state.
      # writes the output for each of the exceptions into the text file under the interface with errors section.

      for interface in nxos_errors:
          #if interface != 'mgmt0' :
           try:
             s = nxos_errors[interface]['counters']['in_errors']
             s1 = nxos_errors[interface]['counters']['in_crc_errors']         
             s2 = nxos_errors[interface]['counters']['out_errors']
           except:
             print('Some Interfaces were skipped for this command')
             pass
           else:
             if s != 0 or s1 != 0 or s2 != 0 :
               with open('L1_NXOS.txt', 'a') as f:
                  f.write( interface + " " + " " + "has " + str(s)  + " " + "input errors," + " " + str(s1) + " " + "CRC errors," + " " + str(s2) + " " + "Output errors" " \n")




