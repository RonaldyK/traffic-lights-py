# M2 Checkpoint 1 - Traffic Light Project
# Created By: MH05                
# Created Date: 12/04/2024                              
# version = '1.0'                  
# Globals   
    # userChoice = 0          
    # settingPin = 1234        
    # ultraSensorCutoff = 20  
    # distanceMeasured = []   

    # stageOneDuration = 30
    # stageTwoDuration = 3
    # stageThreeDuration = 3
    # stageFourDuration = 30
    # stageFiveDuration = 3
    # stageSixDuration = 3
    # currentStage = 0
    # pushButtonStage1 = []
    # pushButtonStage2 = []
    # pedestrianCount = 0
    # pedestrianCount1 = 0
    # pedestrianCount2 = 0
# Functions
    # setup()
    # loop()
    # display_service_menu()
    # maintenance_adjustment_mode()
    # normal_operation_mode()
    # data_observation_mode()
    # traffic_graph_plot(distanceMeasured)
    # read_sensor()
    # sevenSeg(message)
    # push_button()
    # traffic_stage_manager()
                      

import time
import matplotlib.pyplot as plt
from pymata4 import pymata4


board = pymata4.Pymata4()

userChoice = 0          # User choice tracks which opeerating mode the system is supposed to be in.
settingPin = 1234       # Pin to enter maintanance mode.
ultraSensorCutoff = 20  # Cutoff distance for the ultrasound sensor
distanceMeasured = []   # List which hold values for proccessed distance measurements from the ultrasound sensor.

stageOneDuration = 30   # These 6 variables holds the duration for each traffic light stage in seconds
stageTwoDuration = 3    #
stageThreeDuration = 3  #
stageFourDuration = 30  #
stageFiveDuration = 3   #
stageSixDuration = 3    #

currentStage = 0        # Tracks the current traffic stage.
pedestrianCounter = 0



lastDetectedChange = 0 # Hold time for pushbutton debounce.
bouncyTimer = 0.4 # Pushbutton debounce delay in seconds.

# Pushbutton config

pushbuttonPin = 10  # arduino pin number

# ULTRASONIC SENSOR CONFIG

trigPin = 19
echoPin = 18

# 7 SEGMENT REGISTER PINS 

dsPin = 2   # Data Pin # 7seg 
stcpPin = 3  # Latch Pin # 7seg
shcpPin = 4 # Clock Pin # 7seg

# 7 SEGMENT DIGIT PINS 

digitOne = 6 # 7seg
digitTwo = 7 # 7seg
digitThree = 8 # 7seg
digitFour = 9 # 7seg


# TRAFFIC LIGHT LED REGISTER PINS 

ds2Pin = 13   # Data Pin # traffic lights
stcp2Pin = 12  # Latch Pin # traffic lights
shcp2Pin = 11 # Clock Pin # traffic lights




def boardsetup():

    # Clear the shift registers.
    clear_register(stcpPin, shcpPin, dsPin)
    clear_register(stcp2Pin, shcp2Pin, ds2Pin)

    #Init pins for pushbutton
    board.set_pin_mode_digital_input_pullup(pushbuttonPin, callback=pushbutton_callback)

    # Init pins for ultrasonic sensor
    board.set_pin_mode_sonar(trigPin, echoPin, timeout=20000)

    # Init pins for shift register for traffic light leds
    board.set_pin_mode_digital_output(ds2Pin)
    board.set_pin_mode_digital_output(shcp2Pin)
    board.set_pin_mode_digital_output(stcp2Pin)

    # Init pins for shift register for seven segment display
    board.set_pin_mode_digital_output(dsPin)
    board.set_pin_mode_digital_output(shcpPin)
    board.set_pin_mode_digital_output(stcpPin)

    # Init pins for seven segment display
    board.set_pin_mode_digital_output(digitOne)
    board.set_pin_mode_digital_output(digitTwo)
    board.set_pin_mode_digital_output(digitThree)
    board.set_pin_mode_digital_output(digitFour)
    board.digital_write(digitOne, 1)
    board.digital_write(digitTwo, 1)
    board.digital_write(digitThree, 1)
    board.digital_write(digitFour, 1)
    


