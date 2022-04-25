#
# CS 106  Final Project
#
# Author: Jake Roorda
# Date: 11/27/11
#
#  This is the main calling code for my room mapping program.
#
#  Skip to Line 420 for start of actual program
#

import sys
from optparse import OptionParser
import serial
import time
from dataset import DataSet
from echopoint import EchoPoint
from cs1graphics import *
from math import pi, sin, cos

VERSION = "1.0"
OPEN_DELAY = 1.5 #Number of seconds to wait for arduino to boot
VER_DELAY = .3 #Number of seconds to wait for arduino to respond after first test

parser = OptionParser()
parser.set_defaults(verbose=False)
parser.add_option("-v", "--verbose", dest="verbose",
                  help="turn on verbose output",
                  action="store_true")                  
(options, args) = parser.parse_args() 

# I did this to allow me to use verbose for debugging before option parser was inserted
if options.verbose:
    VERBOSE = True
else:
    VERBOSE = False

# This dictionary maps compass directions to step numbers.
compassToStep = {"N":100, "NNE":88, "NE":75, "ENE":63, "E":50, "ESE":38,\
                 "SE":25, "SSE":12, "S":200, "NNW":112, "NW":125, "WNW":137,\
                 "W":150, "WSW":162, "SW":175, "SSW":187}
# This dictionary maps colors to a lighter compliment color used to fill areas 
colorCompliment = {"red":"pink","orange":"orange4","yellow":"lightyellow","green":"lightgreen","blue":"lightblue","violet":"violetred"}


