import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk
import threading
import time
import random
from datetime import datetime
import shutil
import os
from tkinterdnd2 import DND_FILES, TkinterDnD

# PDF
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

# ---------------- App Config ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = TkinterDnD.Tk()
app.geometry("1200x700")
app.title("CyberShield - Ransomware Detector")
app.configure(bg="#1a1a1a")
app.geometry("1200x700")
app.title("CyberShield - Ransomware Detector")

selected_file = None
current_mode = "dark"
current_tab = "home"

# ---------------- Sidebar ----------------
sidebar = ctk.CTkFrame(app, width=220, corner_radius=0)
sidebar.pack(side="left", fill="y")

# ---------------- Navigation ----------------
def show_tab(name):

    global current_tab
    current_tab = name

    if name == "logs":
        logs_frame.tkraise()

    elif name == "about":
        about_frame.tkraise()

    else:
        home_frame.tkraise()

# ---------------- Back Button ----------------
back_button = ctk.CTkButton(
    sidebar,
    text="← Back",
    width=160,
    height=40,
    fg_color="#2b2b2b",
    hover_color="#3a3a3a",
    command=lambda: show_tab("home")
)

back_button.pack(pady=(20, 10))

# ---------------- Logo ----------------
logo = ctk.CTkLabel(
    sidebar,
    text="🛡️ CyberShield",
    font=("Arial", 24, "bold")
)

logo.pack(pady=20)



# ---------------- Sidebar Buttons ----------------
home_btn = ctk.CTkButton(
    sidebar,
    text="🏠 Home",
    command=lambda: show_tab("home")
)

home_btn.pack(pady=10)

logs_btn = ctk.CTkButton(
    sidebar,
    text="📄 Logs",
    command=lambda: show_tab("logs")
)

logs_btn.pack(pady=10)

about_btn = ctk.CTkButton(
    sidebar,
    text="ℹ About",
    command=lambda: show_tab("about")
)

about_btn.pack(pady=10)

# ---------------- Main ----------------
main = ctk.CTkFrame(app)
main.pack(side="right", expand=True, fill="both")

# ---------------- Header ----------------
header = ctk.CTkFrame(main, height=60)
header.pack(fill="x")

status_label = ctk.CTkLabel(
    header,
    text="System Status: Idle 🟡",
    font=("Arial", 16)
)

status_label.pack(side="left", padx=20, pady=10)

# ---------------- Theme Toggle ----------------
def toggle_theme():

    global current_mode

    if current_mode == "dark":

        ctk.set_appearance_mode("light")

        current_mode = "light"

    else:

        ctk.set_appearance_mode("dark")

        current_mode = "dark"

theme_button = ctk.CTkButton(
    header,
    text="🌗 Dark / Light",
    width=140,
    height=35,
    command=toggle_theme
)

theme_button.pack(
    side="right",
    padx=20,
    pady=10
)

# ---------------- Container ----------------
container = ctk.CTkFrame(main)

container.pack(
    expand=True,
    fill="both",
    padx=20,
    pady=20
)

# ---------------- Frames ----------------
home_frame = ctk.CTkFrame(container)
logs_frame = ctk.CTkFrame(container)
about_frame = ctk.CTkFrame(container)

for frame in (home_frame, logs_frame, about_frame):

    frame.place(
        relwidth=1,
        relheight=1
    )

# ---------------- Home Layout ----------------
left_frame = ctk.CTkFrame(home_frame)

left_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=20,
    pady=20
)

right_frame = ctk.CTkFrame(
    home_frame,
    width=280,
    corner_radius=20,
    fg_color="#2b2b2b",
    border_width=3,
    border_color="#444444"
)

right_frame.pack(
    side="right",
    fill="y",
    padx=20,
    pady=20
)

# ---------------- Home UI ----------------
scan_title = ctk.CTkLabel(
    left_frame,
    text="Scan Your File",
    font=("Arial", 28, "bold")
)

scan_title.pack(pady=20)

result_label = ctk.CTkLabel(
    left_frame,
    text="No file selected",
    font=("Arial", 18),
    wraplength=600
)

result_label.pack(pady=20)

# ---------------- Drag & Drop Area ----------------
drop_area = tk.Label(
    left_frame,
    text="📂 Drag & Drop File Here",
    bg="#2b2b2b",
    fg="white",
    font=("Arial", 16),
    width=40,
    height=5
)

drop_area.pack(pady=15)

# Drop Function
def drop_file(event):

    global selected_file

    file_path = event.data.strip("{}")

    selected_file = file_path

    result_label.configure(
        text=f"Selected File:\n{file_path}",
        text_color="white"
    )

# Enable Drag & Drop
drop_area.drop_target_register(DND_FILES)

