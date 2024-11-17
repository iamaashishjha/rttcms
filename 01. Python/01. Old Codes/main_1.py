import tkinter
import customtkinter
import threading
import time
from arduino_sensor import ArduinoSensor  # Import the ArduinoSensor class

# Set the default appearance mode to "System"
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Traffic Congestion Monitoring System")
        self.geometry("1100x580")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=160, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew", padx=10, pady=10)

        # Start button
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Start", command=self.start_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=15, sticky="ew")

        # Stop button
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Stop", command=self.stop_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=15, sticky="ew")

        # Show Logs button
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Show Logs", command=self.show_logs_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=15, sticky="ew")

        # Empty row for spacing
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Appearance mode label and option menu moved to the bottom
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 5))

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(5, 15))

        # Exit button (new button added at the bottom)
        self.sidebar_button_exit = customtkinter.CTkButton(self.sidebar_frame, text="Exit", command=self.quit)
        self.sidebar_button_exit.grid(row=7, column=0, padx=20, pady=10, sticky="ew")

        # Create main content area with two columns
        self.main_content_frame = customtkinter.CTkFrame(self)  # No padding in the constructor
        self.main_content_frame.grid(row=0, column=1, rowspan=2, columnspan=2, sticky="nsew", padx=5, pady=10)  # Padding added

        # Configure columns for the main content area (2 columns) with 5px padding
        self.main_content_frame.grid_columnconfigure(0, weight=1)  # First column (left)
        self.main_content_frame.grid_columnconfigure(1, weight=1)  # Second column (right)

        # Add widgets to the first column
        self.timer_label_1 = customtkinter.CTkLabel(self.main_content_frame, text="Timer 1: 60", font=("Arial", 20))
        self.timer_label_1.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")  # Added padding

        # self.timer_label_2 = customtkinter.CTkLabel(self.main_content_frame, text="Timer 2: 60", font=("Arial", 20))
        # self.timer_label_2.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")  # Added padding

        self.log_display_1 = customtkinter.CTkLabel(self.main_content_frame, text="Logs will appear here", font=("Arial", 12), anchor="w")
        self.log_display_1.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")  # Added padding

        # Add widgets to the second column
        # self.additional_label_1 = customtkinter.CTkLabel(self.main_content_frame, text="Additional Info 1", font=("Arial", 12))
        # self.additional_label_1.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")  # Added padding

        self.timer_label_2 = customtkinter.CTkLabel(self.main_content_frame, text="Timer 2: 60", font=("Arial", 20))
        self.timer_label_2.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")  # Added padding

        # self.additional_label_2 = customtkinter.CTkLabel(self.main_content_frame, text="Additional Info 2", font=("Arial", 12))
        # self.additional_label_2.grid(row=1, column=1, padx=5, pady=10, sticky="nsew")  # Added padding

        self.log_display_2 = customtkinter.CTkLabel(self.main_content_frame, text="Logs will appear here", font=("Arial", 12), anchor="w")
        self.log_display_2.grid(row=2, column=1, padx=5, pady=10, sticky="nsew")  # Added padding

        # Timer countdown values
        self.timer_1 = 60
        self.timer_2 = 60

        self.sensor = None
        self.timer_running = False

    def start_event(self):
        print("START EVENT CLICKED")
        # Disable the start button and enable the stop button
        self.sidebar_button_1.configure(state="disabled")
        self.sidebar_button_2.configure(state="normal")

        # Initialize the ArduinoSensor class and pass the label to it
        # self.sensor = ArduinoSensor(port='/dev/ttyUSB0', baudrate=9600, timeout=0.1, label=self.log_display)
        self.sensor = ArduinoSensor(port='/dev/ttyUSB0', baudrate=9600, timeout=0.1, labels=[self.log_display_1, self.log_display_2])

        # Start the sensor reading in a background thread
        sensor_thread = threading.Thread(target=self.sensor_reading_thread)
        sensor_thread.daemon = True  # Set as daemon thread so it exits with the main app
        sensor_thread.start()

        # Start the timers
        self.timer_running = True
        self.update_timer_1()
        self.update_timer_2()

    def sensor_reading_thread(self):
        while True:
            if self.sensor:
                # Simulate getting sensor data
                self.sensor.read_from_arduino()
                time.sleep(0.2)

    def update_timer_1(self):
        if self.timer_1 > 0 and self.timer_running:
            self.timer_1 -= 1
            self.timer_label_1.configure(text=f"Timer 1: {self.timer_1}")
            self.after(1000, self.update_timer_1)  # Call this method again after 1 second
        else:
            self.timer_label_1.configure(text="Timer 1: 0")

    def update_timer_2(self):
        if self.timer_2 > 0 and self.timer_running:
            self.timer_2 -= 1
            self.timer_label_2.configure(text=f"Timer 2: {self.timer_2}")
            self.after(1000, self.update_timer_2)  # Call this method again after 1 second
        else:
            self.timer_label_2.configure(text="Timer 2: 0")

    def stop_event(self):
        print("STOP EVENT CLICKED")
        # Disable the stop button and enable the start button
        self.sidebar_button_2.configure(state="disabled")
        self.sidebar_button_1.configure(state="normal")

        if self.sensor:
            self.sensor.stop_reading()
            self.sensor = None
        self.timer_running = False  # Stop the timers

    def show_logs_event(self):
        print("SHOW LOGS EVENT CLICKED")
        # Here you can add functionality to show logs from the sensor or other sources
        self.log_display_1.configure(text="Logs will be shown here.")
        self.log_display_2.configure(text="Logs will be shown here.")

    def change_appearance_mode_event(self, new_mode):
        customtkinter.set_appearance_mode(new_mode)

if __name__ == "__main__":
    app = App()
    app.mainloop()