# def dataViewMenu(dataSet, canvas, prevColor, setMax = False):
#     """Prints the second menu and returns a tuple containign the choice, will
# also contain the tuple returned by the first menu if it is called"""
# 
#     #Default Settings
#     newDataConfig = False
# 
#     while True:
#         #Display the view menu
#         print "Please enter an option number"
#         print "1. Turn on square grid"
#         print "2. Turn on circular overlay"
#         print "3. Calculate Enclosed Area"
#         print "4. Calculate Circumference"
#         print "5. Add New Data Set"
#         print "6. Exit Program"
#         usrInp = raw_input()
# 
#         if usrInp not in('1','2','3','4','5','6'):
#             print "Invalid Entry, Please enter an option number"
#             continue
#         # Can now assume a good input
#         opt = int(usrInp)
# 
#         #Take the appropriate action
#         if opt == 1:
#             # Add the grid overlay
#             plotGridOverlay(canvas)
#             if VERBOSE:
#                 print"Grid Overlay Added"
#         elif opt == 2:
#             # Add the circular overlay
#             plotCircOverlay(400,400,canvas)
#             if VERBOSE:
#                 print"Circular Overlay Added"
#         elif opt == 3:
#             # Calculates the enclosed area
#             if VERBOSE:
#                 print"Calculating Area"
#             dataSet.calcArea(canvas, colorCompliment[prevColor])
#         elif opt == 4:
#             # Calculates the circumphrance
#             if VERBOSE:
#                 print"Calculating Circumphrance"
#             dataSet.calcCirc(canvas)
#         elif opt == 5:
#             # Calls the other menu to add a new data set, if that is allowed
#             if setMax:
#                 print"sorry, the system can currently only handle a maximum of two sets"
#             else:
#                 if VERBOSE:
#                     print"Getting a new data Set"
#                 newDataConfig = dataCollectionMenu(True, canvas)
#                 return newDataConfig
#         elif opt == 6:
#             # Getting Out
#             if VERBOSE:
#                 print"Bye"
#             canvas.close()
#             sys.exit(0)
#         
#     
# def dataCollectionMenu(offCenter, canv):
#     """Prints the menu that sets the parameters for the data set to be taken or loaded to the given canvas"""
#     #Default Settings
#     menuRangeMin = 0
#     menuRangeMax = 200
#     menuOffsetX = 400
#     menuOffsetY = 400
#     menuColor = "Blue"
#     menuSave = "No Save"
#     menuLoad = "No Load"
#     while True:
#         # Display the data set configuration menu with current settings
#         print "Please enter an option number"
#         print "1. Collect Data With Current Settings"
#         print "2. Restore Defaults"
#         print "3. Range (%d:%d)" % (menuRangeMin, menuRangeMax)
#         print "4. Color (%s)" % menuColor
#         print "5. Save as (%s)" % menuSave
#         print "6. Load Data Set (%s)" % menuLoad
#         if offCenter:
#             print"7. Offset (%5f:%5f)" % (menuOffsetX-400, menuOffsetY-400)
#         print "8. Exit"
# 
#         usrInp = raw_input()
#         # Check the formatt of the user input
#         if usrInp not in('1','2','3','4','5','6','7','8'):
#             print "Invalid Entry, Please enter an option number"
#             continue
#         # Can now assume good entry
#         opt = int(usrInp)
#         
#         usrChoice = False  # This variable set to True when entered values are good
# 
#         #Take the appropriate action
#         if opt == 1:
#             # Return the chosen settings if that is advisable
#             if portToUse == "Load" and menuLoad in ("No Load", "no load", "No", "no"):
#                 print"With no sensor you must load a file to continue"
#             else:
#                 return ((menuRangeMin,menuRangeMax),menuColor,menuSave,menuLoad,(menuOffsetX,menuOffsetY))
#         elif opt == 2:
#             # Reset the defaults
#             menuRangeMin = 0
#             menuRangeMax = 200
#             menuColor = "Blue"
#             menuSave = "No Save"
#             menuLoad = "No Load"
#             menuOffsetX = 400
#             menuOffsetY = 400
#         elif opt == 3:
#             # Get a new range, check it, reprompt if bad
#             while True:
#                 usrChoice = raw_input("Please enter the range in the format ### ###\n\
# all numbers must be between 0 and 200 inclusive\n")
#                 usrChoice = usrChoice.split()
#                 if len(usrChoice) != 2:
#                     usrChoice = False
#                     continue
#                 try:
#                     if int(usrChoice[0]) not in range(201) or int(usrChoice[1]) not in range(201):
#                         usrChoice = False
#                         continue
#                     if int(usrChoice[0]) > int(usrChoice[1]):
#                         continue
#                 
#                 except Exception:
#                     continue
#             
#                 menuRangeMin = int(usrChoice[0])
#                 menuRangeMax = int(usrChoice[1])
#                 break
#             
#         elif opt == 4:
#             # Get a new color for the set
#             while not usrChoice:
#                 usrChoice = raw_input('Please enter the name of a color for the points from this list\n\
# ("red","orange","yellow","green","blue","violet")\n')
#                 if usrChoice.lower() not in ("red","orange","yellow","green","blue","indigo","violet"):
#                     usrChoice = False
#                     continue
#                 menuColor = usrChoice.lower()
#         elif opt == 5:
#             # Get the same of the file to be saved
#             usrChoice = raw_input("Please enter the name of the file to be saved\n")
#             menuSave = usrChoice
#         elif opt == 6:
#             # Get and test the name of a file to load
#             while True:
#                 usrChoice = raw_input("Please enter the name of the file to be opened\n")
#                 if checkFile(usrChoice):
#                     # We can open the file
#                     menuLoad = usrChoice
#                     break
#             
#         elif opt == 7:
#             # Crazy off center addition stuff
#             if not offCenter:
#                 # They entered 7 even though it wasn't displayed
#                 print"So you think your cleaver...\nOnly the second dataSet can be offset"
#             else:
#                 # Offset is allowed,  usrChoice variable will be set to true if values are good
#                 usrChoice = False
#                 while not usrChoice:
#                     usrChoice = raw_input("Please enter the distance you want to offset the senson\n\
# The distance must be less than 2.00 meters\n")
#                     try:
#                         distToOffset = float(usrChoice)
#                     except Exception:
#                         # Was not a valid number
#                         usrChoice = False
#                         continue
#                     if 0 > distToOffset > 2.00:
#                         # Not in the valid range
#                         usrChoice = False
#                         continue
#                 step = False
#                 while not step:
#                     usrChoice2 = raw_input('Please enter a step number or a compass abbrebiation "NNW" for the angle to point the sensor\n')
#                     try:
#                         step = int(usrChoice2)
#                     except Exception:
#                         # Not a valid number, try our compass conversion
#                         if usrChoice2 in compassToStep:
#                             step = compassToStep[usrChoice2]
#                         else:
#                             # Bad input, start over
#                             step = False
#                 # Call the helpful sensor reposition function            
#                 sensorReposition(distToOffset, step, canv)
#                 # Set the values that do the actual offseting
#                 theta = ((step / 100.0) * pi) - (pi / 2)
#                 menuOffsetX = (distToOffset * 100 * cos(theta)) + 400
#                 menuOffsetY = (-1*distToOffset * 100 * sin(theta)) + 400
#                         
#         elif opt == 8:
#             canv.close()
#             sys.exit(0)
#         else:
#             # Input contianed but was not only a number
#             print"Invalid Entry, Please use the spicified format"


