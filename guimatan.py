import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime
import subprocess
import os

def process_pcap(file_path, ex_start, ex_end, key):
    command = f'python make_reports.py "{file_path}" "{ex_start}" "{ex_end}" "{key}"'
    subprocess.run(command, shell=True)

def open_file():
    file_path = filedialog.askopenfilename(title="Select pcap file", filetypes=[("PCAP files", "*.pcap")])
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(0, file_path)

def start_processing():
    try:
        ex_start_date = entry_start_date.get_date()
        ex_start_hour = entry_start_hour.get()
        ex_start_minute = entry_start_minute.get()
        ex_start = datetime.strptime(f"{ex_start_date} {ex_start_hour}:{ex_start_minute}:00", "%Y-%m-%d %H:%M:%S")

        ex_end_date = entry_end_date.get_date()
        ex_end_hour = entry_end_hour.get()
        ex_end_minute = entry_end_minute.get()
        ex_end = datetime.strptime(f"{ex_end_date} {ex_end_hour}:{ex_end_minute}:00", "%Y-%m-%d %H:%M:%S") if ex_end_hour and ex_end_minute else None

        if var_maof.get() == 1:
            key = "WeLoveMaof"
        elif var_hsl.get() == 1:
            key = "HSLSecretKey"
        else:
            key = ""

        file_path = entry_file_path.get()

        if not os.path.exists(file_path):
            messagebox.showerror("Error", "File path does not exist")
            return
        
        process_pcap(file_path, ex_start, ex_end, key)
        messagebox.showinfo("Success", "Processing completed successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# יצירת חלון GUI
app = tk.Tk()
app.title("PCAP Processor")

frame = tk.Frame(app)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Start Date:").grid(row=0, column=0, sticky='e')
entry_start_date = DateEntry(frame, date_pattern="yyyy-mm-dd")
entry_start_date.grid(row=0, column=1, columnspan=2, sticky='w')

tk.Label(frame, text="Start Time:").grid(row=1, column=0, sticky='e')

start_hour_var = tk.StringVar(value="17")
entry_start_hour = tk.Spinbox(frame, from_=0, to=23, format="%02.0f", width=3, textvariable=start_hour_var)
entry_start_hour.grid(row=1, column=1, sticky='e')

start_minute_var = tk.StringVar(value="00")
entry_start_minute = tk.Spinbox(frame, from_=0, to=59, format="%02.0f", width=3, textvariable=start_minute_var)
entry_start_minute.grid(row=1, column=2, sticky='w')

tk.Label(frame, text="End Date (optional):").grid(row=2, column=0, sticky='e')
entry_end_date = DateEntry(frame, date_pattern="yyyy-mm-dd")
entry_end_date.grid(row=2, column=1, columnspan=2, sticky='w')

tk.Label(frame, text="End Time (optional):").grid(row=3, column=0, sticky='e')

end_hour_var = tk.StringVar()
entry_end_hour = tk.Spinbox(frame, from_=0, to=23, format="%02.0f", width=3, textvariable=end_hour_var)
entry_end_hour.grid(row=3, column=1, sticky='e')

end_minute_var = tk.StringVar()
entry_end_minute = tk.Spinbox(frame, from_=0, to=59, format="%02.0f", width=3, textvariable=end_minute_var)
entry_end_minute.grid(row=3, column=2, sticky='w')

tk.Label(frame, text="File Path:").grid(row=4, column=0, sticky='e')
entry_file_path = tk.Entry(frame, width=40)
entry_file_path.grid(row=4, column=1, columnspan=2, sticky='w')
tk.Button(frame, text="Browse", command=open_file).grid(row=4, column=3)

var_maof = tk.IntVar()
var_hsl = tk.IntVar()
tk.Checkbutton(frame, text="Use key for Maof", variable=var_maof).grid(row=5, column=0, sticky='w')
tk.Checkbutton(frame, text="Use key for HSL", variable=var_hsl).grid(row=5, column=1, sticky='w')

tk.Button(frame, text="Start Processing", command=start_processing).grid(row=6, columnspan=4, pady=10)

app.mainloop()
