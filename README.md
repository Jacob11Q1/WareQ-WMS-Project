# WareQ WMS Project
**Full Stack Django Warehouse Management System (WMS)**

---

## 🚀 Project Overview
WareQ WMS is a **Django-based Warehouse Management System** designed to help manage tasks, products, and inventory efficiently.  
This project demonstrates:  
- User authentication (Login/Registration)  
- Dynamic CRUD operations with AJAX  
- API integration  
- Fully responsive design  
- Secure form handling with CSRF protection  

---

## 🛠 Features
1. **User Authentication**
   - Registration & Login
   - Password hashing
   - Session management

2. **Dashboard & CRUD**
   - Add, edit, delete tasks/items
   - Real-time updates using AJAX
   - Categorize tasks/items

3. **API Endpoint**
   - REST API to fetch user-specific data in JSON

4. **About Page**
   - Project info and developer details

5. **Responsive Design**
   - Works on Desktop, Tablet, Mobile

6. **Security**
   - CSRF protection
   - Form validation

---

## 📂 Folder Structure
wareq_project/
│
├── main/ # Main app
│ ├── migrations/
│ ├── templates/
│ ├── static/
│ ├── admin.py
│ ├── models.py
│ ├── views.py
│ └── urls.py
│
├── wareq_project/ # Project settings
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
│
├── docs/ # Documentation
│ ├── ERD.png
│ └── wireframes/
│
├── manage.py
└── README.md

🔗 API Endpoints

GET /api/items/ → Returns JSON of user-specific items/tasks

📌 Wireframes & ERD

ERD: docs/ERD.png

Wireframes: docs/wireframes/

💻 Tech Stack

Backend: Django 5.2, Python 3.13

Frontend: HTML, CSS, Bootstrap, JavaScript (AJAX)

Database: MySQL

Deployment: AWS (Elastic Beanstalk / EC2)


📝 Future Improvements:

-- Implement user roles (Admin, Staff)
-- Add notifications / email system
-- Advanced inventory reports
-- Dark/Light mode toggle


👨‍💻 Author:

-- Jacob Qumsiyeh
-- Email: qumsiyeh37@gmail.com
-- Phone: +972597298205
-- GitHub: Jacob11Q1
-- Instagram: jacob1q11
