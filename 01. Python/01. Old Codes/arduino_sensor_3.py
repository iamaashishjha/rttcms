import serial
import time
from terminal_colors_1 import TerminalColors  # Assuming TerminalColors is defined

class ArduinoSensor:
    def __init__(self, port, baudrate, timeout, labels):
        self.arduino = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        self.labels = labels  
        self.sensor_data = [None, None] 
        self.is_reading = False  
        
        self.colors = {"red": "\033[91m", "green": "\033[92m", "yellow": "\033[93m", "reset": "\033[0m"}

    def send_command_to_arduino(self, command):
        self.arduino.write((command + "\n").encode())
        print(f"{TerminalColors.CYAN}Sent command to Arduino: {command}{self.colors['reset']}")

    def read_from_arduino(self):
        if self.arduino.in_waiting > 0:
            line = self.arduino.readline().decode('ISO-8859-1').strip()
            print(f"{TerminalColors.CYAN}Received from Arduino: {line}{self.colors['reset']}")

            if line.startswith("SENSOR_") and ":" in line:
                sensor_index = int(line.split(":")[0].split("_")[1])  
                distance = float(line.split(":")[1].strip())  

                if sensor_index < 2:  
                    self.sensor_data[sensor_index] = distance
                    self.process_sensor_data(sensor_index, distance)

    def process_sensor_data(self, sensor_index, distance):
        color = "red" if distance >= 10 else "yellow" if distance >= 5 else "green"
        self.send_command_to_arduino(f"{color}{sensor_index}")
        self.insert_colored_text(sensor_index, f"Sensor {sensor_index}: {distance} cm, LED: {color}", color)

    def insert_colored_text(self, sensor_index, text, color):
        current_text = self.labels[sensor_index].cget("text")
        new_text = f"{current_text}\n{text}"  
        self.labels[sensor_index].configure(text=new_text, text_color=self.colors[color])

    def start_reading(self, delay=0.2):
        self.is_reading = True
        while self.is_reading:
            self.read_from_arduino()
            time.sleep(delay)

    def stop_reading(self):
        self.is_reading = False
        print(f"{self.colors['blue']}Sensor reading stopped.{self.colors['reset']}")
