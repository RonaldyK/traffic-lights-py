import time
import matplotlib.pyplot as plt
import math
import random

userChoice = 0
settingPin = 1234
ultraSensorCutoff = 20
distanceMeasured = []

def setup():
    global userChoice
    userChoice = display_service_menu()


# Control Subsystem
def loop():
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
    global ultraSensorCutoff
    userAuth = 0
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
                  "0. Exit Maintenance Mode\n")
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
                            break
                        else:
                            print("Please enter an integer between 1 and 20.")        
                    except ValueError:
                        print("Please enter a valid integer.")    
    except ValueError:
        print("Please enter a valid integer.")
    except KeyboardInterrupt:
        print("\n")
        setup()



def normal_operation_mode():
    try:
        global distanceMeasured
        startTime = time.time()
        print("I'm in normal op mode")
        distanceMeasured.append(read_sensor())
        print(f"Distance to nearest vehicle: {distanceMeasured[-1]}cm")
        endTime = time.time()
        print(f"Polling loop time: {endTime - startTime}sec")
    except KeyboardInterrupt:
        print("\n")
        setup()



def data_observation_mode():
    global distanceMeasured
    try:
        print("I'm in data op mode")
        if len(distanceMeasured) < 20:
            print("Insufficient data is available for the plot. Returning to the menu\n")
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
    plt.figure(figsize=(8, 6))
    plt.plot(distanceMeasured, marker='x')
    plt.xlabel("Time (seconds)")
    plt.ylabel("Distance from car (cm)")
    plt.xlim(0, len(distanceMeasured))  
    plt.ylim(0, max(distanceMeasured) + 10)  
    plt.legend(['Traffic Distance'])  
    plt.show(block=True)  

def read_sensor():
    rawDistances = []
    for i in range(4):
        sensorReading = random.randint(1, 20)
        rawDistances.append(sensorReading)
        time.sleep(0.25)

    print(rawDistances)   
    averageDistance = sum(rawDistances) / 4
    # print(f"Average ultrasonic sensor reading: {averageDistance}cm")
    return averageDistance

def sevenSeg(message):
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
    for char in message:
        if char in lookupDictionary:
            binaryMesasge.append(lookupDictionary[char])
        else:
            binaryMesasge.append(lookupDictionary[" "])

    return binaryMesasge


if __name__ == '__main__':
    setup()
    loop()