# def sensorReposition(distToOffset, step, canvas):
#     """Directs the user to the new sensor location"""
#     if portToUse == "Load":
#         # Unnecessary for loading data
#         pass
#     else:
#         # Draw the reposition diagram in the upper left
#         distCanv = canvas
#         goodZone = Rectangle(200,40,Point(100,200))
#         goodZone.setFillColor("green")
#         goodZone.setBorderWidth(0)
#         distCanv.add(goodZone)
#         distLine = Path(Point(0,200), Point(200,200))
#         distLine.setBorderWidth(6)
#         distLine.setBorderColor("white")
#         distCanv.add(distLine)
#         start = time.time()
#         sendRecieve("E")  # Enable the motor
#         waiting = 0
#         while waiting < 15:  # Run for 15 seconds
#             # Get a new distance
#             pos = sendRecieve("D%03d" % step)
#             if VERBOSE:
#                 print "raw pos:", pos
#             pos = pos - (distToOffset * 100)
#             pos = pos + 200
#             # Limit distance within bounds
#             if pos < 0:
#                 pos = 0
#             if pos > 400:
#                 pos = 400
#             # Move the indicator line to the right spot
#             distLine.moveTo(0,pos)
#             if VERBOSE:
#                 print pos
#             waiting = time.time() - start
#         sendRecieve("P")  # Park the motor
#         # Get rid of the reposition graphic
#         distCanv.remove(goodZone)
#         distCanv.remove(distLine)
        

def testPort(portName):
    """Test to see if the arduino is on the given port"""
    if portName.isdigit():
        # If just given a number, look at that numbered serial port
        test = serial.Serial()
        test.port = int(portName)
        if VERBOSE:
            print "Testing port COM" + str(portName)
    else:
        # Assume we were given port name, and try that
        try:
            if VERBOSE:
                print "testing port:", portName
            test = serial.Serial(portName, 9600) #Should Fail here if not availible
        except:
            return False
            if VERBOSE:
                print"Sorry, that port did not work"
    try:
        #For either method try to connect to the sensor
        test.open()
        if VERBOSE:
            print "it opened"
        test.baudrate = 9600
        time.sleep(OPEN_DELAY)
        test.write("P")
        time.sleep(VER_DELAY)
        if test.inWaiting():
            time.sleep(.05) # Wait for the whole line
            test.flushInput()
            test.close()
            if VERBOSE:
                print"Port Verified"
            return True
        if VERBOSE:
                print"No response from sensor"
        return False
    except Exception:
        if VERBOSE:
                print"Sorry, port failed to connect"
        try:
            #Try to clean things up
            test.flushOutput()
            test.flushInput()
            test.close()
            return False
        except Exception:
            #Just get out, girlfriend will throw your stuff you the window for you
            return False

def portSearch(minPort, maxPort):
    """Tests the given range of serial ports to find and use a good one by default"""
    for port in range(minPort, maxPort+1):
        if testPort(str(port)):
            return str(port)
    print "No good ports were found"
    return -1
    
        
def userReady():
    """Warns the user of correct sensor usage"""
    print "Position sensor for data collection"
    print "Rotate the sensor so that it points in the direction of the arrow and has enough\
slack in the wires to rotate 180 degrees in either direction"
    print "Plug the power adapter into the stand alone jack if it is not allready"
    raw_input("When you are ready press enter to collect the data\nYou may want to hold the \
the base of the sensor to keep it steady")
    return

def collectData(sel, ds, refX=400, refY=400):
    """Actualy collects the data and adds it to the given data set that it returns"""
    startPos = sel[0][0]
    endPos = sel[0][1]
    color = sel[1]
    cmd = startPos
    sendRecieve("E") #Enable the motor
    while cmd <= endPos:
        if VERBOSE:
            print"Moving motor to:", cmd
        dist = sendRecieve("D%03d" % cmd)
        if VERBOSE:
            print"Distance was", dist
        ptToAdd = EchoPoint("rs", dist, cmd, refX, refY, color)
        ds.addPoint(ptToAdd)
        if VERBOSE:
            print"Point added"
        cmd += 1
    sendRecieve("D100") #Center the motor
    sendRecieve("P")  #Park the motor
    return ds

           
def sendRecieve(send):
    """Sends the given command, waits and returns the response"""
    ser.write(send)
    while ser.inWaiting() == 0: #Wait for response
        pass
    time.sleep(.04) #Wait for the whole float
    recVal = ser.read(ser.inWaiting())
    recVal = float(recVal)
    return recVal

def plotGridOverlay(canvas):
    """Ads the 1 meter grid to the canvas""" 
    for x in range(0,801,100):
        pthToPlot = Path(Point(x,0),Point(x,800))
        pthToPlot.setBorderColor("grey")
        canvas.add(pthToPlot)
    for y in range(0,801,100):
        pthToPlot = Path(Point(0,y),Point(800,y))
        pthToPlot.setBorderColor("grey")
        canvas.add(pthToPlot)

def plotCircOverlay(xCent, yCent, canvas):
    """ Ads the 1 meter circular overlay to the canvas"""
    for r in range(50,551, 50):
        circToPlot = Circle(r,Point(xCent, yCent))
        circToPlot.setBorderColor("grey")
        if r % 100 == 0:
            circToPlot.setBorderWidth(3)
        canvas.add(circToPlot)

