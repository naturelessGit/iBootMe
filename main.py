import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import platform

# Create main window
root = tk.Tk()
root.title("iBootMe")
root.configure(bg="#1e1e1e")  # Dark background
root.geometry("800x600")

# Set system font
default_font = ("Segoe UI", 10) if platform.system() == "Windows" else ("San Francisco", 12)
root.option_add("*Font", default_font)

# Scrollable frame setup
main_frame = tk.Frame(root, bg="#1e1e1e")
main_frame.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(main_frame, bg="#1e1e1e", highlightthickness=0)
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#1e1e1e")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Style scrollbar
style = ttk.Style()
style.theme_use('clam')
style.configure("Vertical.TScrollbar", background="#333", troughcolor="#1e1e1e", bordercolor="#1e1e1e", arrowcolor="#ccc")

# Option storage
option_vars = {}

# Easy function to add options
def add_option(name, flag):
    var = tk.BooleanVar()
    chk = tk.Checkbutton(scrollable_frame, text=name, variable=var, bg="#1e1e1e", fg="white", activebackground="#1e1e1e", activeforeground="white", selectcolor="#333")
    chk.pack(anchor="w", padx=20, pady=2)
    option_vars[flag] = var

# Text inputs
entries = {}

def add_entry(label, key):
    frame = tk.Frame(scrollable_frame, bg="#1e1e1e")
    frame.pack(fill="x", padx=20, pady=2)
    tk.Label(frame, text=label, bg="#1e1e1e", fg="white").pack(side="left")
    ent = tk.Entry(frame, bg="#333", fg="white", insertbackground="white", relief="flat")
    ent.pack(side="left", fill="x", expand=True, padx=(10,0))
    entries[key] = ent

# Section 1: Normal
tk.Label(scrollable_frame, text="Normal Options", bg="#1e1e1e", fg="cyan", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=20, pady=(10, 2))
add_entry("UDID:", "--udid")
add_entry("ECID:", "--ecid")
add_entry("Cache Path:", "--cache-path")

add_option("Flash latest firmware", "--latest")
add_option("Erase device (Factory Reset)", "--erase")
add_option("Print IPSW Info Only", "--ipsw-info")
add_option("Enable Debug Logging", "--debug")
add_option("Show iBootMe Library Version", "--version")

# Section 2: Advanced / Experimental
tk.Label(scrollable_frame, text="Advanced Options", bg="#1e1e1e", fg="cyan", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=20, pady=(10, 2))
add_option("Restore with Custom Firmware (bootrom exploit needed)", "--custom")
add_option("Exclude NOR/Baseband Update", "--exclude")
add_option("Fetch TSS (SHSH Save)", "--shsh")
add_option("No Restore After Ramdisk Boot (legacy devices)", "--no-restore")
add_option("Keep Personalized Components", "--keep-pers")
add_option("Put Device in Pwned DFU (limera1n devices)", "--pwn")
add_option("Plain Progress Output", "--plain-progress")
add_option("Allow Restoring from Restore Mode", "--restore-mode")
add_option("Ignore Errors During Restore", "--ignore-errors")

add_entry("Override Signing Server URL:", "--server")
add_entry("Custom Ticket Path:", "--ticket")
add_entry("Variant:", "--variant")

def fetch_udid():
    try:
        # Run the idevice_id command to get the UDID
        result = subprocess.run(["idevice_id", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            # Successfully fetched the UDID
            udid = result.stdout.strip()  # Remove any extra spaces or newlines
            # Insert the UDID into the UDID input field
            entries["--udid"].delete(0, tk.END)  # Clear the current input field
            entries["--udid"].insert(0, udid)    # Insert the fetched UDID
            output_terminal.insert(tk.END, f"UDID fetched: {udid}\n")
        else:
            # If the command fails, display an error
            output_terminal.insert(tk.END, f"Error fetching UDID: {result.stderr}\n")
    except Exception as e:
        output_terminal.insert(tk.END, f"Exception: {str(e)}\n")


def fetch_ecid():
    output_terminal.insert(tk.END, "Fetching ECID...\n(Feature to be implemented)\n")

btn_frame = tk.Frame(scrollable_frame, bg="#1e1e1e")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Fetch UDID", command=fetch_udid, bg="#333", fg="white", relief="flat").pack(side="left", padx=10)
tk.Button(btn_frame, text="Fetch ECID", command=fetch_ecid, bg="#333", fg="white", relief="flat").pack(side="left", padx=10)

# File picker for IPSW
ipsw_path = tk.StringVar()

def browse_ipsw():
    path = filedialog.askopenfilename(title="Select IPSW File", filetypes=[("IPSW files", "*.ipsw")])
    if path:
        ipsw_path.set(path)

frame_ipsw = tk.Frame(scrollable_frame, bg="#1e1e1e")
frame_ipsw.pack(fill="x", padx=20, pady=5)
tk.Button(frame_ipsw, text="Select IPSW", command=browse_ipsw, bg="#333", fg="white", relief="flat").pack(side="left")
tk.Entry(frame_ipsw, textvariable=ipsw_path, bg="#333", fg="white", insertbackground="white", relief="flat").pack(side="left", fill="x", expand=True, padx=(10,0))

# Terminal output
output_terminal = tk.Text(root, height=10, bg="#111", fg="lime", insertbackground="lime", relief="flat")
output_terminal.pack(fill="x", side="bottom")

# Function to build and run the command
def run_restore():
    output_terminal.delete(1.0, tk.END)
    command = ["idevicerestore"]

    for flag, var in option_vars.items():
        if var.get():
            command.append(flag)

    for flag, entry in entries.items():
        value = entry.get().strip()
        if value:
            command.append(flag)
            command.append(value)

    ipsw = ipsw_path.get()
    if ipsw and "--latest" not in command:
        command.append(ipsw)

    output_terminal.insert(tk.END, f"Running: {' '.join(command)}\n\n")
    try:
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in proc.stdout:
            output_terminal.insert(tk.END, line)
            output_terminal.see(tk.END)
        proc.wait()
    except Exception as e:
        output_terminal.insert(tk.END, f"Error: {e}\n")

tk.Button(root, text="Flash!", command=run_restore, bg="#0078D7", fg="white", relief="flat", font=("Segoe UI", 12)).pack(pady=10)

root.mainloop()