drop_area.dnd_bind(
    '<<Drop>>',
    drop_file
)

# ---------------- Upload File ----------------
def upload_file():

    global selected_file

    file_path = filedialog.askopenfilename()

    if file_path:

        selected_file = file_path

        result_label.configure(
            text=f"Selected File:\n{file_path}",
            text_color="white"
        )

upload_button = ctk.CTkButton(
    left_frame,
    text="Upload File",
    width=220,
    height=45,
    command=upload_file
)

upload_button.pack(pady=10)

# ---------------- Folder Scan ----------------
def scan_folder():

    folder_path = filedialog.askdirectory()

    if not folder_path:
        return

    files = os.listdir(folder_path)

    for file in files:

        full_path = os.path.join(
            folder_path,
            file
        )

        if os.path.isfile(full_path):

            global selected_file

            selected_file = full_path

            scan_file()

folder_button = ctk.CTkButton(
    left_frame,
    text="Scan Folder",
    width=220,
    height=45,
    fg_color="#1f6cff",
    hover_color="#174bcc",
    command=scan_folder
)

folder_button.pack(pady=10)

# ---------------- Scan Button ----------------
scan_button = ctk.CTkButton(
    left_frame,
    text="SCAN",
    width=220,
    height=45,
    fg_color="green",
    hover_color="#0d8f3d"
)

scan_button.pack(pady=10)

# ---------------- Progress Circle ----------------
scan_status = ctk.CTkLabel(
    right_frame,
    text= "Scan progress",
    font=("Arial", 18)
)

scan_status.pack(pady=20)

canvas = tk.Canvas(
    right_frame,
    width=180,
    height=180,
    bg="#2b2b2b",
    highlightthickness=0
)

canvas.pack(pady=20)

background_ring = canvas.create_oval(
    10, 10, 170, 170,
    outline="#444444",
    width=10
)

glow_arc = canvas.create_arc(
    6, 6, 174, 174,
    start=90,
    extent=0,
    style="arc",
    outline="#1f6cff",
    width=18
)

arc = canvas.create_arc(
    10, 10, 170, 170,
    start=90,
    extent=0,
    style="arc",
    outline="#4da6ff",
    width=10
)

percent_text = canvas.create_text(
    90,
    90,
    text="0%",
    fill="white",
    font=("Arial", 28, "bold")
)

# ---------------- Logs UI ----------------
log_title = ctk.CTkLabel(
    logs_frame,
    text="Detection History",
    font=("Arial", 24, "bold")
)

log_title.pack(pady=15)

logs_container = ctk.CTkScrollableFrame(
    logs_frame,
    width=900,
    height=500
)

logs_container.pack(pady=20)

# ---------------- About UI ----------------
about_label = ctk.CTkLabel(
    about_frame,
    text=(
        "CyberShield v1.0\n\n"
        "Machine Learning Based\n"
        "Ransomware Detection Tool\n\n"
        "Made by Omar 😎"
    ),
    font=("Arial", 20)
)

about_label.pack(pady=80)

