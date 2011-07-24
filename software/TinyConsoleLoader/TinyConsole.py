#!/usr/bin/python
#Console Loader for TinyG
#This version of the Console loader is meant to be used with 308.11 + versions of TinyG
#Riley Porter
#Synthetos.com

import serial

import serial, sys, time
from ser.serial_init import scan

#Terminal Color Module
from colorama import init
from termcolor import colored

import sys
import random
from optparse import OptionParser
import time

logo = """
  _______ _              _____ 
 |__   __(_)            / ____|
    | |   _ _ __  _   _| |  __ 
    | |  | | '_ \| | | | | |_ |
    | |  | | | | | |_| | |__| |
    |_|  |_|_| |_|\__, |\_____|
    CONSOLE        __/ |       
                  |___/        """




def usage():
    print """[?] Usage: 
         -f indicates the filename to be sent to TinyG.
         -s indicates the serial port that TinyG is connected to.
EXAMPLE:
           python TinyConsole.py -f gcodefile.nc -s COM7
           or
           python TinyConsole.py -filename gcodefile.nc -serialport /dev/tty/USB0"""

def init_serial():
    #Get Serial Port Options
    def pick_port():
        print colored("Scanning Ports:\n", 'magenta')
        while(1):
            ports = scan()
            if len(ports) == 0:
                self.scanports_mode()
    
            print "Select a Serial Port:"
            count = 1
            for port in ports:
                print "[%s] %s " % (count, port)
                count = count + 1
            print colored(("Default Selection: [%s]  "% (ports[-1])), 'blue', attrs=['bold'])
    
            try:
                port_choice =(raw_input("Choice: "))
                if port_choice == "":
                    port_choice = -1 #Enter was hit as the default port was selected
                    return port_choice, ports
    
                else: #A port number was selected
                    port_choice = (int(port_choice)-1)
                    if port_choice >= len(ports):
                        raise ValueError()
                    return port_choice, ports
                
            except ValueError:
                print colored("Invalid Choice.... Try Again...\n", 'red')
            
    port_selected, ports = pick_port()

    try:
        s = serial.Serial(ports[port_selected], 115200, timeout=.5)
        print colored(("TinyG successfully connected to %s" % ports[port_selected]), 'magenta')
        return s
    except:
        print colored("[ERROR] Opening Serial Port", 'red')
        pick_port()
    

def ser_term():
    """Main Serial terminal function"""
    s.writelines("\n") #Get a prompt in the serial recv buffer
    tmpBuf = s.readall().rstrip().lstrip()  #This is to capture the recv buffer to a var to put it on the same line as the raw_input

    while 1 :

        #Simple prompt fix to catch the right type of prompt string
        if type(tmpBuf) == str:
            prompt = tmpBuf
        else:
            tmpBuf = tmpBuf[-1]


        # get keyboard input
        input = raw_input(colored(tmpBuf, 'green'))
        
        ########################################################
        ## Parse Commandline Commands
        if input == 'exit':
            """Exit the loader"""
            print colored("Exiting....", "grey")
            sys.exit()
            
        elif input.find("#FILE#") <= 0:  #Look for the #FILE# string
            """loading a gcode file function called"""
            loadFile(input)
        ########################################################    
            
        else:
            s.write(input + "\n")
            if s.inWaiting > 0:
                tmpBuf =  s.readall().split('\n')
                for bufLine in tmpBuf:
                    if bufLine == tmpBuf[-1]:
                        pass
                    else:
                        print bufLine
def loadFile(input):
    def processFileXOFF(f):
        """Used Grep Flow Control"""
        for line in f.readlines():
            time.sleep(.25) #Not cool man
            s.writelines(line)
            y = s.readline()
            #print y.rstrip()
            if y != "":
                if "ok" in y:
                    print "\t[#]LINE: %s" % line.rstrip()
                else:
                    print "\t[#]LINE: %s" % line.rstrip()
 
    def processFileXON(f):
        """Use TinyG Flow Control"""
        for line in f.readlines():
            s.writelines(line)
            y = s.readline()
            print y.rstrip()

        
    try:
        input = input.split("#FILE#")[-1] #Parse out the path/to/file.gc
        f = open(input, 'r')
    except IOError:
        pass
    #Begin Processing the Gcode File
    print colored("[*] Begin Processing Gcode File", "magenta")
    #Check to see if flow control is enabled
    if XON == True:
        processFileXON(f)

    elif XON == False:
        processFileXOFF(f)

    
def main():
    init()  #Windows Terminal Color Support.. Just ignore this
    print colored(logo, 'blue') #Print the TinyG Console Logo
    global s, XON
    XON = False
    
    s = init_serial()
    #s = serial.Serial(ports[port_choice], 115200, timeout=.5) #Setup Serial port COnnection
    s.xonxoff = True #Turn on software flow control.  TinyG supports this
    ser_term() #Run the terminal function

if __name__ == "__main__":
    main()