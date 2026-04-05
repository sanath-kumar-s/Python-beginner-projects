import customtkinter as ctk
from datetime import datetime
import time
import threading
import pygame

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AlarmApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Alarm Clock")
        self.geometry("400x300")

        pygame.mixer.init()  # initialize audio

        # Current time label
        self.time_label = ctk.CTkLabel(self, text="", font=("Arial", 24))
        self.time_label.pack(pady=10)

        # Current date label
        self.date_label = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.date_label.pack()

        # Alarm input
        self.alarm_entry = ctk.CTkEntry(self, placeholder_text="Set alarm (HH:MM:SS)")
        self.alarm_entry.pack(pady=20)

        # Set alarm button
        self.set_button = ctk.CTkButton(self, text="Set Alarm", command=self.set_alarm)
        self.set_button.pack()

        self.alarm_time = None
        self.alarm_triggered = False  # prevent multiple triggers

        self.update_time()

    def update_time(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%A, %d %B %Y")

        self.time_label.configure(text=current_time)
        self.date_label.configure(text=current_date)

        # Trigger alarm once
        if self.alarm_time == current_time and not self.alarm_triggered:
            self.alarm_triggered = True
            threading.Thread(target=self.trigger_alarm, daemon=True).start()

        self.after(1000, self.update_time)

    def set_alarm(self):
        self.alarm_time = self.alarm_entry.get()
        self.alarm_triggered = False
        print(f"Alarm set for {self.alarm_time}")

    def trigger_alarm(self):
        try:
            pygame.mixer.music.load("Alarm/alarm.mp3")
            pygame.mixer.music.play()

            time.sleep(10)  # play for 10 sec
            pygame.mixer.music.stop()
        except Exception as e:
            print("Error playing sound:", e)

if __name__ == "__main__":
    app = AlarmApp()
    app.mainloop()