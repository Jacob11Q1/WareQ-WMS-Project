# 🚀 WareQ WMS Project

![WareQ Banner](https://github.com/Jacob11Q1/WareQ-WMS-Project/blob/main/assets/banner.gif)

> **Warehouse Management System (WMS)** built with Django to manage tasks, inventory, and users efficiently.

---

## 🎯 Project Overview

**WareQ WMS** is a modern, **full-stack Django application** that provides a clean interface to manage warehouse operations, tasks, and categories. It demonstrates:

- User authentication (login & registration)
- Dynamic CRUD operations with **AJAX**
- API integration
- Fully responsive design (desktop, tablet, mobile)
- Form validation & security features (CSRF, SQL injection protection)

---

## ✨ Features

### 🛡 User Authentication
- Secure registration & login system
- Password hashing and session management
- Input validation to prevent attacks

### 📊 Dashboard & CRUD Operations
- Add, edit, delete tasks or items
- Categorize items and tasks
- Real-time updates without full page reloads using AJAX

### 🌐 API Endpoint
- REST API to fetch user-specific tasks/items in JSON
- Example endpoint: `/api/items/`

### 📱 Responsive Design
- Fully responsive UI using **Bootstrap**
- Compatible with desktop, tablet, and mobile

### 🔒 Security
- CSRF protection enabled
- Input validation to prevent SQL injection
- Secure authentication

---

## 🗂 Folder Structure

wareq_project/
│
├── main/
│ ├── migrations/
│ ├── templates/
│ ├── static/
│ ├── admin.py
│ ├── models.py
│ ├── views.py
│ └── urls.py
│
├── wareq_project/
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
│
├── docs/
│ ├── ERD.png
│ └── wireframes/
│
├── manage.py
└── README.md


👨‍💻 Author:
      -- Jacob Qumsiyeh
      -- Email: qumsiyeh37@gmail.com
      -- Phone: +972597298205
      -- GitHub: Jacob11Q1
      -- Instagram: jacob1q11
