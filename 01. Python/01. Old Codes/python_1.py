import serial
import time

# Keep track of the previous readings
prev_sensor_0 = None
prev_sensor_1 = None
sensor_0_counter = 0
sensor_1_counter = 0

arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=.1)

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def send_command_to_arduino(command):
    arduino.write((command + "\n").encode())
    print(f"{BLUE}PYTHON => Sent command to Arduino: {command}")
    
    while True:
        if arduino.in_waiting > 0:
            line = arduino.readline().decode('ISO-8859-1').rstrip()
            print(f"{BLUE}PYTHON => Raw data received: {line}{RESET}")
            if line.startswith("LED_"):
                print(f"{BLUE}PYTHON => Confirmation from Arduino: {line}{RESET}")
                break

def read_from_arduino():
    global prev_sensor_0, prev_sensor_1, sensor_0_counter, sensor_1_counter
    if arduino.in_waiting > 0:
        line = arduino.readline().decode('ISO-8859-1').rstrip()
        print(f"{BLUE}Received from Arduino: {line}{RESET}")

        if line.startswith("SENSOR_") and ":" in line:
            print(f"{GREEN}#########################################################{RESET}")
            print(line)
            print(f"{GREEN}#########################################################{RESET}")

            parts = line.split(":")
            sensor_index = int(parts[0].split("_")[1])  # Extract sensor index
            distance = float(parts[1].strip())  # Extract distance

            # Handle SENSOR_0 data
            if sensor_index == 0:
                if distance < 5:
                    print(f"{GREEN}PYTHON => Vehicle detected by sensor {sensor_index} (distance: {distance} cm){RESET}")
                    send_command_to_arduino(f"green{sensor_index}")
                elif distance < 10:
                    print(f"{YELLOW}PYTHON => Vehicle approaching sensor {sensor_index} (distance: {distance} cm){RESET}")
                    send_command_to_arduino(f"yellow{sensor_index}")
                else:
                    print(f"{RED}PYTHON => No vehicle detected by sensor {sensor_index} (distance: {distance} cm){RESET}")
                    send_command_to_arduino(f"red{sensor_index}")
                
                prev_sensor_0 = distance  # Update the previous sensor distance

            # Handle SENSOR_1 data
            elif sensor_index == 1:
                if distance < 5:
                    print(f"{GREEN}PYTHON => Vehicle detected by sensor {sensor_index} (distance: {distance} cm){RESET}")
                    send_command_to_arduino(f"green{sensor_index}")
                elif distance < 10:
                    print(f"{YELLOW}PYTHON => Vehicle approaching sensor {sensor_index} (distance: {distance} cm){RESET}")
                    send_command_to_arduino(f"yellow{sensor_index}")
                else:
                    print(f"{RED}PYTHON => No vehicle detected by sensor {sensor_index} (distance: {distance} cm){RESET}")
                    send_command_to_arduino(f"red{sensor_index}")
                
                prev_sensor_1 = distance  # Update the previous sensor distance

            else:
                print(f"{RED}Unexpected sensor index: {sensor_index}{RESET}")
                time.sleep(0.1)  # Small delay to prevent continuous overflow

# Main loop
while True:
    read_from_arduino()
    time.sleep(0.2)
