import serial
import time
from terminal_colors import TerminalColors  # Import the ArduinoSensor class

class ArduinoSensor:
    def __init__(self, port, baudrate, timeout, labels):
        """Initialize the ArduinoSensor with labels."""
        self.arduino = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        self.labels = labels  # A list of CTkLabel widgets to display data
        self.sensor_data = [None, None]  # Store sensor data for both sensors
        self.is_reading = False  # Flag to control the reading process

    def send_command_to_arduino(self, command):
        """Send a command to the Arduino and wait for acknowledgment."""
        self.arduino.write((command + "\n").encode())
        print(f"{TerminalColors.CYAN}Sent command to Arduino: {command}{self.RESET}")

        while True:
            if self.arduino.in_waiting > 0:
                line = self.arduino.readline().decode('ISO-8859-1').rstrip()
                print(f"{TerminalColors.CYAN}Received from Arduino: {line}{self.RESET}")
                if line.startswith("LED_"):
                    break

    def read_from_arduino(self):
        """Read data from Arduino and process sensor readings."""
        if self.arduino.in_waiting > 0:
            line = self.arduino.readline().decode('ISO-8859-1').rstrip()
            print(f"{TerminalColors.CYAN}Received from Arduino: {line}{self.RESET}")

            if line.startswith("SENSOR_") and ":" in line:
                sensor_index = int(line.split(":")[0].split("_")[1])  # Extract sensor index
                distance = float(line.split(":")[1].strip())  # Extract distance

                if sensor_index < 2:  # Only process if valid sensor index (0 or 1)
                    self.sensor_data[sensor_index] = distance
                    self.process_sensor_data(sensor_index, distance)

    def process_sensor_data(self, sensor_index, distance):
        """Process and update the sensor data and LED color."""
        color = "red" if distance >= 10 else "yellow" if distance >= 5 else "green"
        self.send_command_to_arduino(f"{color}{sensor_index}")
        self.insert_colored_text(sensor_index, f"Sensor {sensor_index}: {distance} cm, LED: {color}", color)

    def insert_colored_text(self, sensor_index, text, color):
        """Insert colored text into the specific label widget based on sensor index."""
        # Get the current text in the label
        current_text = self.labels[sensor_index].cget("text")
        # Append the new colored text to the current text for that label
        new_text = f"{current_text}\n{text}"  # Prepend the new sensor data without color formatting

        # Update the text of the label with the new text
        self.labels[sensor_index].configure(text=new_text)
        
        # Set the color for the current text to only apply to the newly added line
        self.labels[sensor_index].configure(text_color=color)  # Set color for the most recent line

    def start_reading(self, delay=0.2):
        """Start reading sensor data in a background thread."""
        self.is_reading = True
        while self.is_reading:
            self.read_from_arduino()
            time.sleep(delay)

    def stop_reading(self):
        """Stop reading sensor data."""
        self.is_reading = False
        print(f"{self.BLUE}Sensor reading stopped.{self.RESET}")
