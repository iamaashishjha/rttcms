# main.py
import customtkinter
import threading
from arduino_sensor_3 import ArduinoSensor

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Traffic Congestion Monitoring System")
        self.geometry("1100x580")
        self.sensor = None
        self.timer_running = False
        self.timer_1 = 60
        self.timer_2 = 60

        # GUI setup omitted for brevity

    def start_event(self):
        self.sidebar_button_1.configure(state="disabled")
        self.sidebar_button_2.configure(state="normal")
        self.sensor = ArduinoSensor(port='/dev/ttyUSB0', baudrate=9600, timeout=0.1, labels=[self.log_display_1, self.log_display_2])
        self.timer_running = True
        threading.Thread(target=self.sensor.start_reading, daemon=True).start()
        self.update_timer(self.timer_label_1, "timer_1")
        self.update_timer(self.timer_label_2, "timer_2")

    def update_timer(self, label, timer_attr):
        timer = getattr(self, timer_attr)
        if timer > 0 and self.timer_running:
            setattr(self, timer_attr, timer - 1)
            label.configure(text=f"Timer: {timer - 1}")
            self.after(1000, self.update_timer, label, timer_attr)
        else:
            label.configure(text="Timer: 0")

    def stop_event(self):
        self.sidebar_button_2.configure(state="disabled")
        self.sidebar_button_1.configure(state="normal")
        if self.sensor:
            self.sensor.stop_reading()
            self.sensor = None
        self.timer_running = False

    # Additional methods like `show_logs_event` and `change_appearance_mode_event` are omitted for brevity

if __name__ == "__main__":
    app = App()
    app.mainloop()