def setup():
    """
    The setup function that initializes the program by displaying the service menu and setting the user's choice.

    The function calls the `display_service_menu()` function to display the service menu and prompt the user to select an operating mode.
    The user's choice is then assigned to the global variable `userChoice`.

    After setting the `userChoice` variable, the function returns, allowing the program to proceed with the selected operating mode.
    Parameters:
        No parameters
    Returns:
        None

    """

    global userChoice
    userChoice = display_service_menu()


# Control Subsystem
def loop():

    """
    The main loop function that controls the execution of different operating modes based on user choice.

    The function enters an infinite loop and checks the value of the `userChoice` variable to determine which operating mode to execute:

    - If `userChoice` is 3, the function calls the `maintenance_adjustment_mode()` function to enter the maintenance adjustment mode.
    - If `userChoice` is 2, the function calls the `data_observation_mode()` function to enter the data observation mode.
    - If `userChoice` is any other value (default), the function calls the `normal_operation_mode()` function to enter the normal operation mode.

    The loop continues indefinitely until the program is manually terminated or an exception occurs.
    Parameters:
        No parameters
    Returns:
        None

    """

    while True:
        if userChoice == 3:
            maintenance_adjustment_mode()
        elif userChoice == 2:
            data_observation_mode()
        else:
            normal_operation_mode()


# Below will be all the different subsystems for the project.

# Service Subsystem
def display_service_menu():

    """
    Displays the service menu and prompts the user to select an operating mode.

    The function displays a welcome message and presents the user with three operating mode options:
    1. Normal Operation Mode
    2. Data Observation Mode
    3. Maintenance Adjustment Mode

    The user is prompted to enter the number corresponding to their desired operating mode.

    If the user enters a valid option (1, 2, or 3), the function returns the selected option as an integer.

    If the user enters an invalid option, the function displays an error message and prompts the user to enter a valid option again.

    If the user enters an invalid input, the function displays an error message and prompts the user to enter a valid integer.

    If a keyboard interrupt (Ctrl+C) occurs during the execution of this function, it prints a newline character, displays an
    "Exiting the program..." message, and terminates the program using `exit()`.

    Returns:
        int: The selected operating mode option (1, 2, or 3).


    """

    print(f"Welcome!\n" 
          "Please select which operating mode you want to boot into.\n\n"
          "1.Normal Operation Mode\n"
          "2.Data Observation Mode\n"
          "3.Maintenance Adjustment Mode\n"
          )
    
    while True:
        try:
            global userChoice
            userChoice = int(input("Option: "))
            if userChoice == 1 or userChoice == 2 or userChoice == 3:
                return userChoice
            else:
                print("Please enter a valid option!")
        except ValueError:
            print("Please enter a valid integer.")
        except KeyboardInterrupt:
            print("\n")
            print("Exiting the program... ")
            clear_register(stcpPin,shcpPin, dsPin)
            clear_register(stcp2Pin,shcp2Pin, ds2Pin)
            board.shutdown()
            exit()

