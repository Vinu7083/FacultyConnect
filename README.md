# FacultyConnect

A web-based application built with Flask and MySQL for managing faculty, courses, student registrations, and feedback in an educational institution.

## Features

### Admin Dashboard
- View and manage faculty members
- Assign courses to faculty
- Review and approve leave requests
- Reset faculty leave balances
- View student feedback and ratings for a faculty

### Faculty Portal
- View assigned courses and timetable
- Apply for leaves
- Track leave status and available leave balance
- View student registrations for courses

### Student Portal
- Register/Unregister for courses
- View registered courses
- Submit feedback for faculty
- Track academic progress

## Technology Stack

- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Session-based with bcrypt password hashing

## Database Schema

- `Faculty`: Stores faculty information and credentials
- `Student`: Stores student information and credentials
- `Handles_Courses`: Maps faculty to their assigned courses
- `Registration`: Tracks student course registrations
- `Feedback`: Stores student feedback for faculty
- `Leaves_Taken`: Manages faculty leave applications
- `Timetable`: Manages course schedules

## Security Features

- Password hashing using bcrypt
- Session-based authentication
- Role-based access control
- SQL injection Prevention


## API Endpoints

### Admin Routes
- `/admin` - Admin dashboard
- `/api/faculty/<id>` - Get faculty details
- `/api/leave/<id>/<action>` - Handle leave requests
- `/assign-course` - Assign courses to faculty

### Faculty Routes
- `/api/timetable/<id>` - Get faculty timetable
- `/api/leave/apply` - Apply for leave
- `/api/faculty/<id>/reset-leaves` - Reset leave balance

### Student Routes
- `/api/courses/available` - List available courses
- `/api/courses/registered` - View registered courses
- `/api/courses/register/<id>` - Register for a course
- `/api/feedback/submit` - Submit faculty feedback


###System Requirements:

Python 3.8+
MySQL 8.0+
Windows 10/11


## Setup Instructions

1. Create MySQL database:
```bash
mysql -u root -p < setup.sql

2. Install dependencies and necessary packages
pip install Flask
pip install flask-mysqldb
pip install mysqlclient
pip install bcrypt

3. Configure the database:
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'faculty_management'

4. Run the application:
  python app.py
