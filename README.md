# Doctor Appointment System

A complete, full-stack web application for managing doctor appointments built with Flask, Bootstrap, and SQLite.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Default Credentials](#default-credentials)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Screenshots](#screenshots)
- [Assignment Compliance](#assignment-compliance)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

The Doctor Appointment System is a comprehensive web application designed for the Web Technology (BIT233) assignment. It enables patients to book appointments with qualified doctors and allows doctors to manage their appointments efficiently.

**Assignment Details:**
- **Course:** Web Technology (BIT233)
- **Project Type:** Full-Stack Website Development
- **Academic Year:** Second Year / Third Semester
- **Institution:** Texas College of Management & IT

## ✨ Features

### For Patients
- ✅ User registration and authentication
- ✅ Browse available doctors by specialization
- ✅ Book appointments with preferred doctors
- ✅ View all appointments (pending, confirmed, completed, cancelled)
- ✅ Cancel appointments
- ✅ Update profile information
- ✅ Responsive dashboard with statistics

### For Doctors
- ✅ Doctor registration with professional details
- ✅ View all appointment requests
- ✅ Confirm or reject appointments
- ✅ Mark appointments as completed
- ✅ Update professional information
- ✅ Dashboard with appointment statistics

### Security Features
- 🔒 Password hashing using Werkzeug
- 🔒 Session-based authentication
- 🔒 Protected routes
- 🔒 SQL injection prevention through SQLAlchemy ORM

### UI/UX Features
- 📱 Fully responsive design (mobile, tablet, desktop)
- 🎨 Modern, professional interface
- ⚡ Fast loading times
- 🔍 Search functionality for doctors
- 🎯 Client-side form validation
- 💬 Flash messages for user feedback

## 🛠 Technologies Used

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Custom styling
- **Bootstrap 5.3.0** - Responsive framework
- **JavaScript** - Client-side scripting
- **jQuery 3.6.0** - DOM manipulation
- **Bootstrap Icons** - Icon library

### Backend
- **Python 3.8+** - Programming language
- **Flask 2.3.3** - Web framework
- **Flask-SQLAlchemy 3.0.5** - ORM for database
- **Werkzeug 2.3.7** - Password hashing

### Database
- **SQLite** - Lightweight database

## 📦 Prerequisites

Before running this application, ensure you have:

- Python 3.8 or higher installed
- pip (Python package manager)
- Git (for cloning the repository)
- A modern web browser (Chrome, Firefox, Safari, Edge)

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/doctor-appointment-system.git
cd doctor-appointment-system
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database

The database will be automatically created when you first run the application. Sample data (3 doctors and 1 patient) will be inserted.

## ▶️ Running the Application

### Start the Flask Server

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## 🔑 Default Credentials

### Patient Account
- **Username:** patient1
- **Password:** patient123

### Doctor Accounts
1. **Dr. Rajesh Sharma (Cardiologist)**
   - Username: dr_sharma
   - Password: doctor123

2. **Dr. Priya Patel (Pediatrician)**
   - Username: dr_patel
   - Password: doctor123

3. **Dr. Amit Kumar (Orthopedic)**
   - Username: dr_kumar
   - Password: doctor123

## 📁 Project Structure

```
doctor_appointment_system/
│
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── .gitignore                     # Git ignore file
├── README.md                      # Project documentation
│
├── static/                        # Static files
│   ├── css/
│   │   └── style.css             # Custom styles
│   ├── js/
│   │   └── script.js             # JavaScript validation
│   └── images/                    # Images (if any)
│
├── templates/                     # HTML templates
│   ├── base.html                 # Base template
│   ├── index.html                # Home page
│   ├── login.html                # Login page
│   ├── register.html             # Registration page
│   ├── patient_dashboard.html    # Patient dashboard
│   ├── doctor_dashboard.html     # Doctor dashboard
│   ├── doctors.html              # Doctors list
│   ├── book_appointment.html     # Appointment booking
│   ├── profile.html              # User profile
│   ├── edit_profile.html         # Edit profile
│   ├── 404.html                  # 404 error page
│   └── 500.html                  # 500 error page
│
└── doctor_appointment.db          # SQLite database (created on first run)
```

## 🗃 Database Schema

### Users Table
- `id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `password` (Hashed)
- `full_name`
- `phone`
- `user_type` (patient/doctor)
- `created_at`

### Doctors Table
- `id` (Primary Key)
- `user_id` (Foreign Key → Users)
- `specialization`
- `qualification`
- `experience`
- `consultation_fee`
- `available_days`
- `available_time`

### Appointments Table
- `id` (Primary Key)
- `patient_id` (Foreign Key → Users)
- `doctor_id` (Foreign Key → Doctors)
- `appointment_date`
- `appointment_time`
- `reason`
- `status` (Pending/Confirmed/Completed/Cancelled)
- `created_at`

### Database Relationships
- **One-to-Many:** User → Appointments (as patient)
- **One-to-One:** User → Doctor (for doctor accounts)
- **One-to-Many:** Doctor → Appointments

## 📸 Screenshots

### Home Page
![Home Page](screenshots/home.png)

### Registration Page
![Registration](screenshots/register.png)

### Login Page
![Login](screenshots/login.png)

### Patient Dashboard
![Patient Dashboard](screenshots/patient-dashboard.png)

### Doctor Dashboard
![Doctor Dashboard](screenshots/doctor-dashboard.png)

### Doctors List
![Doctors List](screenshots/doctors-list.png)

### Book Appointment
![Book Appointment](screenshots/book-appointment.png)

### Profile Page
![Profile](screenshots/profile.png)

*Note: Take screenshots of your running application and place them in a `screenshots/` folder*

## ✅ Assignment Compliance

This project fulfills all requirements of the Web Technology (BIT233) assignment:

### Task 1: Theoretical Analysis (40 Marks)
- Comprehensive documentation covering all topics
- Detailed explanations of web technologies
- Code examples and diagrams included

### Task 2: Website Development Project (60 Marks)

#### Frontend (10 marks)
- ✅ HTML5 semantic elements
- ✅ Responsive CSS with Bootstrap
- ✅ JavaScript form validation
- ✅ Modern webpage layouts
- ✅ 5+ interconnected pages

#### Backend (12 marks)
- ✅ Flask framework with MVC pattern
- ✅ Jinja2 templating
- ✅ Flask routing and URL handling
- ✅ Database operations (CRUD)
- ✅ User authentication and sessions
- ✅ Password hashing

#### Database (4 marks)
- ✅ 3 related tables (Users, Doctors, Appointments)
- ✅ Proper relationships (One-to-Many, One-to-One)
- ✅ Data validation

#### Documentation & Deployment (15 marks)
- ✅ Clean, commented code
- ✅ GitHub repository
- ✅ Comprehensive README
- ✅ Installation instructions
- ✅ User manual

### Bonus Features Implemented
- ✅ Admin-like features for doctors (+4 marks)
- ✅ Advanced search and filters (+3 marks)
- ✅ User roles and permissions (+4 marks)
- ✅ Responsive design excellence (+3 marks)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Your Name**
- LCID: Your_LCID
- Course: BIT Second Year
- Semester: Third Semester
- Email: your.email@example.com

## 🙏 Acknowledgments

- Texas College of Management & IT
- Mr. Ashish Gautam (PhD Scholar) - Course Lecturer
- Bootstrap team for the excellent framework
- Flask community for comprehensive documentation

## 📞 Support

For any queries or support, please contact:
- Email: your.email@example.com
- GitHub Issues: [Create an issue](https://github.com/your-username/doctor-appointment-system/issues)

---

**Note:** This project was developed as part of the Web Technology (BIT233) course assignment at Texas College of Management & IT, Kathmandu.

**Date:** January 2026