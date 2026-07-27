import customtkinter as ctk

app = ctk.CTk()

headers = ["Subject", "Attended", "Total"]
table_frame = ctk.CTkFrame(app)
table_frame.pack()

# Creates "Subject" at Col 0, "Attended" at Col 1, "Total" at Col 2
for i, h in enumerate(headers):
    ctk.CTkLabel(
        table_frame, 
        text=h, 
        font=("Arial", 15, "bold")
    ).grid(row=0, column=i, padx=15, pady=10)

# Empty label ready to display overall score later
total_label = ctk.CTkLabel(app, text="")
total_label.pack()

app.mainloop()
