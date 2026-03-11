

# 🚚 Courier Management System

A web-based application that helps administrators manage courier shipments and allows customers to track their courier status using a unique tracking ID. The system also provides customer support features such as complaint submission and feedback.

---

# ⚙️ Tech Stack

**Frontend**

* HTML
* CSS
* JavaScript

**Backend**

* Python Flask

**Database**

* SQLite

**Libraries**

* ReportLab (PDF generation)
* Chart.js (analytics visualization)

---

# ✨ Features

* Admin login and dashboard
* Add, update, and delete courier records
* Automatic tracking ID generation
* Customer courier tracking
* Complaint submission system
* Customer feedback system
* Courier analytics dashboard
* PDF receipt generation

---

# 🖥️ Working

The Courier Management System allows the **admin to manage courier shipments** through the admin dashboard. The admin can add courier details, generate a tracking ID, update courier status, and view complaints or feedback from customers. Customers can enter the tracking ID to check the delivery status of their courier. The system stores and manages all information using an SQLite database.

---

# ▶️ Steps to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/courier-management-system.git
```

---

### 2. Open the Project Folder

```bash
cd courier-management-system
```

---

### 3. Install Required Libraries

```bash
pip install flask
pip install reportlab
```

---

### 4. Run the Application

```bash
python app.py
```

---

### 5. Open in Browser

```
http://127.0.0.1:5000
```

---

# 🔐 Admin Login

```
Username: admin
Password: admin123
```

---

# 📂 Project Structure

```
CourierManagementSystem
│
├── app.py
├── database.db
│
├── templates
│   ├── index.html
│   ├── login.html
│   ├── admin.html
│   ├── customer.html
│   ├── track.html
│   ├── service.html
│   ├── complaints.html
│   └── feedback.html
│
└── static
    ├── style.css
    └── script.js
```

---

# 🚀 Future Improvements

* Email notifications for courier updates
* SMS alerts for shipment tracking
* GPS-based courier tracking
* Mobile application version

---
