# arduino_sensor.py
import serial
import time

class ArduinoSensor:
    def __init__(self, port, baudrate, timeout, labels):
        self.arduino = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        self.labels = labels
        self.sensor_data = [None, None]
        self.is_reading = False
        
        # Define terminal color codes
        self.colors = {"red": "\033[91m", "green": "\033[92m", "yellow": "\033[93m", "cyan": "\033[96m", "reset": "\033[0m"}

    def send_command_to_arduino(self, command):
        self.arduino.write((command + "\n").encode())
        print(f"{self.colors['cyan']}Sent command to Arduino: {command}{self.colors['reset']}")
        
        while self.arduino.in_waiting > 0:
            line = self.arduino.readline().decode('ISO-8859-1').strip()
            if line.startswith("LED_"):
                break

    def read_from_arduino(self):
        while self.arduino.in_waiting > 0:
            line = self.arduino.readline().decode('ISO-8859-1').strip()
            print(f"{self.colors['cyan']}Received from Arduino: {line}{self.colors['reset']}")
            if line.startswith("SENSOR_"):
                self.process_line(line)

    def process_line(self, line):
        sensor_index = int(line.split(":")[0].split("_")[1])
        distance = float(line.split(":")[1].strip())
        self.sensor_data[sensor_index] = distance
        self.process_sensor_data(sensor_index, distance)

    def process_sensor_data(self, sensor_index, distance):
        color = "red" if distance >= 10 else "yellow" if distance >= 5 else "green"
        self.send_command_to_arduino(f"{color}{sensor_index}")
        self.insert_colored_text(sensor_index, f"Sensor {sensor_index}: {distance} cm, LED: {color}", color)

    def insert_colored_text(self, sensor_index, text, color):
        self.labels[sensor_index].configure(text=f"{text}\n{self.labels[sensor_index].cget('text')}", text_color=color)

    def start_reading(self, delay=0.2):
        self.is_reading = True
        while self.is_reading:
            self.read_from_arduino()
            time.sleep(delay)

    def stop_reading(self):
        self.is_reading = False

