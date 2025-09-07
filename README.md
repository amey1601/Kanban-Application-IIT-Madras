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
- **Bootstrap 5**: Modern CSS framework for responsive design
- **Font Awesome**: Icon library for enhanced UI
- **Chart.js**: Interactive charts for analytics (fixed sizing issues)
- **Vanilla JavaScript**: No additional frameworks required

### Authentication Pages
- **Login Page**: Secure user authentication with password visibility toggle
- **Signup Page**: User registration with real-time password validation
- **Password Recovery**: OTP-based reset with countdown timer and resend functionality

## 📂 Project Structure

```
kanban-app/
├── app.py                    # Flask backend with authentication
├── requirements.txt          # Python dependencies
├── kanban.db                # SQLite database (auto-created)
├── templates/
│   ├── index.html           # Main Kanban board (authenticated)
│   ├── summary.html         # Analytics dashboard (authenticated)
│   ├── login.html           # Login page
│   ├── signup.html          # Registration page
│   └── forgot_password.html # Password recovery with OTP
└── README.md                # This comprehensive guide
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)


## 👤 User Authentication Flow

### Registration Process
1. User provides username, email, phone, and password
2. Password validation with real-time requirements check
3. Account creation with automatic default lists
4. Automatic login after successful registration

### Login Process
1. Username and password authentication
2. Session establishment for authenticated access
3. Redirect to personal Kanban board

### Password Recovery
1. Enter phone number associated with account
2. Receive 6-digit OTP (simulated in console for demo)
3. Enter OTP with 5-minute countdown timer
4. Set new password and automatic redirect to login

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
