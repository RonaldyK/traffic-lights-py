import time
import matplotlib
import math
import random

userChoice = 0
settingPin = 1234
ultraSensorCutoff = 20


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
    try:
        print("Entered Maintenance Mode")
        # Input validation for user pin.
        while True:
            userPin = int(input("Please enter pin: "))
            if userPin == settingPin:
                print("Gained access!")
                break
            else:
                print("Incorrect pin!")
        # Main logic  for maintenance adjustment mode
        print("Available parameters"
              f"Ultrasound Cutoff Distance: {ultraSensorCutoff}")
    except ValueError:
        print("Please enter a valid integer.")
    except KeyboardInterrupt:
        print("\n")
        display_service_menu()



def normal_operation_mode():
    try:
        print("I'm in normal op mode")
        read_sensor()
    except KeyboardInterrupt:
        print("\n")
        display_service_menu()



def data_observation_mode():
    try:
        print("I'm in data op mode")
    except KeyboardInterrupt:
        print("\n")
        display_service_menu()

def read_sensor():
    rawDistances = []
    while True:
        sensorReading = random.randint(1, 30)
        print(sensorReading)
        if sensorReading <= ultraSensorCutoff:
            rawDistances.append(sensorReading)
        else:
            continue


        if len(rawDistances) > 4:
            rawDistances.pop(0)
        print(rawDistances)
        if len(rawDistances) == 4:    
            averageDistances = sum(rawDistances) / 4
            print(f"Average ultrasonic sensor reading: {averageDistances}cm")
            return averageDistances
        else:
            print("Insufficient data points.")
        time.sleep(2)


if __name__ == '__main__':
    setup()
    loop()


def pull_request():
    pass