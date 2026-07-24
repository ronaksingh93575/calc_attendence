import customtkinter as ctk
import tkinter as tk
import pandas as pd

from calculator import AttendanceCalculator


class AttendanceUI(ctk.CTk):

    def __init__(self):

        super().__init__()


        self.title(f"Attendence")

        self.geometry("900x600")

        ctk.set_appearance_mode("Dark")

        self.subject_rows = []
        self.data = pd.read_csv("academic_time_table.csv")
        self.subject_columns = {
            "Select Subject" : 0,
            "RESEARCH METHODOLOGY": "RM",
            "RESEARCH METHODOLOGY LAB": "RM(Lab)",            
            "INFERENTIAL STATISTICS": "IS",
            "MACHINE LEARNING ALGORITHMS": "ML",
            "MACHINE LEARNING ALGORITHMS LAB": "ML(Lab)",
            "APPLIED DATA SCIENCE": "ADS",
            "APPLIED DATA SCIENCE LAB": "ADS(Lab)",
            "BIG DATA ECOSYSTEM": "BDE"
        }

        self.months = [

            "August",

            "September",

            "October",

            "November"

        ]

        self.create_widgets()

    def create_widgets(self):

        title = ctk.CTkLabel(

            self,

            text="Calculate \U0001F447",

            font=("Arial", 24, "bold")

        )

        title.pack(pady=20)

        top = ctk.CTkFrame(self)

        top.pack(fill="x", padx=20)

        ctk.CTkLabel(
            top,
            text="Month"
        ).grid(row=0, column=0, padx=10, pady=10)

        self.month_menu = ctk.CTkOptionMenu(

            top,

            values=self.months,

            command=self.update_working_days

        )

        self.month_menu.grid(row=0, column=1)

        ctk.CTkLabel(
            top,
            text="Subjects"
        ).grid(row=0, column=2, padx=20)

        self.subject_menu = ctk.CTkOptionMenu(

            top,

            values=[str(i) for i in range(1, 11)],

            command=self.generate_subject_rows

        )

        self.subject_menu.grid(row=0, column=3)

        self.working_label = ctk.CTkLabel(

            top,

            text="Working Days : "

        )

        self.working_label.grid(row=0, column=4, padx=20)

        self.table = ctk.CTkFrame(self)

        self.table.pack(fill="both", expand=True, padx=20, pady=20)

        headers = [

            "Subject",

            "Classes / 5 Days",

            "Need (75%)"

        ]

        for i, h in enumerate(headers):

            ctk.CTkLabel(

                self.table,

                text=h,

                font=("Arial", 15, "bold")

            ).grid(
                row=0,
                column=i,
                padx=15,
                pady=10
            )

        self.total_label = ctk.CTkLabel(

            self,

            text=""

        )

        self.total_label.pack(pady=10)

        calculate = ctk.CTkButton(

            self,

            text="Calculate",

            command=self.calculate

        )

        calculate.pack(pady=10)

        self.update_working_days(
            self.months[0]
        )

        self.generate_subject_rows("1")

    def update_working_days(self, month):

        working_days = {
            "August": 19,
            "September": 20,
            "October": 19,
            "November": 15
        }

        self.working_days = working_days.get(month, 0)

        self.working_label.configure(
            text=f"Working Days : {self.working_days}"
        )
    def generate_subject_rows(self, count):

        for row in self.subject_rows:
            for widget in row:
                widget.destroy()

        self.subject_rows.clear()

        count = int(count)

        for i in range(count):

            # Subject Dropdown
            subject = ctk.CTkComboBox(
                self.table,
                values=list(self.subject_data.keys()),
                width=280
            )

            subject.grid(
                row=i + 1,
                column=0,
                padx=10,
                pady=5
            )

            # Classes Entry
            classes = ctk.CTkEntry(
                self.table,
                width=100
            )

            classes.grid(
                row=i + 1,
                column=1,
                padx=10
            )

            # Result Label
            result = ctk.CTkLabel(
                self.table,
                text="-",
                width=80
            )

            result.grid(
                row=i + 1,
                column=2,
                padx=10
            )

            # Auto-fill classes when subject changes
            subject.configure(
                command=lambda value,
                entry=classes: self.subject_selected(value, entry)
            )

            self.subject_rows.append(
                (
                    subject,
                    classes,
                    result
                )
            )
    def calculate(self):

        total_classes = 0

        for subject, classes, result in self.subject_rows:

            try:

                value = int(classes.get())

            except ValueError:

                result.configure(text="Invalid")

                continue

            estimated, needed = AttendanceCalculator.calculate_subject(

                self.working_days,

                value

            )

            total_classes += estimated

            result.configure(

                text=f"{needed}/{estimated}"

            )

        overall = AttendanceCalculator.calculate_overall(
            total_classes
        )

        self.total_label.configure(

            text=f"Total Classes : {total_classes}     Need Overall : {overall}"

        )
    def subject_selected(self, subject_name, class_entry):

        classes = self.subject_data.get(subject_name, "")

        class_entry.delete(0, "end")
        class_entry.insert(0, str(classes))