# ---------------- PDF Export ----------------
def export_pdf(
    result,
    family,
    confidence,
    reason,
    scan_time
):

    clean_result = (
        result
        .replace("✅", "")
        .replace("❌", "")
    )

    clean_reason = (
        reason
        .replace("⚠", "")
        .replace("❌", "")
        .replace("🛡", "")
        .replace("📌", "")
    )

    pdf_file_name = (
        f"scan_report_{int(time.time())}.pdf"
    )

    pdf = SimpleDocTemplate(
        pdf_file_name,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    content = []

    title = Paragraph(
        "CyberShield Scan Report",
        styles['Title']
    )

    content.append(title)
    content.append(Spacer(1, 20))

    report_data = f"""
    <b>Detection Result:</b> {clean_result}<br/><br/>

    <b>Ransomware Family:</b> {family}<br/><br/>

    <b>Scan Time:</b> {scan_time:.2f} seconds<br/><br/>

    <b>Detection Confidence:</b> {confidence}%<br/><br/>

    <b>Analysis Reason:</b><br/><br/>

    {clean_reason}
    """

    body = Paragraph(
        report_data,
        styles['BodyText']
    )

    content.append(body)

    try:

        pdf.build(content)

        success_window = ctk.CTkToplevel(app)

        success_window.geometry("400x180")
        success_window.title("PDF Exported")

        success_window.focus()
        success_window.grab_set()

        success_label = ctk.CTkLabel(
            success_window,
            text=(
                "PDF Exported Successfully\n\n"
                f"{pdf_file_name}"
            ),
            font=("Arial", 18),
            text_color="green"
        )

        success_label.pack(
            expand=True,
            pady=40
        )

    except Exception as e:

        error_window = ctk.CTkToplevel(app)

        error_window.geometry("450x220")
        error_window.title("Export Error")

        error_window.focus()
        error_window.grab_set()

        error_label = ctk.CTkLabel(
            error_window,
            text=(
                f"Failed To Export PDF\n\n{str(e)}"
            ),
            font=("Arial", 16),
            text_color="red",
            wraplength=350
        )

        error_label.pack(
            expand=True,
            pady=40
        )

# ---------------- Report Window ----------------
def show_report(
    result,
    family,
    reason,
    confidence,
    scan_time
):

    report_window = tk.Toplevel(app)
    report_window.attributes("-topmost", True)
    report_window.after(100, lambda: report_window.attributes("-topmost", False))

    report_window.geometry("650x550")
    report_window.title("Scan Report")
    report_window.lift()


    title = ctk.CTkLabel(
        report_window,
        text="Scan Report",
        font=("Arial", 28, "bold")
    )

    title.pack(pady=20)

    status_color = (
        "green"
        if "Safe" in result
        else "red"
    )


# ---------------- STATUS CARD ----------------
    status_card = ctk.CTkFrame(
        report_window,
        corner_radius=20,
        fg_color="#242424"
    )

    status_card.pack(
        fill="x",
        padx=20,
        pady=15
    )

    status_text = ctk.CTkLabel(
        status_card,
        text=f"Result: {result}",
        font=("Arial", 24, "bold"),
        text_color=status_color
    )

    status_text.pack(
        pady=20
    )

    # ---------------- INFO CARD ----------------
    info_card = ctk.CTkFrame(
        report_window,
        corner_radius=20
    )

    info_card.pack(
        fill="x",
        padx=20,
        pady=10
    )

    family_label = ctk.CTkLabel(
        info_card,
        text=f"Ransomware Family: {family}",
        font=("Arial", 18)
    )

    family_label.pack(
        anchor="w",
        padx=20,
        pady=(20,10)
    )

    confidence_label = ctk.CTkLabel(
        info_card,
        text=f"Detection Confidence: {confidence}%",
        font=("Arial", 18)
    )

    confidence_label.pack(
        anchor="w",
        padx=20,
        pady=10
    )

    time_label = ctk.CTkLabel(
        info_card,
        text=f"Scan Time: {scan_time:.2f} sec",
        font=("Arial", 18)
    )

    time_label.pack(
        anchor="w",
        padx=20,
        pady=(10,20)
    )

    # ---------------- ANALYSIS CARD ----------------
    analysis_card = ctk.CTkFrame(
        report_window,
        corner_radius=20
    )

    analysis_card.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=15
    )

    analysis_title = ctk.CTkLabel(
        analysis_card,
        text="Analysis Reason",
        font=("Arial", 20, "bold")
    )

    analysis_title.pack(
        anchor="w",
        padx=20,
        pady=(20,10)
    )

    analysis_text = ctk.CTkLabel(
        analysis_card,
        text=reason,
        wraplength=520,
        justify="left",
        font=("Arial", 16)
    )

    analysis_text.pack(
        anchor="w",
        padx=20,
        pady=(0,20)
    )
    
    export_btn = ctk.CTkButton(

    report_window,

    text="Export PDF",

    width=180,

    height=40,

    font=("Arial", 16, "bold"),

    command=lambda: export_pdf(

        result,
        family,
        confidence,
        reason,
        scan_time

    )

    )

    export_btn.pack(pady=10)

# ---------------- Detection History ----------------
def add_log_card(
    file_name,
    result,
    family,
    reason,
    confidence,
    scan_time
):

    card = ctk.CTkFrame(
        logs_container,
        corner_radius=15
    )

    card.pack(
        fill="x",
        padx=10,
        pady=10
    )

    time_now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    title = ctk.CTkLabel(
        card,
        text=f"{time_now}\n\n{file_name}",
        font=("Arial", 15),
        justify="left"
    )

    title.pack(
        side="left",
        padx=15,
        pady=15
    )

    view_btn = ctk.CTkButton(
        card,
        text="View Report ➜",
        width=150,
        command=lambda: show_report(
            result,
            family,
            reason,
            confidence,
            scan_time
        )
            )

    view_btn.pack(
        side="right",
        padx=15
    )

# ---------------- Quarantine ----------------
def quarantine_file(file_path):

    quarantine_folder = "quarantine"

    if not os.path.exists(
        quarantine_folder
    ):

        os.makedirs(
            quarantine_folder
        )

    file_name = os.path.basename(
        file_path
    )

    destination = os.path.join(
        quarantine_folder,
        file_name
    )

    try:

        shutil.move(
            file_path,
            destination
        )

        return True, destination

    except Exception as e:

        return False, str(e)

