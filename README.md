# Kanban-Application-IIT-Madras

# Multi-User Kanban Board Application with Authentication

A comprehensive full-stack Kanban board application built with Flask, SQLite, Bootstrap, and vanilla JavaScript. This application supports multiple users with secure authentication, OTP-based password recovery, and individual task management for each user.

## 🔐 Authentication Features

### User Management
- **Secure Registration**: Username, email, phone number, and password
- **Login System**: Session-based authentication with secure password hashing
- **Password Recovery**: OTP-based password reset via phone number
- **Multi-User Support**: Each user has their own isolated task boards and data

### Security Features
- **Password Hashing**: SHA-256 encryption for secure password storage
- **Session Management**: Flask sessions for user authentication
- **OTP Verification**: 6-digit OTP with 5-minute expiry for password recovery
- **Input Validation**: Client and server-side validation for all forms

## 📱 Core Features

### Task Management (Per User)
- **Multiple Lists**: Create and manage multiple task lists (To Do, In Progress, Done, etc.)
- **Task Cards**: Add detailed cards with title, content, and deadlines
- **Drag & Drop**: Move cards between lists with intuitive drag-and-drop interface
- **Task Completion**: Mark tasks as completed with automatic timestamp tracking
- **Deadline Management**: Set deadlines and get visual indicators for overdue tasks

### Analytics & Tracking (Per User)
- **Summary Dashboard**: Comprehensive overview of individual project progress
- **Progress Tracking**: Visual progress bars for each list
- **Completion Trends**: 7-day trend chart showing completion patterns
- **Task Distribution**: Pie chart showing task distribution across lists
- **Overdue Alerts**: Automatic alerts for overdue tasks

## 🛠 Technology Stack

### Backend
- **Flask**: Python web framework for API and routing
- **SQLite**: Lightweight database with user isolation
- **Jinja2**: Template engine for HTML rendering
- **SHA-256**: Secure password hashing
- **Session Management**: Flask built-in sessions

### Frontend
- **Bootstrap 5**
- **Font Awesome**
- **Chart.js**
- **JavaScript**

### Authentication Pages
- **Login Page**
- **Signup Page**
- **Password Recovery**

```