def maintenance_adjustment_mode():

    """
    Enters the maintenance adjustment mode to modify system parameters.

    The function prompts the user to enter a pin for authentication. If the entered pin matches the `settingPin`,
    the user gains access to the maintenance mode. Otherwise, an "Incorrect pin" message is displayed, and the user
    is prompted to enter the pin again.

    Once authenticated, the function displays the available parameters that can be edited, along with their current values.
    The user is prompted to select a parameter to edit by entering the corresponding number.

    If the user selects "0" to exit the maintenance mode, the function prints "Exiting Maintenance Mode..." and returns
    to the setup menu.

    If the user selects "1" to edit the ultrasonic sensor cutoff distance, the function prompts the user to enter an
    integer value between 1 and 20 (inclusive). If the entered value is valid, the `ultraSensorCutoff` global variable
    is updated with the new value, and a confirmation message is printed. If the entered value is invalid, an appropriate
    error message is displayed, and the user is prompted to enter a valid value again.

    If a keyboard interrupt (Ctrl+C) occurs during the execution of this function, it prints a newline character and
    returns to the setup menu.
    Parameters:
        No Parameters
    Returns:
        None


    """

    global ultraSensorCutoff
    global settingPin
    global stageOneDuration
    global stageTwoDuration
    global stageThreeDuration
    global stageFourDuration
    global stageFiveDuration
    global stageSixDuration
    userAuth = 0
    # print(sevenSeg("HAL1")) # Remove this later.
    print("Entered Maintenance Mode")
    try:
        while True:
            # Input validation for user pin.
            while userAuth == 0:
                userPin = int(input("Please enter pin: "))
                if userPin == settingPin:
                    print("Gained access!\n")
                    userAuth = 1
                else:
                    print("Incorrect pin!\n")
            # Main logic  for maintenance adjustment mode
            print("Available parameters\n"
                 f"1. Ultrasound Cutoff Distance: {ultraSensorCutoff}cm\n"
                 f"2. User PIN: {settingPin}\n"
                 f"3. Stage Interval Timing\n"
                 f"4. Seven Segment Display\n"
                 f"0. Exit Maintenance Mode\n")
            userEdit = int(input("Please select which parameter you want to edit: "))
            if userEdit == 0:
                print("Exiting Maintenance Mode...")
                setup()
                return
            if userEdit == 1:
                print("Editing the ultrasonic sensor cutoff distance...\n "
                    "Please select an integer from 1 - 20 cm\n"
                     )
                while True:
                    try:
                        userEditValue = int(input("Editing: "))
                        if 1 <= userEditValue <= 20:
                            ultraSensorCutoff = userEditValue
                            print(f"Ultrasound cutoff distance set to: {ultraSensorCutoff}cm")
                            print("\n")
                            break
                        else:
                            print("Please enter an integer between 1 and 20.")        
                    except ValueError:
                        print("Please enter a valid integer.")
            if userEdit == 2:
                print("Please enter a new 4 digit PIN.")
                while True:
                    try:
                        userEditValue = int(input("New PIN: "))
                        if len(str(userEditValue)) == 4:
                            settingPin = userEditValue
                            print(f"New PIN set to: {settingPin}")
                            print("\n")
                            break
                        else:
                            print("PIN can only be 4 digits long.")        
                    except ValueError:
                        print("Please enter a valid integer.")
            if userEdit == 3:
                print("Current stage duration intervals:\n"
                      f"Stage One  : {stageOneDuration}\n"
                      f"Stage Two  : {stageTwoDuration}\n"
                      f"Stage Three: {stageThreeDuration}\n"
                      f"Stage Four : {stageFourDuration}\n"
                      f"Stage Five : {stageFiveDuration}\n"
                      f"Stage Six  : {stageSixDuration}\n"
                      "Note: You can press Ctrl+C to go back once desired parameters are edited.")
                while True:
                    try:
                        userEditValueOne = int(input("New Stage One duration: "))
                        if userEditValueOne > 0 and userEditValueOne % 3 == 0:
                            stageOneDuration = userEditValueOne
                            print(f"New Stage One duration set to: {stageOneDuration}")
                            break
                        else:
                            print("Please enter a positive integer that is a multiple of 3.")
                    except ValueError:
                        print("Please enter a valid integer.")

                while True:
                    try:
                        userEditValueTwo = int(input("New Stage Two duration: "))
                        if userEditValueTwo > 0 and userEditValueTwo % 3 == 0:
                            stageTwoDuration = userEditValueTwo
                            print(f"New Stage Two duration set to: {stageTwoDuration}")
                            break
                        else:
                            print("Please enter a positive integer that is a multiple of 3.")
                    except ValueError:
                        print("Please enter a valid integer.")

                while True:
                    try:
                        userEditValueThree = int(input("New Stage Three duration: "))
                        if userEditValueThree > 0 and userEditValueThree % 3 == 0:
                            stageThreeDuration = userEditValueThree
                            print(f"New Stage Three duration set to: {stageThreeDuration}")
                            break
                        else:
                            print("Please enter a positive integer that is a multiple of 3.")
                    except ValueError:
                        print("Please enter a valid integer.")

                while True:
                    try:
                        userEditValueFour = int(input("New Stage Four duration: "))
                        if userEditValueFour > 0 and userEditValueFour % 3 == 0:
                            stageFourDuration = userEditValueFour
                            print(f"New Stage Four duration set to: {stageFourDuration}")
                            break
                        else:
                            print("Please enter a positive integer that is a multiple of 3.")
                    except ValueError:
                        print("Please enter a valid integer.")

                while True:
                    try:
                        userEditValueFive = int(input("New Stage Five duration: "))
                        if userEditValueFive > 0 and userEditValueFive % 3 == 0:
                            stageFiveDuration = userEditValueFive
                            print(f"New Stage Five duration set to: {stageFiveDuration}")
                            break
                        else:
                            print("Please enter a positive integer that is a multiple of 3.")
                    except ValueError:
                        print("Please enter a valid integer.")

                while True:
                    try:
                        userEditValueSix = int(input("New Stage Six duration: "))
                        if userEditValueSix > 0 and userEditValueSix % 3 == 0:
                            stageSixDuration = userEditValueSix
                            print(f"New Stage Six duration set to: {stageSixDuration}")
                            break
                        else:
                            print("Please enter a positive integer that is a multiple of 3.")
                    except ValueError:
                        print("Please enter a valid integer.")

            if userEdit == 4:
                print("Please enter a message you want to show on the seven segment.\n"
                      "Message should contain valid characters\n"
                      "Digits: 0 to 9\n"
                      "Uppercase letters: A-Z\n"
                      "Lowercase letters: a-z\n"
                      "Space character\n"
                      "Note: Invalid characters will be replaced with a space instead\n"
                      "Note: Maximum output length of message will be 4 alphanumeric characters\n")
                while True:
                    try:
                        userMessage = input("Message: ")
                        print("Press Ctrl+C to go back.")
                        parsedUserMessage = seven_segment(userMessage)
                        while True:
                            for i in range(len(parsedUserMessage)):
                                write_to_seg(i, parsedUserMessage[i], stcpPin, shcpPin, dsPin)     
                    except ValueError:
                        print("Please enter a valid integer.")
                    except KeyboardInterrupt:
                        print("\n")
                        break        
            else:
                print("Please entered a valid option!")            
    except ValueError:
        print("Please enter a valid integer.\n")
    except KeyboardInterrupt:
        print("\n")
        setup()

