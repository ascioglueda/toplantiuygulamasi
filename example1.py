import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

class MeetingScheduler:
    def __init__(self):
        self.meetings = []

    def create_meeting(self, organizer, title, possible_dates):
        meeting = {
            "organizer": organizer,
            "title": title,
            "possible_dates": possible_dates,
            "participants": {}
        }
        self.meetings.append(meeting)
        return meeting

    def generate_code(self, meeting):
        code = hash(meeting["organizer"] + meeting["title"])
        return str(code)

    def share_meeting_code(self, code, participants):
        for participant in participants:
            participant["meetings"].append(code)

    def show_available_dates(self, code):
        for meeting in self.meetings:
            if hash(meeting["organizer"] + meeting["title"]) == int(code):
                return meeting["possible_dates"]
        return None

    def register_participation(self, code, participant, selected_date):
        for meeting in self.meetings:
            if hash(meeting["organizer"] + meeting["title"]) == int(code):
                meeting["participants"][participant] = selected_date
                return True
        return False

    def save_meetings_to_file(self):
        with open("meetings.json", "w") as file:
            json.dump(self.meetings, file)

    def load_meetings_from_file(self):
        try:
            with open("meetings.json", "r") as file:
                self.meetings = json.load(file)
        except FileNotFoundError:
            pass

class MeetingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Toplantı Planlama Uygulaması")

        self.scheduler = MeetingScheduler()

        # Arayüz bileşenleri
        self.label_organizer = tk.Label(master, text="Organizer:")
        self.entry_organizer = tk.Entry(master)
        self.label_title = tk.Label(master, text="Title:")
        self.entry_title = tk.Entry(master)
        self.label_dates = tk.Label(master, text="Possible Dates (comma separated):")
        self.entry_dates = tk.Entry(master)
        self.button_create_meeting = tk.Button(master, text="Create Meeting", command=self.create_meeting)

        self.label_code = tk.Label(master, text="Meeting Code:")
        self.entry_code = tk.Entry(master)
        self.button_share_code = tk.Button(master, text="Share Code", command=self.share_code)

        self.label_participant = tk.Label(master, text="Your Name:")
        self.entry_participant = tk.Entry(master)
        self.label_selected_date = tk.Label(master, text="Selected Date:")
        self.entry_selected_date = tk.Entry(master)
        self.button_register_participation = tk.Button(master, text="Register Participation", command=self.register_participation)

        # Arayüz bileşenlerini yerleştirme
        self.label_organizer.grid(row=0, column=0, sticky=tk.E, pady=5)
        self.entry_organizer.grid(row=0, column=1, pady=5)
        self.label_title.grid(row=1, column=0, sticky=tk.E, pady=5)
        self.entry_title.grid(row=1, column=1, pady=5)
        self.label_dates.grid(row=2, column=0, sticky=tk.E, pady=5)
        self.entry_dates.grid(row=2, column=1, pady=5)
        self.button_create_meeting.grid(row=3, column=0, columnspan=2, pady=10)

        self.label_code.grid(row=4, column=0, sticky=tk.E, pady=5)
        self.entry_code.grid(row=4, column=1, pady=5)
        self.button_share_code.grid(row=5, column=0, columnspan=2, pady=10)

        self.label_participant.grid(row=6, column=0, sticky=tk.E, pady=5)
        self.entry_participant.grid(row=6, column=1, pady=5)
        self.label_selected_date.grid(row=7, column=0, sticky=tk.E, pady=5)
        self.entry_selected_date.grid(row=7, column=1, pady=5)
        self.button_register_participation.grid(row=8, column=0, columnspan=2, pady=10)


    def create_meeting(self):
        organizer = self.entry_organizer.get()
        title = self.entry_title.get()
        dates_str = self.entry_dates.get()
        possible_dates = [date.strip() for date in dates_str.split(",")]

        if organizer and title and possible_dates:
            meeting = self.scheduler.create_meeting(organizer, title, possible_dates)
            code = self.scheduler.generate_code(meeting)
            messagebox.showinfo("Meeting Created", f"Meeting created. Share this code: {code}")
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def share_code(self):
        code = self.entry_code.get()
        if code:
            participants = [
                {"name": "Ayşe", "meetings": []},
                {"name": "Mehmet", "meetings": []},
                {"name": "Merve", "meetings": []}
            ]
            self.scheduler.share_meeting_code(code, participants)
            messagebox.showinfo("Code Shared", "Meeting code shared with participants.")
        else:
            messagebox.showwarning("Input Error", "Please enter a meeting code.")

    def register_participation(self):
        code = self.entry_code.get()
        participant = self.entry_participant.get()
        selected_date = self.entry_selected_date.get()

        if code and participant and selected_date:
            success = self.scheduler.register_participation(code, participant, selected_date)
            if success:
                messagebox.showinfo("Participation Registered", f"{participant} registered for the meeting.")
            else:
                messagebox.showwarning("Registration Error", "Invalid meeting code.")
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MeetingApp(root)
    root.mainloop()
