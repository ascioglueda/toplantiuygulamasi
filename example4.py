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
        self.load_meetings_from_file()


    def create_meeting(self, organizer, title, possible_dates):
        meeting = {
            "organizer": organizer,
            "title": title,
            "possible_dates": possible_dates,
            "participants": {},
            "selected_date": None,  # Seçilen tarih
            "code": self.generate_code({"organizer": organizer, "title": title})
        }
        self.meetings.append(meeting)
        self.save_meetings_to_file()  # Save meetings to file after creating a new one
        return meeting

    def generate_code(self, meeting):
        code = hash(meeting["organizer"] + meeting["title"]) % 1000  # Toplantı kodunu 3 basamaklı yap
        return f"{code:03d}"


    def share_meeting_code(self, code, participants):
        for participant in participants:
            participant["meetings"].append(code)

    def show_available_dates(self, code, selected_date):
        for meeting in self.meetings:
            if self.generate_code(meeting) == code:
                if selected_date in meeting["possible_dates"]:
                    return meeting["possible_dates"]
                else:
                    return None  # Seçilen tarih müsait değil
        return None  # Geçersiz toplantı kodu

    # MeetingScheduler class'ındaki register_participation fonksiyonunu güncelle
    def register_participation(self, code, participant, selected_date):
        for meeting in self.meetings:
            if self.generate_code(meeting) == code:
                if selected_date in meeting["possible_dates"]:
                    if selected_date not in meeting["participants"].values():
                        meeting["participants"][participant] = selected_date
                        self.save_meetings_to_file()
                        return True  # Başarıyla kaydedildi
                    else:
                        return False  # Seçilen tarih başka bir katılımcı tarafından seçildi
                else:
                    return False  # Seçilen tarih müsait değil
        return False  # Geçersiz toplantı kodu

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

    def find_meeting_by_code(self, code):
        for meeting in self.meetings:
            if self.generate_code(meeting) == code:
                return meeting
        return None

    def show_available_dates(self, code):
        meeting = self.find_meeting_by_code(code)
        if meeting:
            return meeting["possible_dates"]
        return None  # Geçersiz toplantı kodu
        # Yeni metod: Katılımcının toplantıya katılmasını sağlar
    def participate_in_meeting(self, code, participant_name, selected_date):
        meeting = self.find_meeting_by_code(code)
        if meeting:
            if selected_date in meeting["possible_dates"]:
                if selected_date not in meeting["participants"].values():
                    meeting["participants"][participant_name] = selected_date
                    self.save_meetings_to_file()
                    return True  # Başarıyla kaydedildi
                else:
                    return False  # Seçilen tarih başka bir katılımcı tarafından seçildi
            else:
                return False  # Seçilen tarih müsait değil
        return False  # Geçersiz toplantı kodu

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
        self.button_add_to_google_calendar = tk.Button(master, text="Google Takvimine Ekle", command=self.add_to_google_calendar)
        self.label_participant_name = tk.Label(master, text="Katılımcı Adı:")
        self.entry_participant_name = tk.Entry(master)
        self.label_participant_date = tk.Label(master, text="Katılma Tarihi (gün.ay.yıl):")
        self.entry_participant_date_placeholder = tk.Label(master, text="örn: 01.01.2023", foreground="grey")
        self.entry_participant_date_var = tk.StringVar()
        self.entry_participant_date = tk.Entry(master, textvariable=self.entry_participant_date_var, width=30)
        self.entry_participant_date.bind("<FocusIn>", lambda event: self.entry_participant_date_placeholder.pack_forget())
        self.entry_participant_date.bind("<FocusOut>", lambda event: self.show_participant_date_placeholder())
        self.button_participate_in_meeting = tk.Button(master, text="Toplantıya Katıl", command=self.participate_in_meeting)
        # Arayüz bileşenlerini yerleştirme
        self.label_organizer.grid(row=0, column=0, sticky=tk.E, pady=5)
        self.entry_organizer.grid(row=0, column=1, pady=5)
        self.label_title.grid(row=1, column=0, sticky=tk.E, pady=5)
        self.entry_title.grid(row=1, column=1, pady=5)
        self.label_dates.grid(row=2, column=0, sticky=tk.E, pady=5)
        self.entry_dates.grid(row=2, column=1, pady=5)
        self.button_create_meeting.grid(row=3, column=0, columnspan=2, pady=10)
        self.label_participant_name.grid(row=4, column=0, sticky=tk.E, pady=5)
        self.entry_participant_name.grid(row=4, column=1, pady=5)
        self.label_participant_date.grid(row=5, column=0, sticky=tk.E, pady=5)
        self.entry_participant_date.grid(row=5, column=1, pady=5)
        self.button_participate_in_meeting.grid(row=6, column=0, columnspan=2, pady=10)

        self.treeview_meetings = ttk.Treeview(master, columns=("Organizer", "Title", "Possible Dates"))
        self.treeview_meetings.heading("#0", text="Meeting Code")
        self.treeview_meetings.heading("Organizer", text="Organizer")
        self.treeview_meetings.heading("Title", text="Title")
        self.treeview_meetings.heading("Possible Dates", text="Possible Dates")
        self.treeview_meetings.column("#0", width=0, stretch=tk.NO)

        self.treeview_meetings.grid(row=9, column=0, columnspan=2, pady=10)
        # MeetingApp class'ında __init__ metodunun sonuna ekle
        self.master.configure(bg='#ADD8E6')

        for meeting in self.scheduler.meetings:
                code = self.scheduler.generate_code(meeting)
                self.treeview_meetings.insert("", "end", values=(meeting["organizer"], meeting["title"], ', '.join(meeting["possible_dates"]), code))


    def create_meeting(self):
        organizer = self.entry_organizer.get()
        title = self.entry_title.get()
        dates_str = self.entry_dates.get()
        possible_dates = [date.strip() for date in dates_str.split(",")]

        if organizer and title and possible_dates:
            meeting = self.scheduler.create_meeting(organizer, title, possible_dates)
            meeting_code = meeting['code']
            messagebox.showinfo("Toplantı Oluşturuldu", f"Toplantı oluşturuldu. Bu kodu paylaş: {meeting['code']}")

            # Yeni toplantıyı Treeview'a ekleme
            self.treeview_meetings.insert("", "end", values=(organizer, title, ', '.join(possible_dates), meeting['code']))
            
            # Yeni toplantı oluşturulduktan hemen sonra toplantı bilgilerini text dosyasına kaydet
        else:
            messagebox.showwarning("Giriş Hatası", "Lütfen tüm alanları doldurun.")

    def add_to_google_calendar(self):
        code = self.entry_code.get()
        meeting_date = self.scheduler.show_available_dates(code)
        if meeting_date:
            meeting_date = simpledialog.askstring("Google Takvim'e Ekle", "Toplantı tarihini girin (YYYY-AA-GG):")
            if meeting_date:
                self.scheduler.add_to_google_calendar(code, meeting_date)
                messagebox.showinfo("Google Calendar", "Toplantı Google Takvim'e eklendi.")
            else:
                messagebox.showwarning("Lütfen geçerli bir tarih giriniz.")
        else:
            messagebox.showwarning("Geçersiz Kod", "Geçersiz toplantı kodu.")
    # MeetingApp class'ına yeni metod: Toplantıya katılma işlemini gerçekleştirir
    def participate_in_meeting(self):
        code = simpledialog.askstring("Toplantıya Katıl", "Toplantı kodunu girin:")
        if code:
            participant_name = self.entry_participant_name.get()
            participant_date = self.entry_participant_date.get()

            if participant_name and participant_date:
                success = self.scheduler.participate_in_meeting(code, participant_name, participant_date)

                if success:
                    messagebox.showinfo("Toplantıya Katılma", "Toplantıya başarıyla katıldınız.")
                else:
                    messagebox.showwarning("Toplantıya Katılma Hatası", "Seçtiğiniz tarih müsait değil veya başka bir katılımcı tarafından seçildi.")
            else:
                messagebox.showwarning("Giriş Hatası", "Lütfen katılımcı adı ve tarih alanlarını doldurun.")

    # MeetingApp class'ındaki show_placeholder metodunu güncelle
    def show_participant_date_placeholder(self):
        if not self.entry_participant_date_var.get():
            self.entry_participant_date_placeholder.pack(side="left")

    # MeetingApp class'ına yeni metod: Placeholder'ı gösterir
    def show_participant_date_placeholder(self):
        if not self.entry_participant_date_var.get():
            self.entry_participant_date_placeholder.pack(side="left")
if __name__ == "__main__":
    root = tk.Tk()
    app = MeetingApp(root)
    root.mainloop()