# 7 SEG HELPER FUCNTIONS

def write_to_seg(digitIndex, digitData, latchPin, clockPin, serialInputPin):
    reverseDigitData = reversed(digitData)
    turn_off_digits()
    shift_out(reverseDigitData, latchPin, clockPin, serialInputPin)
    set_digit_pin(digitIndex)

def turn_off_digits():
    board.digital_write(digitOne, 1)
    board.digital_write(digitTwo, 1)
    board.digital_write(digitThree, 1)
    board.digital_write(digitFour, 1)

def set_digit_pin(digitIndex):
    if digitIndex == 0:
        board.digital_write(digitOne, 0)
    elif digitIndex == 1:
        board.digital_write(digitTwo, 0)
    elif digitIndex == 2:
        board.digital_write(digitThree, 0)
    elif digitIndex == 3:
        board.digital_write(digitFour, 0)



# 7 SEG HELPER FUNCTION END

def normal_operation_mode():

    """
    Enters the normal operation mode to manage traffic stages and measure distance.

    The function starts by recording the current time using `time.time()` and stores it in the `startTime` variable.
    It then calls the `traffic_stage_manager` function to manage the traffic stages and perform distance measurements.

    After the `traffic_stage_manager` function completes, the function records the end time using `time.time()` and
    stores it in the `endTime` variable. It calculates the duration of the polling loop by subtracting `startTime`
    from `endTime` and prints the result in seconds.

    If a keyboard interrupt occurs during the execution of this function, it prints a newline character
    and returns to the setup menu.

    Returns:
        None

    """

    global distanceMeasured
    try:
        # startTime = time.time()
        traffic_stage_manager()
        # endTime = time.time()
       # print(f"Time for one normal operation mode cycle: {endTime - startTime}sec")
    except KeyboardInterrupt:
        print("\n")
        setup()



def data_observation_mode():

    """
    Enters the data observation mode to display a graph of distance measurements.

    The function checks if there are sufficient distance measurements (at least 20) available in the global
    `distanceMeasured` list. If there is insufficient data, it prints a message indicating that and returns to
    the setup menu after a 1.5-second delay.

    If there is sufficient data, the function prints a message indicating that the graph is being displayed and
    calls the `traffic_graph_plot` function to plot the graph of distance measurements. After displaying the graph,
    it returns to the setup menu.

    If a keyboard interrupt (Ctrl+C) occurs during the execution of this function, it prints a newline character
    and returns to the setup menu.

    Returns:
        None

    """

    global distanceMeasured
   #  print(sevenSeg("HAL1")) # Remove this later.
    print("Entered Data Observation Mode")
    try:
        if len(distanceMeasured) < 20:
            print("Insufficient data is available for the plot. Returning to the menu\n")
            time.sleep(1.5)
            setup()
            return
        else:
            print("Displaying graph!")
            traffic_graph_plot(distanceMeasured)
            setup()
            return
    except KeyboardInterrupt:
        print("\n")
        setup()

