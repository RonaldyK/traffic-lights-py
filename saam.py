############################################################
#                 Monash University Malaysia               #
#                           M2                             #
#                    Rafghaan Mohamed Ali                  #
#                      Date: 4/3/2024                      #
############################################################
import time
import matplotlib.pyplot as plt
import math
import random

userChoice = 0
settingPin = 1234
ultraSensorCutoff = 20
distanceMeasured = []

def setup():

    """
    The setup function that initializes the program by displaying the service menu and setting the user's choice.

    The function calls the `display_service_menu()` function to display the service menu and prompt the user to select an operating mode.
    The user's choice is then assigned to the global variable `userChoice`.

    After setting the `userChoice` variable, the function returns, allowing the program to proceed with the selected operating mode.

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
          "2.Data Observartion Mode\n"
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

    Returns:
        None


    """

    global ultraSensorCutoff
    global settingPin
    userAuth = 0
    print(sevenSeg("HAL1")) # Remove this later.
    try:
        while True:
            print("Entered Maintenance Mode")
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
            else:
                print("Please entered a valid option!")            
    except ValueError:
        print("Please enter a valid integer.\n")
    except KeyboardInterrupt:
        print("\n")
        setup()



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
        startTime = time.time()
        traffic_stage_manager()
        endTime = time.time()
        print(f"Time for one normal operation mode cycle: {endTime - startTime}sec")
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
    print(sevenSeg("HAL1")) # Remove this later.
    try:
        print("I'm in data op mode")
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
        sensorReading = random.randint(2, 400)
        rawDistances.append(sensorReading)
        time.sleep(0.25) # Time between sensor polls

    # print(rawDistances)   
    averageDistance = sum(rawDistances) / 4
    # print(f"Average ultrasonic sensor reading: {averageDistance}cm")
    return averageDistance

def sevenSeg(message):

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
        "b": "0011111",
        "C": "1001110",
        "c": "0111101",
        "d": "1001111",
        "E": "1000111",
        "F": "1011110",
        "g": "0110111",
        "G": "0110000",
        "H": "0111100",
        "h": "1010111",
        "i": "0001110",
        "I": "1010100",
        "j": "1110110",
        "L": "1111110",
        "l": "1100111",
        "n": "1101011",
        "N": "1100110",
        "O": "1011011",
        "o": "0001111",
        "p": "0111110",
        "q": "0111011",
        "r": "1101100",
        "S": "0000001",
        "t": "0001000",
        "U": "0000000",
        "u": "0001001",
        "y": "0000001",
        " ": "0000000"
    }
    binaryMesasge = []
    for char in message[:4]: # This only takes a string slice of the first 4 charecters in the message since that's the max amount of charecters which can be displayed.
        if char in lookupDictionary:
            binaryMesasge.append(lookupDictionary[char])
        else:
            binaryMesasge.append(lookupDictionary[" "])

    return binaryMesasge

def traffic_stage_manager():
    
    """
    Used to control the state of traffic lights. Also used to display information about the current stage of traffic operations, the distance to the nearest vehicle in two decimal cm readings, and the presence of pedestrians as the total number of presses on the console.
        Paramters:
            function has no parameters
        Returns:
            function has no returns
    """

    #4. create a list to hold dictionaries containing information about the duration, main road traffic lights, side road traffic lights, and pedestrian lights of each traffic stage
    trafficOperation = [
        {"duration": 30,
        "mainRoadLights": "Green",
        "sideRoadLights": "Red",
        "pedestrianLights": "Red"
        },

        {"duration": 3,
        "mainRoadLights": "Yellow",
        "sideRoadLights": "Red",
        "pedestrianLights": "Red"
        },

        {"duration": 3,
        "mainRoadLights": "Red",
        "sideRoadLights": "Red",
        "pedestrianLights": "Red"
        },

        {"duration": 30,
        "mainRoadLights": "Red",
        "sideRoadLights": "Green",
        "pedestrianLights": "Green"
        },

        {"duration": 3,
        "mainRoadLights": "Red",
        "sideRoadLights": "Yellow",
        "pedestrianLights": "Flashing Green at 2-3 Hz"
        },

        {"duration": 3,
        "mainRoadLights": "Red",
        "sideRoadLights": "Red",
        "pedestrianLights": "Red"
        }
    ]

    #5. initialise currentStage and pedestrianCount variables, set them equal to zero
    currentStage = 0
    pedestrianCount = 0
    global distanceMeasured
    
    #6. loop to control the state of traffic lights and display information about the current traffic stage operations on the console
    while True:
            
            try: 
                #7. displays the current stage of traffic operation on the console once per stage in the current sequence
                print(f"Current Stage: Stage {currentStage + 1}\n")
                print(f'Main Road Traffic Lights: {trafficOperation[currentStage]["mainRoadLights"]}')
                print(f'Side Road Traffic Lights: {trafficOperation[currentStage]["sideRoadLights"]}')
                print(f'Pedestrian Lights: {trafficOperation[currentStage]["pedestrianLights"]}\n')

                #8. displays presence of pedestrians on the console as the total number of presses at the beginning of stage three. before stage three (stages one & two), the amount of state changes from the pushbutton is retrieved and stored inside the variable pedestrianCount
                if currentStage == 0:
                    pedestrianCount1 = random.randint(0,10)
                elif currentStage == 1:
                    pedestrianCount2 = random.randint(0,3)
                elif currentStage == 2:
                    pedestrianCount = pedestrianCount1 + pedestrianCount2
                    print(f"Total number of pedestrian presses: {pedestrianCount}\n")

                #9. create a variable stageEndTime to store the end time of the current traffic stage in the current sequence
                stageDuration = trafficOperation[currentStage]["duration"]
                stageEndTime = time.time() + stageDuration

                #10. loop to display the distance to the nearest vehicle in two decimal cm readings on the console, once every 1-3 seconds
                while stageEndTime > time.time():
                        startTime = time.time()
                        distanceMeasured.append(read_sensor())
                        # So that distanceMeasured only contains the latest data.
                        if len(distanceMeasured) == 21:
                            distanceMeasured.pop(0)
                        # Calculates vehicle velocity based on the distance <- need to work on  this a bit more
                        if len(distanceMeasured) > 2:
                            carVelocity = distanceMeasured[-1] - distanceMeasured[-2] / 1.5
                            print(f"Vehicle velocity: {carVelocity:.2f} cm/s")

                        print(f"Distance to nearest vehicle: {distanceMeasured[-1]}cm")
                        print(f"distanceMeasured: {distanceMeasured}") # Remove later, only for debugging
                        subsequentDisplay = min(0.5, stageEndTime - time.time())
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
                    pedestrianCount = 0

            #14. ctrl+c to break from the loop and return to the display service menu function
            except KeyboardInterrupt:
                print("\n")
                setup()
                return


if __name__ == '__main__':
    setup()
    loop()

