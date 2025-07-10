
# 🏨 Lomash Hotel Management System

A modern, interactive Hotel Management System GUI built using **Python Tkinter**. This project enables hotel front-desk operations such as room booking, customer details tracking, and payment via QR code—all with a visual room allocation interface.

---

## 🚀 Features

- 🔑 Customer Registration Form (Name, Contact, ID, Room Type, Dates, etc.)
- 📦 Room Allocation with floor-wise room buttons
- 💸 QR Code Generation for Payment
- 🧾 Unique Serial Number Generator
- 🧠 Real-time Room Booking Status with Blinking Indicator
- 📊 Customer Details Table
- 🖼️ Responsive UI built with Tkinter and ttk
- 🏗️ Multi-floor Room Management (up to 50 floors, 5 rooms each)

---

## 🖥️ Technologies Used

- Python 3
- Tkinter GUI Library
- `qrcode` (for QR generation)
- `PIL` (for QR image rendering)

---

## 📷 Screenshots

| Room UI | QR Code | Customer Details |
|--------|---------|------------------|
| ![room_ui](screenshots/room_ui.png) | ![qr_code](screenshots/qr_code.png) | ![customer_table](screenshots/customer_table.png) |

> 💡 Add screenshots in the `screenshots/` folder and update paths above.

---

## 🛠️ How to Run

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/lomash-hotel-management.git
cd lomash-hotel-management
```

2. **Install required packages**

```bash
pip install pillow qrcode
```

3. **Run the application**

```bash
python Lomash\ Hotel\ Management\ System.py
```

---

## 📁 Project Structure

```
lomash-hotel-management/
│
├── Lomash Hotel Management System.py     # Main Python script
├── payment_qr.png                        # QR generated during runtime
├── screenshots/                          # Add UI screenshots here (optional)
└── README.md
```

---

## 📌 Notes

- Rooms already booked blink red with the customer name displayed.
- QR codes are generated with customer name and amount.
- Serial numbers are auto-generated using customer name + room number.

---

## 🙌 Acknowledgements

Developed by **Lomash Srivastava**  
[📧 Email](mailto:lomashgroups@gmail.com) | [🌐 GitHub](https://github.com/lomashsrivastava) | [💼 LinkedIn](https://www.linkedin.com/in/lomashsrivastava)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