def checkFile(filename):
    """Checks to see if we can open the given file name, returns a boolean"""
    try:
        testFile = open(filename, "r")
        testFile.close()
        return True
    except:
        return False
    
#
#  Program Starts Here
#

#Display the program name, author and version
print "BBString - Robotics Musicianship Project"


#Get the com port instructions from the user

goodPort = False
while not goodPort:
    #Ask user for port name
    portToTest = raw_input("Please Enter a port number or full name to use. \nEnter Q to quit, S to skip, or E to search for ports on Windows.  \nOn Linux? might I suggest '/dev/ttyUSB0'\n")
    if portToTest in ("S", "s", "Skip", "skip"):
        if VERBOSE:
            print "Continuing without sensor"
        portToUse = "Load"
        break
    elif portToTest in ("Q", "q", "Quit", "quit"):
        print "Exiting the program"
        sys.exit(0)
    elif portToTest in ("E", "e"):
        portToUse = portSearch(0,9)
        if portToUse == -1:
            # Returned if no good port is found
            continue
        else:
            goodPort = True
            if VERBOSE:
                print "Using Port:", portToUse
    else:     
        #Manual Mode: Test the port
        goodPort = testPort(portToTest)
        if goodPort:
            portToUse = portToTest
            if VERBOSE:
                print "Using Port:", portToUse

# Now we should have a good port, let's open it up

if portToUse.isdigit():
    #Create a new serial instance
    ser = serial.Serial()
    #Open that numbered serial port
    ser.port = int(portToUse)
    ser.open()
    #Set the baudrate
    ser.baudrate = 9600
    #Wait for the arduino to boot up
    time.sleep(OPEN_DELAY)
elif portToUse == "Load":
    pass
else:
    #Open the named port and set baudrate
    ser = serial.Serial(portToUse, 9600)
    ser.open()
    #Wait for the arduino to boot up
    time.sleep(OPEN_DELAY)
    


# Initiate the pins
## Read current position
## Reset to a pre-defined position if needed: Check sensorReposition

# Set them as output if needed
# Set rotaion parameters - num_steps and velocity
# Checkout SendReceive to send and receive data
# Close port


# #Create the canvas
# canv = Canvas(800,800,"Black")
# # Get the first data collection settings
# selections = dataCollectionMenu(False,canv)

# Create a new empty dataSet
firstSet = DataSet("auto")
# If the user is not loading a set take the data
if selections[3] in ("No Load", "no load", "No", "no"):
    userReady()
    firstSet = collectData(selections, firstSet)
    firstSetColor = selections[1]
else:
    #Load the given file
    firstSet.loadSet(selections[3])
    firstSetColor = firstSet._color
# Save the dataSet if requested
if selections[2] not in ("No", "no", "no save", "No Save"):
    firstSet.saveSet(selections[2])

# Draw the set and the little X in the center
firstSet.drawSet(canv)
pth1 = Path([Point(390,400),Point(410,400)])
pth2 = Path([Point(400,390),Point(400,410)])
pth1.setBorderColor(firstSetColor)
pth2.setBorderColor(firstSetColor)
canv.add(pth1)
canv.add(pth2)

#We are now done drawing, Print the second Menu of Choices
newSetConfig = dataViewMenu(firstSet, canv, firstSetColor.lower())

#User must have wanted another dataSet, take it like the first one
secondSet = DataSet("auto")
# If the user is not loading a set take the data
if newSetConfig[3] in ("No Load", "no load", "No", "no"):
    secondSet = collectData(newSetConfig, secondSet, newSetConfig[4][0],newSetConfig[4][1])
    secondSetColor = newSetConfig[1]
else:
    #Load the given file
    secondSetColor = secondSet.loadSet(newSetConfig[3],newSetConfig[4][0],newSetConfig[4][1])
# Save the dataSet if requested
if newSetConfig[2] not in ("No", "no", "no save", "No Save"):
    secondSet.saveSet(selections[2])

#Draw the second set and its center X
secondSet.drawSet(canv)
pth1 = Path([Point(newSetConfig[4][0] - 10,newSetConfig[4][1]),Point(newSetConfig[4][0] + 10,newSetConfig[4][1])])
pth2 = Path([Point(newSetConfig[4][0],newSetConfig[4][1] - 10),Point(newSetConfig[4][0],newSetConfig[4][1] + 10)])
pth1.setBorderColor(secondSetColor)
pth2.setBorderColor(secondSetColor)
canv.add(pth1)
canv.add(pth2)

#Diplay the view menu one more time
dataViewMenu(secondSet, canv, secondSetColor.lower(), True)


#Program should exit from a menu function...It should never get here
#Some problems may cause it to get here, so we will try to close gracefully in these cases
try:
    ser.close()
except Exception:
    pass

print "Sorry"



