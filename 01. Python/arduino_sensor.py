import serial
import time
import datetime  # Import datetime for adding timestamps
import logging
from terminal_colors import TerminalColors as Colors  # Import the ArduinoSensor class


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ArduinoSensor:
    def __init__(self, port, baudrate, timeout, labels):
        """Initialize the ArduinoSensor with labels."""
        self.arduino = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        self.labels = labels  # A list of CTkLabel widgets to display data
        self.sensor_data = [None, None]  # Store sensor data for both sensors
        self.is_reading = False  # Flag to control the reading process
        self.sensor_counter = 0  # Counter to alternate between the two sensors

    def send_command_to_arduino(self, command):
        """Send a command to the Arduino."""
        self.arduino.write((command + "\n").encode())
        logger.info(f"Sent command to Arduino: {command}")  # Log the actual data

    # def send_command_to_arduino(self, command):
    #     """Send a command to the Arduino and wait for acknowledgment."""
    #     self.arduino.write((command + "\n").encode())
    #     logger.info(f"Sent command to Arduino: {command}")  # Log the actual data
    #     while True:
    #         if self.arduino.in_waiting > 0:
    #             line = self.arduino.readline().decode('ISO-8859-1').rstrip()
    #             logger.info(f"Received from Arduino: {line}")  # Log the actual data
    #             if line.startswith("LED_"):
    #                 break

    def sensor_reading_thread(self):
        """Background thread to read sensor data and update logs."""
        try:
            self.sensor.start_reading()
        except Exception as e:
            error_log = f"{Colors.RED}Error: {e}{Colors.RESET}"
            print(error_log)
            self.log_display_1.configure(text="Error occurred: Check terminal logs.")


    def read_from_arduino(self):
        """Read data from Arduino and process sensor readings."""
        if self.arduino.in_waiting > 0:
            line = self.arduino.readline().decode('ISO-8859-1').rstrip()

            try:
                # Try to split the line into two parts
                ledKey, sensorKey = line.split(":", 1)  # Split only once

                ledString, colorValue = ledKey.split("=", 1)  # Split only once
                ledColor = colorValue.strip()  # Clean up any leading/trailing spaces

                senorString, distanceValue = sensorKey.split("=", 1)  # Split only once
                distance = float(distanceValue.strip())  # Extract distance

                indexValue = ledString.split("_", 1)[1] # Split only once
                sensorIndex = int(indexValue)  # Clean up any leading/trailing spaces

                color_code = Colors.get_color(ledColor)

                logger.info(f"{color_code}Sensor Index : {sensorIndex}. Sensor Distance : {distance}. Led Color : {ledColor}{Colors.RESET}") # Log the actual data

                if sensorIndex < 2:  # Only process if valid sensor index (0 or 1)
                    self.sensor_data[sensorIndex] = distance
                    self.process_sensor_data(sensorIndex, distance)

                # Map the color to the terminal color
            except ValueError:
                # Catch the ValueError in case splitting fails
                logger.error(f"Error: Unable to unpack the line correctly: {line}")  # Log the actual data

            

    def process_sensor_data(self, sensor_index, distance):
        """Process and update the sensor data and LED color."""
        color = "red" if distance >= 10 else "yellow" if distance >= 5 else "green"
        self.send_command_to_arduino(f"{color}{sensor_index}")
        self.insert_colored_text(sensor_index, f"Sensor {sensor_index}: {distance} cm, LED: {color}", color)


    def insert_colored_text(self, sensor_index, text, color):
        """Insert text into the specific label widget based on sensor index."""
        # Schedule UI update on the main thread
        def update_label():
            current_text = self.labels[sensor_index].cget("text")
            new_text = f"{current_text}\n{text}"  # Append the new log text
            self.labels[sensor_index].configure(text=new_text)

        self.labels[sensor_index].after(0, update_label)


    def start_reading(self, delay=0.2):
        """Start reading sensor data in a background thread."""
        logger.info("Starting sensor reading thread.")  # Log when the sensor starts reading
        self.is_reading = True
        while self.is_reading:
            sensor_index = self.sensor_counter % 2
            self.sensor_counter += 1  # Increment the counter to alternate sensors
            # self.read_from_arduino()
            # Send a command to the selected sensor
            self.send_command_to_arduino(f"Sensor{sensor_index}_Command")

            time.sleep(delay)
            logger.success(f"Sensor reading in progress with delay of {delay} seconds.")  # Log the delay in each loop

    def stop_reading(self):
        """Stop reading sensor data."""
        self.is_reading = False
        logger.success("Stopping sensor reading.") 

    def get_timestamp(self):
        """Return the current timestamp formatted as 'YYYY-MM-DD HH:MM:SS'."""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