def traffic_graph_plot(distanceMeasured):

    """
    Plots a graph of the distance measurements over time.

    The function takes a list of distance measurements as input and creates a graph using the matplotlib library.
    The graph shows the distance measurements on the y-axis and the corresponding time points on the x-axis.
    The x-axis represents the time in seconds, assuming each measurement is taken at regular intervals.
    The y-axis represents the distance from the car in centimeters.

    Parameters:
        distanceMeasured: A list of distance measurements in centimeters.

    Returns:
        None

    """

    plt.figure(figsize=(8, 6))
    plt.plot(distanceMeasured, marker='x')
    plt.xlabel("Time (seconds)")
    plt.ylabel("Distance from car (cm)")
    plt.xlim(0, len(distanceMeasured))  
    plt.ylim(0, max(distanceMeasured) + 10)  
    plt.legend(['Traffic Distance'])  
    plt.show(block=True)  

def read_sensor():

    """
    Reads the distance to the nearest object using an ultrasonic sensor.

    The function simulates reading from an ultrasonic sensor by generating random distance values
    between 1 and 20 centimeters. It takes four readings with a 0.25 second delay between each reading.
    The average of the four readings is calculated and returned as the final distance measurement.

    Returns:
        float: The average distance to the nearest object in centimeters, calculated from four sensor readings.

    """

    rawDistances = []
    for _ in range(4):
        sensorReading , _ = board.sonar_read(trigPin)
        rawDistances.append(sensorReading)
        time.sleep(0.25) # Time between sensor polls

    # print(rawDistances)   
    averageDistance = sum(rawDistances) / 4
    # print(f"Average ultrasonic sensor reading: {averageDistance}cm")
    return averageDistance

def seven_segment(inputMessage):

    """
    Converts a message string into a list of binary strings representing the state of a seven-segment display.

    The function takes a message string as input and returns a list of binary strings. Each binary string
    corresponds to a character in the message and represents the state of the seven segments needed to display
    that character on a seven-segment display. The function uses a lookup dictionary to map each character to
    its corresponding binary representation. If a character is not found in the lookup dictionary, a space
    character is used instead. The function only considers the first four characters of the message string.

    Parameters:
        message: The message to be displayed on the seven-segment display.

    Returns:
        List: A list of binary strings representing the state of the seven-segment display for each character
              in the message. Each binary string is 7 characters long, where '1' represents an active segment
              and '0' represents an inactive segment.

    """

    lookupDictionary = {
        "0": "1111110",
        "1": "0110000",
        "2": "1101101",
        "3": "1111001",
        "4": "0110011",
        "5": "1011011",
        "6": "1011111",
        "7": "1110000",
        "8": "1111111",
        "9": "1111011",
        "A": "1110111",
        "B": "0011111",
        "b": "0011111",
        "C": "1001110",
        "c": "1001110",
        "d": "0111101",
        "D": "0111101",
        "E": "1001111",
        "F": "1000111",
        "g": "1011110",
        "G": "1011110",
        "H": "0110111",
        "h": "0110111",
        "i": "0110000",
        "I": "0110000",
        "j": "1111100",
        "J": "1111100",
        "K": "0100111",
        "L": "0001110",
        "l": "0001110",
        "M": "1010101",
        "n": "0010111",
        "N": "0010111",
        "O": "1111110",
        "o": "1111110",
        "P": "1100111",
        "p": "1100111",
        "q": "1110011",
        "Q": "1110011",
        "R": "0000101",
        "r": "0000101",
        "S": "1011011",
        "T": "0001111",
        "t": "0001111",
        "V": "0111110",
        "U": "0111110",
        "W": "1111000",
        "X": "0110111",
        "u": "0111110",
        "y": "0111011",
        "Y": "0111011",
        "Z": "1101101",
        " ": "0000000"
    }
    binaryMesasge = []
    for messageChar in inputMessage[:4]: # This only takes a string slice of the first 4 charecters in the message since that's the max amount of charecters which can be displayed.
        if messageChar in lookupDictionary:
            binaryMesasge.append(lookupDictionary[messageChar])
        else:
            binaryMesasge.append(lookupDictionary[" "])

    return binaryMesasge

