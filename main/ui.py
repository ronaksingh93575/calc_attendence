import customtkinter as ctk
import tkinter as tk
import pandas as pd
import math

from calculator import AttendanceCalculator


class AttendanceUI(ctk.CTk):

    def __init__(self):

        super().__init__()


        self.title(f"Attendence")

        self.geometry("900x600")

        ctk.set_appearance_mode("Dark")

        self.data = pd.read_csv("academic_time_table.csv")
        self.subject_rows = []
        self.data["Date"] = pd.to_datetime(self.data["Date"])
        self.subject_columns = {
            "Select Subject": "None",
            "RESEARCH METHODOLOGY"              : "RM",
            "RESEARCH METHODOLOGY LAB"          : "RM(Lab)",
            "INFERENTIAL STATISTICS"            : "IS",
            "MACHINE LEARNING ALGORITHMS"       : "ML",
            "MACHINE LEARNING ALGORITHMS LAB"   : "ML(Lab)",
            "APPLIED DATA SCIENCE"              : "ADS",
            "APPLIED DATA SCIENCE LAB"          : "ADS(Lab)",
            "BIG DATA ECOSYSTEM"                : "BDE"
        }
        self.subjects = list(self.subject_columns.keys())

        self.months = [

            "July",
            "August" ,
            "September",
            "October",
            "November"
        ]
        self.month_map = {
            "July" : 7,
            "August": 8,
            "September": 9,
            "October": 10,
            "November": 11
        }

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
            "Total Classes",
            "Required (75%)"

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



    def generate_subject_rows(self, count):
        print(self.subject_rows)

        for row in self.subject_rows:
            for widget in row:
                widget.destroy()

        self.subject_rows.clear()

        count = int(count)

        for i in range(count):

            # Subject Dropdown
            subject = ctk.CTkComboBox(
                self.table,
                values = list(self.subject_columns.keys()),
                width=280
            )

            subject.grid(
                row=i + 1,
                column=0,
                padx=10,
                pady=5
            )

            # Classes Entry
            classes = ctk.CTkLabel(
                self.table,
                text ="-",
                width=100
            )

            classes.grid(
                row=i + 1,
                column=1,
                padx=10
            )

            # Result Label
            required = ctk.CTkLabel(
                self.table,
                text="-",
                width=100
            )

            required.grid(
                row=i + 1,
                column=2,
                padx=10
            )

            self.subject_rows.append(
                (
                    subject,
                    classes,
                    required
                )
            )
    def update_working_days(self, month):
        print(f"Selected Month: {month}")

    def update_working_days(self, month):

        month_number = self.month_map[month]

        month_data = self.data[
            self.data["Date"].dt.month == month_number
        ]
        print(month_data.head())
        print("Rows:", len(month_data))

        print(self.data["Status"].unique())

        working_days = month_data[
            month_data["Status"] == "Working day"
        ].shape[0]

        self.working_days = working_days
        self.working_label.configure(
            text = f"Working Days : {working_days}"
        )

    def calculate(self):
        print("calculate button clicked")

        month = self.month_menu.get()

        month_number = self.month_map[month]

        month_data = self.data[
            self.data["Date"].dt.month == month_number
        ]

        total_classes = 0

        for subject_box, total_label, required_label in self.subject_rows:

            subject_name = subject_box.get()

            if subject_name == "Select Subject":
                continue

            column = self.subject_columns[subject_name]

            # Sum all lectures of that subject
            classes = month_data[column].fillna(0).sum()

            required = math.ceil(classes * 0.75)

            total_label.configure(text=str(classes))

            required_label.configure(text=str(required))

            total_classes += classes

        overall_required = math.ceil(total_classes * 0.75)

        self.total_label.configure(
            text=f"Overall Classes : {total_classes}    Required : {overall_required}"
        )