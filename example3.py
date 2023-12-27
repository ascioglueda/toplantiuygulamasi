# meeting_scheduler_app.py

import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import tkinter.ttk as ttk

class MeetingScheduler:
    def __init__(self):
        self.meetings = []

    def create_meeting(self, organizer, title, possible_dates):
        meeting = {
            "organizer": organizer,
            "title": title,
            "possible_dates": possible_dates,
            "participants": {},
            "selected_date": None  # Seçilen tarih
        }
        self.meetings.append(meeting)
        return meeting

    def generate_code(self, meeting):
        code = hash(meeting["organizer"] + meeting["title"]) % 1000  # Toplantı kodunu 3 basamaklı yap
        return f"{code:03d}"


    def share_meeting_code(self, code, participants):
        for participant in participants:
            participant["meetings"].append(code)

    def show_available_dates(self, code, selected_date):
        for meeting in self.meetings:
            if hash(meeting["organizer"] + meeting["title"]) == int(code):
                if selected_date in meeting["possible_dates"]:
                    return meeting["possible_dates"]
                else:
                    return None  # Seçilen tarih müsait değil
        return None  # Geçersiz toplantı kodu

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

    def add_to_google_calendar(self, code, meeting_date):
        # Burada Google Takvim'e ekleme işlemi yapılabilir.
        print(f"Added meeting on {meeting_date} to Google Calendar (code: {code}).")

    def save_to_txt(self, filename):
        # Mevcut dosyadaki bilgileri oku
        existing_meetings = []
        try:
            with open(filename, "r") as file:
                existing_meetings = file.readlines()
        except FileNotFoundError:
            pass

        # Yeni toplantı bilgilerini ekle
        with open(filename, "a") as file:
            for meeting in self.meetings:
                file.write(f"Organizer: {meeting['organizer']}\n")
                file.write(f"Title: {meeting['title']}\n")
                file.write(f"Possible Dates: {', '.join(meeting['possible_dates'])}\n")
                file.write(f"Participants: {', '.join(meeting['participants'])}\n")
                file.write(f"Selected Date: {meeting['selected_date']}\n")
                file.write("\n")

        # Eski toplantı bilgilerini tekrar dosyaya ekle
        with open(filename, "a") as file:
            file.writelines(existing_meetings)

class MeetingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Toplantı Planlama Uygulaması")

        self.scheduler = MeetingScheduler()

        # Arayüz bileşenleri
        self.label_organizer = tk.Label(master, text="Düzenleyen:")
        self.entry_organizer = tk.Entry(master)
        self.label_title = tk.Label(master, text="Başlık:")
        self.entry_title = tk.Entry(master)
        self.label_dates = tk.Label(master, text="Toplantı Tarihi (gün.ay.yıl):")
        self.entry_dates_placeholder = tk.Label(master, text="örn: 01.01.2023, 15.02.2023", foreground="grey")
        self.entry_dates_var = tk.StringVar()
        self.entry_dates = tk.Entry(master, textvariable=self.entry_dates_var, width=30)
        self.entry_dates.bind("<FocusIn>", lambda event: self.entry_dates_placeholder.pack_forget())
        self.entry_dates.bind("<FocusOut>", lambda event: self.show_placeholder())


        self.button_create_meeting = tk.Button(master, text="Toplantı Oluştur", command=self.create_meeting)

        #self.label_code = tk.Label(master, text="Toplantı Kodu:")
        #self.entry_code = tk.Entry(master)
        #self.button_share_code = tk.Button(master, text="Kodu Paylaş", command=self.share_code)

        #self.label_participant = tk.Label(master, text="Adınız:")
        #self.entry_participant = tk.Entry(master)
        #self.label_selected_date = tk.Label(master, text="Seçilen Tarih:")
        #self.entry_selected_date = tk.Entry(master)
        #self.button_register_participation = tk.Button(master, text="Katılım Kaydı Oluştur", command=self.register_participation)

        self.button_show_available_dates = tk.Button(master, text="Müsait Tarihleri Göster", command=self.show_available_dates)
        self.button_register_participation = tk.Button(master, text="Katılım Kaydı Oluştur", command=self.register_participation)
        self.button_add_to_google_calendar = tk.Button(master, text="Google Takvimine Ekle", command=self.add_to_google_calendar)

        # Arayüz bileşenlerini yerleştirme
        self.label_organizer.grid(row=0, column=0, sticky=tk.E, pady=5)
        self.entry_organizer.grid(row=0, column=1, pady=5)
        self.label_title.grid(row=1, column=0, sticky=tk.E, pady=5)
        self.entry_title.grid(row=1, column=1, pady=5)
        self.label_dates.grid(row=2, column=0, sticky=tk.E, pady=5)
        self.entry_dates.grid(row=2, column=1, pady=5)
        self.button_create_meeting.grid(row=3, column=0, columnspan=2, pady=10)

        self.treeview_meetings = ttk.Treeview(master, columns=("Organizer", "Title", "Possible Dates"))
        self.treeview_meetings.heading("#0", text="Meeting Code")
        self.treeview_meetings.heading("Organizer", text="Organizer")
        self.treeview_meetings.heading("Title", text="Title")
        self.treeview_meetings.heading("Possible Dates", text="Possible Dates")
        self.treeview_meetings.grid(row=9, column=0, columnspan=2, pady=10)

     #   self.label_code.grid(row=4, column=0, sticky=tk.E, pady=5)
    #    self.entry_code.grid(row=4, column=1, pady=5)
     #   self.button_share_code.grid(row=5, column=0, columnspan=2, pady=10)

        #self.label_participant.grid(row=6, column=0, sticky=tk.E, pady=5)
        #self.entry_participant.grid(row=6, column=1, pady=5)
        #self.label_selected_date.grid(row=7, column=0, sticky=tk.E, pady=5)
        #self.entry_selected_date.grid(row=7, column=1, pady=5)
       # self.button_register_participation.grid(row=8, column=0, columnspan=2, pady=10)

        master.protocol("WM_DELETE_WINDOW", self.on_closing)
    def on_closing(self):
            # Uygulama kapatıldığında toplantı bilgilerini kaydet
        self.scheduler.save_to_txt("meetings.txt")
        self.master.destroy()

    def create_meeting(self):
        organizer = self.entry_organizer.get()
        title = self.entry_title.get()
        dates_str = self.entry_dates.get()
        possible_dates = [date.strip() for date in dates_str.split(",")]

        if organizer and title and possible_dates:
            meeting = self.scheduler.create_meeting(organizer, title, possible_dates)
            code = self.scheduler.generate_code(meeting)
            messagebox.showinfo("Meeting Created", f"Meeting created. Share this code: {code}")

            # Yeni toplantıyı Treeview'a ekleme
            self.treeview_meetings.insert("", "end", values=(organizer, title, ', '.join(possible_dates), code))
            
            # Yeni toplantı oluşturulduktan hemen sonra toplantı bilgilerini text dosyasına kaydet
            self.scheduler.save_to_txt("meetings.txt")
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

    def show_available_dates(self):
        code = self.entry_code.get()
        selected_date = self.entry_selected_date.get()
        
        if code and selected_date:
            available_dates = self.scheduler.show_available_dates(code, selected_date)
            if available_dates:
                messagebox.showinfo("Available Dates", f"Available dates: {', '.join(available_dates)}")
            else:
                messagebox.showwarning("Invalid Input", "Invalid meeting code or selected date is not available.")
        else:
            messagebox.showwarning("Input Error", "Please enter a meeting code and a selected date.")

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

    def add_to_google_calendar(self):
        code = self.entry_code.get()
        meeting_date = self.scheduler.show_available_dates(code)
        if meeting_date:
            meeting_date = simpledialog.askstring("Add to Google Calendar", "Enter the meeting date (YYYY-MM-DD):")
            if meeting_date:
                self.scheduler.add_to_google_calendar(code, meeting_date)
                messagebox.showinfo("Google Calendar", "Meeting added to Google Calendar.")
            else:
                messagebox.showwarning("Input Error", "Please enter a valid date.")
        else:
            messagebox.showwarning("Invalid Code", "Invalid meeting code.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MeetingApp(root)
    root.mainloop()

    # Uygulama kapatıldıktan sonra toplantı bilgilerini kaydet
    app.scheduler.save_to_txt("meetings.txt")

