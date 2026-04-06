import customtkinter as ctk
from datetime import datetime
import threading
import time
import pygame

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AlarmApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Alarm Clock")
        self.geometry("420x320")

        pygame.mixer.init()

        # ===== TIME DISPLAY =====
        self.time_label = ctk.CTkLabel(self, text="", font=("Arial", 32, "bold"))
        self.time_label.pack(pady=(15, 5))

        self.date_label = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.date_label.pack(pady=(0, 15))

        # ===== INPUT SECTION =====
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=10)

        self.hour_entry = ctk.CTkEntry(input_frame, width=60, placeholder_text="HH")
        self.hour_entry.grid(row=0, column=0, padx=5, pady=10)

        self.min_entry = ctk.CTkEntry(input_frame, width=60, placeholder_text="MM")
        self.min_entry.grid(row=0, column=1, padx=5, pady=10)

        self.sec_entry = ctk.CTkEntry(input_frame, width=60, placeholder_text="SS")
        self.sec_entry.grid(row=0, column=2, padx=5, pady=10)

        # ===== BUTTON =====
        self.set_button = ctk.CTkButton(self, text="Set Alarm", command=self.set_alarm)
        self.set_button.pack(pady=15)

        # ===== STATUS =====
        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.status_label.pack()

        self.alarm_time = None
        self.alarm_triggered = False

        self.update_time()

    def update_time(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%A, %d %B %Y")

        self.time_label.configure(text=current_time)
        self.date_label.configure(text=current_date)

        if self.alarm_time == current_time and not self.alarm_triggered:
            self.alarm_triggered = True
            threading.Thread(target=self.trigger_alarm, daemon=True).start()

        self.after(1000, self.update_time)

    def set_alarm(self):
        try:
            h = int(self.hour_entry.get())
            m = int(self.min_entry.get())
            s = int(self.sec_entry.get())

            self.alarm_time = f"{h:02d}:{m:02d}:{s:02d}"
            self.alarm_triggered = False

            self.status_label.configure(text=f"Alarm set for {self.alarm_time}")

        except ValueError:
            self.status_label.configure(text="Invalid input. Use numbers only.")

    def trigger_alarm(self):
        try:
            pygame.mixer.music.load("Alarm/alarm.mp3")
            pygame.mixer.music.play()

            self.status_label.configure(text="⏰ Alarm Ringing!")

            time.sleep(10)
            pygame.mixer.music.stop()

            self.status_label.configure(text="Alarm Stopped")

        except Exception as e:
            self.status_label.configure(text="Error playing sound")
            print(e)


if __name__ == "__main__":
    app = AlarmApp()
    app.mainloop()