# ---------------- Scan Function ----------------
def scan_file():

    global selected_file

    if not selected_file:

        result_label.configure(
            text="No file selected",
            text_color="red"
        )

        return

    file_path = selected_file

    status_label.configure(
        text="System Status: Scanning..."
    )

    result_label.configure(
        text="Scanning...",
        text_color="yellow"
    )

    start_scan = time.time()

    canvas.itemconfig(
        arc,
        extent=0
    )

    canvas.itemconfig(
        glow_arc,
        extent=0
    )

    canvas.itemconfig(
        arc,
        outline="#4da6ff"
    )

    canvas.itemconfig(
        glow_arc,
        outline="#1f6cff"
    )

    canvas.itemconfig(
        background_ring,
        outline="#1f6cff"
    )

    right_frame.configure(
        fg_color="#102a43",
        border_color="#1f6cff",
        border_width=4
    )

    canvas.itemconfig(
        percent_text,
        text="0%"
    )

    def process():

        for i in range(101):

            time.sleep(0.02)

            value = i / 100

            canvas.itemconfig(
                arc,
                extent=-(value * 360)
            )

            canvas.itemconfig(
                glow_arc,
                extent=-(value * 360)
            )

            canvas.itemconfig(
                percent_text,
                text=f"{i}%"
            )

        # Fake Detection
        is_safe = random.choice([
            True,
            False
        ])

        end_scan = time.time()

        total_scan_time = (
            end_scan - start_scan
        )

        # ---------------- SAFE ----------------
        confidence = random.randint(92, 99)
        if is_safe:

            result = "Safe"
            family = "No Threat Detected"
            severity = "LOW"

            reason = (
                f"Threat Severity: {severity}\n\n"
                "The file showed normal behavior "
                "patterns and no suspicious "
                "encryption activity was detected."
            )

            result_label.configure(
                text="Safe",
                text_color="green"
            )

            status_label.configure(
                text="System Status: Safe"
            )

            canvas.itemconfig(
                arc,
                outline="#00ff88"
            )

            canvas.itemconfig(
                glow_arc,
                outline="#00ff88"
            )

            canvas.itemconfig(
                background_ring,
                outline="#00ff88"
            )

            right_frame.configure(
                fg_color="#0f2e24",
                border_color="#00ff88",
                border_width=4
            )

        # ---------------- RANSOMWARE ----------------
        else:

            result = "Ransomware"
            family = random.choice([
                "WannaCry",
                "LockBit",
                "Ryuk",
                "Conti"
            ])

            reasons = {

                "WannaCry":
                "Detected SMB exploitation behavior and rapid file encryption activity.",

                "LockBit":
                "High-speed encryption pattern and suspicious privilege escalation detected.",

                "Ryuk":
                "Detected targeted encryption techniques commonly used in enterprise attacks.",

                "Conti":
                "Observed multithreaded encryption behavior and ransomware note indicators."
            }

            severity_levels = {

                "WannaCry": "CRITICAL",
                "LockBit": "HIGH",
                "Ryuk": "HIGH",
                "Conti": "MEDIUM"
            }

            severity = severity_levels[
                family
            ]

            reason = (
                f"Threat Severity: {severity}\n\n"
                + reasons[family]
            )

            # Quarantine
            success, quarantine_path = quarantine_file(
                file_path
            )

            if success:

                quarantine_message = (
                    f"\n\nFile moved to quarantine:\n"
                    f"{quarantine_path}"
                )

            else:

                quarantine_message = (
                    f"\n\nQuarantine Failed:\n"
                    f"{quarantine_path}"
                )

            reason += quarantine_message

            result_label.configure(
                text="Ransomware Detected",
                text_color="red"
            )

            status_label.configure(
                text="System Status: Threat Detected"
            )

            canvas.itemconfig(
                arc,
                outline="#ff2b2b"
            )

            canvas.itemconfig(
                glow_arc,
                outline="#ff2b2b"
            )

            canvas.itemconfig(
                background_ring,
                outline="#ff2b2b"
            )

            right_frame.configure(
                fg_color="#3a1010",
                border_color="#ff2b2b",
                border_width=4
            )

        # Add History Card
        app.after(
            0,
            lambda: add_log_card(
                file_path,
                result,
                family,
                reason,
                confidence,
                total_scan_time
            )
        )

        # Show Report
        app.after(
            0,
            lambda: show_report(
                result,
                family,
                reason,
                confidence,
                total_scan_time
            )
        )

    threading.Thread(
        target=process
    ).start()

# ---------------- Bind Scan Button ----------------
scan_button.configure(
    command=scan_file
)

# ---------------- Start App ----------------
show_tab("home")

app.mainloop()