# def push_button():

#     """
#     Used to record the number of times the pedestrian push button is triggered when pressed, 
#     indicating the presence of pedestrians. The pedestrian push button triggers a single 
#     clean signal (de-bounced) when pressed.
#         Paramters:
#             function has no parameters
#         Returns:
#             function has no returns
#     """

#     global pushButtonStage1
#     global pushButtonStage2
#     flag = True
#     while True: 
#         buttonPressed = random.choice([True,False])
#         if buttonPressed == True and flag == True:
#             flag == False
#             if currentStage == 0:
#                 pushButtonStage1.append(1)
#             if currentStage == 1:
#                 pushButtonStage2.append(1)
#             break
#         else:
#             flag = True
#             break

# PUSHBUTTON CODE

def pushbutton_callback(callbackData):
    global lastDetectedChange
    global bouncyTimer
    global currentStage
    global pedestrianCounter

    timeNow = callbackData[3]

    if timeNow - lastDetectedChange > bouncyTimer:
        if (currentStage == 0 or currentStage == 1) and callbackData[2] == 0:
                pedestrianCounter += 1
                lastDetectedChange = timeNow

# PUSHBUTTON CODE END

## LIGHT CONTROL HELPER FUNCTIONS

def shift_out(shiftData, latchPin, clockPin, serialInputPin):
    board.digital_write(latchPin, 0)
    for shiftBit in (shiftData):
        board.digital_write(clockPin, 0)
        board.digital_write(serialInputPin, int(shiftBit))
        board.digital_write(clockPin, 1)
    board.digital_write(latchPin, 1)
    board.digital_write(latchPin, 0)

def clear_register(latchPin, clockPin, serialInputPin):
    shift_out("00000000", latchPin, clockPin, serialInputPin)

## LIGHT CONTROL HELPER FUNCTIONS END

