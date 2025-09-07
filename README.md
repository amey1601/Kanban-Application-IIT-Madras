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

### Step-by-Step Installation

1. **Create project directory:**
   ```bash
   mkdir kanban-app
   cd kanban-app
   ```

2. **Save all files in the correct structure:**
   ```
   kanban-app/
   ├── app.py
   ├── requirements.txt
   └── templates/
       ├── index.html
       ├── summary.html
       ├── login.html
       ├── signup.html
       └── forgot_password.html
   ```

3. **Install dependencies:**
   ```bash
   pip install flask
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the application:**
   - **Registration**: http://localhost:5000/signup
   - **Login**: http://localhost:5000/login
   - **Main Board**: http://localhost:5000 (after login)
   - **Analytics**: http://localhost:5000/summary (after login)

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

### Lists Table (User-Isolated)
```sql
CREATE TABLE lists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

### Cards Table (Linked to User Lists)
```sql
CREATE TABLE cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT,
    deadline DATE,
    completed BOOLEAN DEFAULT 0,
    list_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (list_id) REFERENCES lists (id)
);
```

## 🔌 API Endpoints

### Authentication Endpoints
- `POST /api/signup` - User registration
- `POST /api/login` - User authentication
- `POST /api/logout` - User logout
- `POST /api/forgot-password` - Request password reset OTP
- `POST /api/verify-otp` - Verify OTP and reset password

### Data Endpoints (Authenticated Only)
- `GET /api/lists` - Get user's lists
- `POST /api/lists` - Create new list for user
- `DELETE /api/lists/<id>` - Delete user's list
- `GET /api/cards` - Get user's cards
- `POST /api/cards` - Create new card in user's list
- `PUT /api/cards/<id>` - Update user's card
- `DELETE /api/cards/<id>` - Delete user's card
- `GET /api/summary` - Get user's analytics data

## 🎨 UI Improvements

### Fixed Issues
- **Chart Sizing**: Fixed pie chart taking too much vertical space
- **Responsive Design**: Better mobile compatibility
- **Visual Hierarchy**: Clear user identification in navigation
- **Interactive Elements**: Smooth hover effects and animations

### Authentication UI
- **Modern Design**: Gradient backgrounds and rounded corners
- **Password Validation**: Real-time requirements checking
- **OTP Interface**: User-friendly 6-digit input with timer
- **Error Handling**: Clear error messages and validation feedback

## 🔧 Configuration

### OTP Integration
Currently simulated for demo purposes. For production:

```python
def send_otp(phone, otp):
    # Integration examples:
    # Twilio SMS API
    # AWS SNS
    # Firebase SMS
    return True  # Replace with actual SMS service
```

### Security Configuration
```python
# In production, use environment variables
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key')
```

## 🚀 Deployment Options

### Local Development
```bash
python app.py
# Access at http://localhost:5000
```

### Replit.com Deployment
1. Create new Python repl
2. Upload all files maintaining directory structure
3. Install Flask: `pip install flask`
4. Run: `python app.py`
5. Replit provides public URL

### Production Deployment
- **Heroku**: Add `Procfile` with `web: python app.py`
- **PythonAnywhere**: Upload to web app directory
- **Railway/Render**: Direct deployment from repository

## 📈 Usage Guide

### Getting Started
1. **Sign Up**: Create account with username, email, phone, password
2. **Login**: Access your personal Kanban board
3. **Create Lists**: Add custom lists beyond default ones
4. **Add Tasks**: Create cards with titles, content, and deadlines
5. **Manage Tasks**: Drag-drop between lists, mark as complete
6. **View Analytics**: Check progress and trends in Summary page

### Advanced Features
- **Multi-List Management**: Create lists for different projects
- **Deadline Tracking**: Visual indicators for overdue tasks
- **Progress Monitoring**: Real-time analytics and charts
- **Password Recovery**: Secure OTP-based password reset

## 🛡️ Security Considerations

### Current Implementation
- Password hashing with SHA-256
- Session-based authentication
- Input validation and sanitization
- OTP with time-based expiry

### Production Recommendations
- Use bcrypt for password hashing
- Implement rate limiting for login attempts
- Add CSRF protection
- Use HTTPS for all communications
- Implement proper logging and monitoring

## 🐛 Troubleshooting

### Common Issues

**Authentication Problems**
- Clear browser cookies/sessions
- Check database permissions
- Verify all template files are present

**OTP Not Working**
- Check console logs for simulated SMS
- Ensure phone number format is correct
- OTP expires after 5 minutes

**Database Issues**
- Delete `kanban.db` to reset completely
- App recreates database automatically
- Each user gets isolated data

### Performance Tips
- Database includes user isolation at query level
- Charts auto-refresh every 30 seconds
- Drag-and-drop optimized for smooth experience

## 🤝 Contributing

Enhancements welcome:
1. Real SMS integration for OTP
2. Email notifications for deadlines
3. Team collaboration features
4. File attachments for cards
5. Advanced analytics and reporting

## 📄 License

MIT License - Open source and free to use.

## 🆘 Support

For issues:
1. Check browser console for JavaScript errors
2. Review Flask terminal output for backend errors
3. Ensure all files are in correct directory structure
4. Verify database permissions and creation

---

**Multi-User Task Management Made Simple!** 🎯

### Key Improvements Made:
✅ **User Authentication**: Complete login/signup system
✅ **OTP Password Recovery**: Phone-based password reset
✅ **User Isolation**: Each user has their own tasks and lists
✅ **Fixed Chart Sizing**: Proper height constraints for pie chart
✅ **Enhanced Security**: Password hashing and session management
✅ **Better UX**: Modern authentication pages with validation
