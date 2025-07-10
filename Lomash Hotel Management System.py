import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import qrcode
import threading
import random

# Initialize Window
root = tk.Tk()
root.title("🏨 Hotel Management System - Nitin Residency")
root.geometry("1600x900")
root.configure(bg="#F3F4F6")

# --------- Variables ---------
name = tk.StringVar()
room_no = tk.StringVar()
floor_no = tk.StringVar()
room_type = tk.StringVar()
contact = tk.StringVar()
id_type = tk.StringVar()
id_number = tk.StringVar()
purpose = tk.StringVar()
checkin_date = tk.StringVar()
checkout_date = tk.StringVar()
total_bill = tk.StringVar()
serial_number = tk.StringVar()
room_status = {}
blinking_rooms = {}
qr_img = None

# --------- Serial Number Generator ---------
def generate_serial_number():
    return f"{name.get()[:3].upper()}{random.randint(1000, 9999)}{room_no.get()}"

# --------- Blink Effect for Booked Rooms ---------
def blink_text(floor, room, label):
    while blinking_rooms.get(f"{floor}-{room}", False):
        label.config(fg="white" if label.cget("fg") == "red" else "red")
        root.update()
        root.after(500)

# --------- Generate QR Code ---------
def generate_qr():
    global qr_img
    amount = total_bill.get()
    if not amount or not name.get():
        messagebox.showwarning("Warning", "Enter valid details before payment!")
        return

    qr = qrcode.make(f"Payment of Rs {amount} by {name.get()}")
    qr.save("payment_qr.png")
    img = Image.open("payment_qr.png").resize((150, 150))
    qr_img = ImageTk.PhotoImage(img)
    qr_label.config(image=qr_img)
    qr_label.image = qr_img
    root.after(10000, complete_payment)

# --------- Complete Payment and Allocate Room ---------
def complete_payment():
    floor = floor_no.get()
    room = room_no.get()
    key = f"{floor}-{room}"

    if key in room_status:
        messagebox.showwarning("Error", "Room is already booked!")
        return

    serial_number.set(generate_serial_number())

    room_status[key] = {
        "name": name.get(),
        "room_type": room_type.get(),
        "contact": contact.get(),
        "id_type": id_type.get(),
        "id_number": id_number.get(),
        "purpose": purpose.get(),
        "checkin_date": checkin_date.get(),
        "checkout_date": checkout_date.get(),
        "total_bill": total_bill.get(),
        "serial_number": serial_number.get()
    }

    blinking_rooms[key] = True
    update_room_display()
    update_customer_table()
    threading.Thread(target=blink_text, args=(floor, room, room_buttons[key]), daemon=True).start()

# --------- Update Room Display ---------
room_buttons = {}

def update_room_display():
    for widget in room_display.winfo_children():
        widget.destroy()

    for floor in range(1, 51):
        floor_frame = tk.Frame(room_display, bg="white", pady=2)
        floor_frame.pack(fill="x")
        tk.Label(floor_frame, text=f"Floor {floor}", font=("Arial", 10, "bold"), width=10, bg="#B0C4DE").pack(side="left")
        
        for room in range(1, 6):
            key = f"{floor}-{room}"
            room_btn = tk.Button(floor_frame, text=f"R{room}", width=5, relief="ridge")

            if key in room_status:
                room_btn.config(
                    bg="red", fg="white", text=room_status[key]["name"], 
                    font=("Arial", 8, "bold"), command=lambda f=floor, r=room: show_customer_details(f, r)
                )
            
            room_btn.pack(side="left", padx=2)
            room_buttons[key] = room_btn

# --------- Update Customer Table ---------
def update_customer_table():
    for row in customer_tree.get_children():
        customer_tree.delete(row)

    for key, details in room_status.items():
        floor, room = key.split("-")
        customer_tree.insert("", "end", values=(
            room, floor, details["name"], details["contact"], 
            details["checkin_date"], details["checkout_date"], details["serial_number"]
        ))

# --------- UI Layout ---------
frame_left = tk.Frame(root, bg="#D1E7DD", padx=10, pady=10)  # Customer Form
frame_left.grid(row=0, column=0, sticky="nsew")

frame_middle = tk.Frame(root, bg="white", padx=10, pady=10)  # Building UI
frame_middle.grid(row=0, column=1, sticky="nsew")

frame_right = tk.Frame(root, bg="#F3F4F6", padx=10, pady=10)  # Customer Table
frame_right.grid(row=0, column=2, sticky="nsew")

# --------- Registration Form ---------
fields = [
    ("Full Name", name),
    ("Room No", room_no),
    ("Floor No", floor_no),
    ("Room Type", room_type),
    ("Contact", contact),
    ("ID Type", id_type),
    ("ID Number", id_number),
    ("Purpose", purpose),
    ("Check-in Date", checkin_date),
    ("Check-out Date", checkout_date),
    ("Total Bill (Rs)", total_bill)
]

for i, (label, var) in enumerate(fields):
    ttk.Label(frame_left, text=label + ":", background="#D1E7DD").grid(row=i, column=0, sticky="w", padx=5, pady=2)
    ttk.Entry(frame_left, textvariable=var).grid(row=i, column=1, padx=5, pady=2)

ttk.Label(frame_left, text="Serial Number:", background="#D1E7DD").grid(row=len(fields), column=0, sticky="w", padx=5, pady=2)
ttk.Entry(frame_left, textvariable=serial_number, state="readonly").grid(row=len(fields), column=1, padx=5, pady=2)

ttk.Button(frame_left, text="Generate QR & Pay", command=generate_qr).grid(row=len(fields)+1, columnspan=2, pady=5)
qr_label = ttk.Label(frame_left, background="#D1E7DD")
qr_label.grid(row=len(fields)+2, columnspan=2, pady=5)

# --------- Building UI ---------
ttk.Label(frame_middle, text="Room Allocation", font=("Arial", 12, "bold"), background="white").pack()
room_display = tk.Frame(frame_middle, bg="white")
room_display.pack(fill="both", expand=True)
update_room_display()

# --------- Customer Table ---------
ttk.Label(frame_right, text="Customer Details", font=("Arial", 14, "bold"), background="#F3F4F6").pack()

columns = ("Room No", "Floor No", "Name", "Contact", "Check-in", "Check-out", "Serial No")
customer_tree = ttk.Treeview(frame_right, columns=columns, show="headings")

for col in columns:
    customer_tree.heading(col, text=col)
    customer_tree.column(col, width=120)

customer_tree.pack(fill="both", expand=True)

root.mainloop()