def traffic_stage_manager():
    global stageOneDuration
    global stageTwoDuration
    global stageThreeDuration
    global stageFourDuration
    global stageFiveDuration
    global stageSixDuration

    """
    Used to control the state of traffic lights. Also used to display information about the current stage of traffic operations, the distance to the nearest vehicle in two decimal cm readings, and the presence of pedestrians as the total number of presses on the console.
        Paramters:
            function has no parameters
        Returns:
            function has no returns
    """

    #4. create a list to hold dictionaries containing information about the duration, main road traffic lights, side road traffic lights, and pedestrian lights of each traffic stage
    trafficOperation = [
        {
            "duration": stageOneDuration,
            "mainRoadLights": "Green",
            "sideRoadLights": "Red",
            "pedestrianLights": "Red",
            "lightTruthTable" : "10001100"
        },

        {
            "duration": stageTwoDuration,
            "mainRoadLights": "Yellow",
            "sideRoadLights": "Red",
            "pedestrianLights": "Red",
            "lightTruthTable" : "10001010"
        },

        {
            "duration": stageThreeDuration,
            "mainRoadLights": "Red",
            "sideRoadLights": "Red",
            "pedestrianLights": "Red",
            "lightTruthTable" : "10001001"
        },

        {
            "duration": stageFourDuration,
            "mainRoadLights": "Red",
            "sideRoadLights": "Green",
            "pedestrianLights": "Green",
            "lightTruthTable" : "01100001"
        },

        {
            "duration": stageFiveDuration,
            "mainRoadLights": "Red",
            "sideRoadLights": "Yellow",
            "pedestrianLights": "Flashing Green at 2-3 Hz",
            "lightTruthTable" : "01010001",
            "lightTruthTableOff" : "00010001" 
        },

        {
            "duration": stageSixDuration,
            "mainRoadLights": "Red",
            "sideRoadLights": "Red",
            "pedestrianLights": "Red",
            "lightTruthTable" : "10001001"
        }
    ]

    #5. initialise currentStage and pedestrianCount variables, set them equal to zero
    global currentStage
    global distanceMeasured
    global pedestrianCounter
    
    #6. loop to control the state of traffic lights and display information about the current traffic stage operations on the console
    while True:
            
            try: 
                #7. displays the current stage of traffic operation on the console once per stage in the current sequence
                print(f"Current Stage: Stage {currentStage + 1}\n")
                print(f'Main Road Traffic Lights: {trafficOperation[currentStage]["mainRoadLights"]}')
                print(f'Side Road Traffic Lights: {trafficOperation[currentStage]["sideRoadLights"]}')
                print(f'Pedestrian Lights: {trafficOperation[currentStage]["pedestrianLights"]}\n')
                 
                shift_out(trafficOperation[currentStage]["lightTruthTable"], stcp2Pin, shcp2Pin, ds2Pin)
                

                #8. displays presence of pedestrians on the console as the total number of presses at the beginning of stage three. before stage three (stages one & two), the amount of state changes from the pushbutton is retrieved and stored inside the variable pedestrianCount
                if currentStage == 0:
                    pedestrianCounter = 0
                if currentStage == 2:
                    print(f"Total number of pedestrian presses: {pedestrianCounter}\n")

                #9. create a variable stageEndTime to store the end time of the current traffic stage in the current sequence
                stageDuration = trafficOperation[currentStage]["duration"]
                stageEndTime = time.time() + stageDuration



                # Stage 5 blinking logic
                if currentStage == 4:
                    stageCycle = 0
                    sensorPollInterval = 0   
                    blinkDelay = 0.1
                    lastPollTime = time.time()
                    while stageEndTime > time.time():
                        startTime = time.time()
                        if stageCycle % 2 == 0:
                            for i in range(8):
                                if i % 2 == 0:
                                    shift_out(trafficOperation[currentStage]["lightTruthTable"], stcp2Pin, shcp2Pin, ds2Pin)
                                else:
                                    shift_out(trafficOperation[currentStage]["lightTruthTableOff"], stcp2Pin, shcp2Pin, ds2Pin)
                                time.sleep(blinkDelay)
                        stageCycle += 1
                        
                        #print(stageCycle)
                        if time.time() - lastPollTime >= sensorPollInterval:
                            sensorPollInterval = 0
                            distanceMeasured.append(read_sensor())
                            if len(distanceMeasured) == 21:
                                distanceMeasured.pop(0)
                            if len(distanceMeasured) >= 2:
                                carVelocity = distanceMeasured[-2] - distanceMeasured[-1] / 1.5
                                print(f"Vehicle velocity: {carVelocity:.2f} cm/s")
            
                            print(f"Distance to nearest vehicle: {distanceMeasured[-1]} cm\n")
            
                            lastPollTime = time.time()

                        time.sleep(blinkDelay)
                        if time.time() >= stageEndTime:
                                endTime = time.time()
                                stageCycle = 0
                                break
                        
                        endTime = time.time()
                        #print(f'Blinking time is {endTime - startTime}')

                while stageEndTime > time.time():
                        startTime = time.time()
                        distanceMeasured.append(read_sensor())
                        # So that distanceMeasured only contains the latest data.
                        if len(distanceMeasured) == 21:
                            distanceMeasured.pop(0)
                        # Calculates vehicle velocity based on the distance <- need to work on  this a bit more
                        if len(distanceMeasured) >= 2:
                            carVelocity = distanceMeasured[-2] - distanceMeasured[-1] / 1.5
                            print(f"Vehicle velocity: {carVelocity:.2f} cm/s")

                        print(f"Distance to nearest vehicle: {distanceMeasured[-1]} cm\n")
                        subsequentDisplay = min(0.5, stageEndTime - time.time())
                        if subsequentDisplay < 0:
                            endTime = time.time()
                            print(f'Sensor polling cycle: {(endTime - startTime):.2f} seconds')
                            continue
                        time.sleep(subsequentDisplay)
                        endTime = time.time()
                        print(f'Sensor polling cycle: {(endTime - startTime):.2f} seconds')
                
                #11. line break between two traffic stages 
                print ("\n\n\n")

                #12. update the value of currentStage to proceed to the next traffic stage in the current sequence
                currentStage += 1
        
                #13. restart from stage one after stage six. reset the total number of pedestrain presses every time the traffic operation sequence restarts at stage one
                if currentStage % len(trafficOperation) == 0:
                    currentStage = 0
                    pedestrianCounter = 0

            #14. ctrl+c to break from the loop and return to the display service menu function
            except KeyboardInterrupt:
                print("\n")
                setup()
                return


if __name__ == '__main__':
    boardsetup()
    setup()
    loop()


