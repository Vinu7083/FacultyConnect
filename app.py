from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import bcrypt  # Import bcrypt for password hashing

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Vinod@2802'
app.config['MYSQL_DB'] = 'faculty_management'

mysql = MySQL(app)

# Helper function to hash passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

password = 'faculty'  # Replace with the desired password
hashed_password = hash_password(password)
print(hashed_password.decode('utf-8'))  # Print the hashed password

# Helper function to verify passwords
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Decorator for login-required routes
def login_required(f):
    def wrap(*args, **kwargs):
        if 'loggedin' not in session:
            return jsonify({'error': 'Unauthorized'}), 403
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

# Login Route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']
        print(f"Login Attempt: username={username}, user_type={user_type}")  # Debugging

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        if user_type == 'admin':
            cursor.execute('SELECT * FROM Faculty WHERE username = %s AND is_admin = TRUE', (username,))
        elif user_type == 'faculty':
            cursor.execute('SELECT * FROM Faculty WHERE username = %s', (username,))
        elif user_type == 'student':
            cursor.execute('SELECT * FROM Student WHERE username = %s', (username,))

        user = cursor.fetchone()

        if user and verify_password(password, user['password']):  # Verify hashed password
            session['loggedin'] = True
            session['username'] = user['username']
            session['user_type'] = user_type
            session['user_id'] = user['Faculty_id'] if user_type != 'student' else user['S_id']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        user_type = session['user_type']
        if user_type == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif user_type == 'faculty':
            faculty_id = session.get('user_id')

            # Fetch timetable data for the logged-in faculty
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('''
                SELECT t.Faculty_id, t.Course_id, t.Room_No, t.Timeslot, t.Day, hc.Course_Name
                FROM Timetable t
                JOIN Handles_Courses hc ON t.Course_id = hc.Course_id
                WHERE t.Faculty_id = %s
                ORDER BY FIELD(t.Day, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'), t.Timeslot
            ''', (faculty_id,))
            timetable = cursor.fetchall()

            # Fetch leave requests for the logged-in faculty
            cursor.execute('''
                SELECT Leave_id, Faculty_id, DATE_FORMAT(Leave_Date, '%%Y-%%m-%%d') as Leave_Date, Approval_Status
                FROM Leaves_Taken
                WHERE Faculty_id = %s
            ''', (faculty_id,))
            leaves = cursor.fetchall()

            # Fetch available leaves for the faculty
            cursor.execute('SELECT available_leaves FROM Faculty WHERE Faculty_id = %s', (faculty_id,))
            available_leaves = cursor.fetchone()['available_leaves']

            cursor.close()

            return render_template('faculty_dashboard.html', timetable=timetable, leaves=leaves, available_leaves=available_leaves)
        elif user_type == 'student':
            # Fetch student's registered courses
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('''
                SELECT hc.Course_id, hc.Course_Name, f.Name AS Faculty_Name, f.Faculty_id
                FROM Registration r
                JOIN Handles_Courses hc ON r.Course_id = hc.Course_id
                JOIN Faculty f ON hc.Faculty_id = f.Faculty_id
                WHERE r.S_id = %s
            ''', (session.get('user_id'),))
            registered_courses = cursor.fetchall()
            cursor.close()

            # Debugging: Print the registered_courses data
            print(registered_courses)

            return render_template('student_dashboard.html', registered_courses=registered_courses)
    return redirect(url_for('login'))
"""
# Admin APIs
@app.route('/admin')
@login_required
def admin_dashboard():
    if session.get('user_type') != 'admin':
        return redirect(url_for('login'))

    db = mysql.connection
    cursor = db.cursor(MySQLdb.cursors.DictCursor)

    # Fetch faculties with grouped courses
    cursor.execute('''
        SELECT 
            f.Faculty_id,
            f.Name AS Faculty_Name,
            f.Designation,
            f.Phone_No,
            f.Joining_Date,
            f.available_leaves,
            GROUP_CONCAT(CONCAT(hc.Course_Name, ' (', hc.Credits, ' Credits)') SEPARATOR ', ') AS Courses
        FROM Faculty f
        LEFT JOIN Handles_Courses hc ON f.Faculty_id = hc.Faculty_id
        GROUP BY f.Faculty_id
        ORDER BY f.Faculty_id
    ''')
    faculties = cursor.fetchall()

    # Fetch leave requests with faculty names
    cursor.execute('''
        SELECT lt.Leave_id, f.Name AS Faculty_Name, lt.Leave_Date, lt.Approval_Status
        FROM Leaves_Taken lt
        JOIN Faculty f ON lt.Faculty_id = f.Faculty_id
        WHERE lt.Approval_Status = 'Pending'
    ''')
    leave_requests = cursor.fetchall()

    # Fetch feedback data
    cursor.execute('''
        SELECT fb.Feedback_id, f.Name AS Faculty_Name, s.Name AS Student_Name, fb.Rating, fb.Date
        FROM Feedback fb
        JOIN Faculty f ON fb.Faculty_id = f.Faculty_id
        JOIN Gives g ON fb.Feedback_id = g.Feedback_id
        JOIN Student s ON g.S_id = s.S_id
    ''')
    feedbacks = cursor.fetchall()

    cursor.close()

    return render_template('admin_dashboard.html', faculties=faculties, leave_requests=leave_requests, feedbacks=feedbacks)
"""

@app.route('/admin')
@login_required
def admin_dashboard():
    if session.get('user_type') != 'admin':
        return redirect(url_for('login'))

    db = mysql.connection
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    
    # Fetch faculties with grouped courses
    cursor.execute('''
        SELECT 
            f.Faculty_id,
            f.Name AS Faculty_Name,
            f.Designation,
            f.Phone_No,
            f.Joining_Date,
            f.available_leaves,
            GROUP_CONCAT(CONCAT(hc.Course_Name, ' (', hc.Credits, ' Credits)') SEPARATOR ', ') AS Courses
        FROM Faculty f
        LEFT JOIN Handles_Courses hc ON f.Faculty_id = hc.Faculty_id
        GROUP BY f.Faculty_id
        ORDER BY f.Faculty_id
    ''')
    faculties = cursor.fetchall()
    
    # Fetch leave requests with faculty names
    cursor.execute('''
        SELECT lt.Leave_id, f.Name AS Faculty_Name, lt.Leave_Date, lt.Approval_Status
        FROM Leaves_Taken lt
        JOIN Faculty f ON lt.Faculty_id = f.Faculty_id
        WHERE lt.Approval_Status = 'Pending'
    ''')
    leave_requests = cursor.fetchall()

    # Fetch feedback data
    cursor.execute('''
            SELECT 
                f.Name AS Faculty_Name,
                fb.Rating,
                fb.Date
            FROM Feedback fb
            INNER JOIN Faculty f ON fb.Faculty_id = f.Faculty_id
            ORDER BY fb.Date DESC
            LIMIT 10
        ''')
    feedbacks = cursor.fetchall()

    cursor.close()
    
    return render_template('admin_dashboard.html', faculties=faculties, leave_requests=leave_requests, feedbacks=feedbacks)
    """
    try:
        # Fetch faculties with courses and feedback stats
        cursor.execute('''
            SELECT 
                f.Faculty_id,
                f.Name AS Faculty_Name,
                f.Designation,
                f.Phone_No,
                f.Joining_Date,
                f.available_leaves,
                GROUP_CONCAT(DISTINCT CONCAT(hc.Course_Name, ' (', hc.Credits, ' Credits)') SEPARATOR ', ') AS Courses,
                COUNT(DISTINCT fb.Feedback_id) as feedback_count,
                ROUND(AVG(fb.Rating), 2) as avg_rating
            FROM Faculty f
            LEFT JOIN Handles_Courses hc ON f.Faculty_id = hc.Faculty_id
            LEFT JOIN Feedback fb ON f.Faculty_id = fb.Faculty_id
            GROUP BY f.Faculty_id
            ORDER BY f.Faculty_id
        ''')
        faculties = cursor.fetchall()

        # Fetch pending leave requests
        cursor.execute('''
            SELECT 
                fb.Feedback_id,
                f.Name AS Faculty_Name,
                fb.Rating,
                fb.Date
            FROM Feedback fb
            INNER JOIN Faculty f ON fb.Faculty_id = f.Faculty_id
            ORDER BY fb.Date DESC
            LIMIT 10
        ''')
        leave_requests = cursor.fetchall()

        # Fetch recent feedback with course info
        cursor.execute('''
            SELECT DISTINCT
                fb.Feedback_id,
                f.Faculty_id,
                f.Name AS Faculty_Name,
                hc.Course_Name,
                fb.Rating,
                fb.Date
            FROM Feedback fb
            INNER JOIN Faculty f ON fb.Faculty_id = f.Faculty_id
            INNER JOIN Handles_Courses hc ON f.Faculty_id = hc.Faculty_id
            ORDER BY fb.Date DESC
            LIMIT 10
        ''')
        feedbacks = cursor.fetchall()

        return render_template('admin_dashboard.html',
                             faculties=faculties,
                             leave_requests=leave_requests,
                             feedbacks=feedbacks)

    except Exception as e:
        print(f"Error in admin dashboard: {str(e)}")
        return "An error occurred", 500
    finally:
        cursor.close()"""

@app.route('/api/faculty/<int:faculty_id>', methods=['GET'])
@login_required
def get_faculty_details(faculty_id):
    if session.get('user_type') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    db = mysql.connection
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT f.*, 
               GROUP_CONCAT(DISTINCT fr.Role) as roles,
               COUNT(DISTINCT hc.Course_id) as course_count,
               COUNT(DISTINCT lt.Leave_id) as leave_count
        FROM Faculty f
        LEFT JOIN Faculty_Role fr ON f.Faculty_id = fr.Faculty_id
        LEFT JOIN Handles_Courses hc ON f.Faculty_id = hc.Faculty_id
        LEFT JOIN Leaves_Taken lt ON f.Faculty_id = lt.Faculty_id
        WHERE f.Faculty_id = %s
        GROUP BY f.Faculty_id
    ''', (faculty_id,))
    
    faculty = cursor.fetchone()
    cursor.close()
    if faculty:
        return jsonify(faculty)
    return jsonify({'error': 'Faculty not found'}), 404

@app.route('/api/leave/<int:leave_id>/<action>', methods=['POST'])
@login_required
def handle_leave(leave_id, action):
    if session.get('user_type') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    if action not in ['approve', 'reject']:
        return jsonify({'error': 'Invalid action'}), 400

    db = mysql.connection
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    status = 'Approved' if action == 'approve' else 'Rejected'

    try:
        # Update the leave status
        cursor.execute(
            'UPDATE Leaves_Taken SET Approval_Status = %s WHERE Leave_id = %s',
            (status, leave_id)
        )

        # If the leave is approved, decrement available_leaves
        if action == 'approve':
            cursor.execute('''
                UPDATE Faculty
                SET available_leaves = available_leaves - 1
                WHERE Faculty_id = (SELECT Faculty_id FROM Leaves_Taken WHERE Leave_id = %s)
            ''', (leave_id,))

        db.commit()
        return jsonify({'message': f'Leave {status.lower()} successfully'})
    except Exception as e:
        print("Error handling leave:", str(e))  # Debugging
        db.rollback()
        return jsonify({'error': 'Database error'}), 500
    finally:
        cursor.close()

"""

@app.route('/api/courses/assign', methods=['POST'])
@login_required
def assign_course():
    if session.get('user_type') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.json
    faculty_id = data.get('faculty_id')
    course_id = data.get('course_id')
    course_name = data.get('course_name')
    credits = data.get('credits')
    
    if not faculty_id or not course_id or not course_name or not credits:
        return jsonify({'error': 'Missing required fields'}), 400

    db = mysql.connection
    cursor = db.cursor()
    try:
        # Check if the course ID already exists
        cursor.execute('SELECT 1 FROM Handles_Courses WHERE Course_id = %s', (course_id,))
        if cursor.fetchone():
            return jsonify({'error': 'Course ID already exists'}), 400

        # Insert the new course assignment
        cursor.execute('''
            INSERT INTO Handles_Courses (Faculty_id, Course_id, Course_Name, Credits)
            VALUES (%s, %s, %s, %s)
        ''', (faculty_id, course_id, course_name, credits))

        db.commit()
        return jsonify({'message': 'Course assigned successfully'})
    except Exception as e:
        print("Error assigning course:", str(e))  # Debugging
        db.rollback()
        return jsonify({'error': 'Database error'}), 500
    finally:
        cursor.close()       
"""

@app.route('/assign-course', methods=['POST'])
@login_required
def assign_course():
    data = request.get_json()
    cursor = mysql.connection.cursor()
    try:
        cursor.execute('''
            INSERT INTO Handles_Courses 
            (Faculty_id, Course_id, Course_Name, Credits,semester_id)
            VALUES (%s, %s, %s, %s, %s)
        ''', (
            data['faculty_id'], 
            data['course_id'], 
            data['course_name'], 
            data['credits'],
            data['semester']
        ))
        mysql.connection.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    finally:
        cursor.close()

@app.route('/api/courses/unregister/<int:course_id>', methods=['POST'])
@login_required
def unregister_course(course_id):
    if session.get('user_type') != 'student':
        return jsonify({'error': 'Unauthorized'}), 403

    student_id = session.get('user_id')

    db = mysql.connection
    cursor = db.cursor()
    try:
        # Check if the student is registered for the course
        cursor.execute('''
            SELECT 1 FROM Registration WHERE S_id = %s AND Course_id = %s
        ''', (student_id, course_id))
        if not cursor.fetchone():
            return jsonify({'error': 'You are not registered for this course'}), 400

        # Unregister the student from the course
        cursor.execute('''
            DELETE FROM Registration WHERE S_id = %s AND Course_id = %s
        ''', (student_id, course_id))
        db.commit()
        return jsonify({'message': 'Course unregistered successfully'})
    except Exception as e:
        print("Error unregistering course:", str(e))  # Debugging
        db.rollback()
        return jsonify({'error': 'Database error'}), 500
    finally:
        cursor.close()
        
 #apply leaves       
@app.route('/api/leave/apply', methods=['POST'])
@login_required
def apply_leave():
    if session.get('user_type') != 'faculty':
        return jsonify({'error': 'Unauthorized'}), 403

    leave_date = request.json.get('leave_date')
    faculty_id = session.get('user_id')

    if not leave_date:
        return jsonify({'error': 'Leave date is required'}), 400

    db = mysql.connection
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    try:
        # Check if the faculty has available leaves
        cursor.execute('SELECT available_leaves FROM Faculty WHERE Faculty_id = %s', (faculty_id,))
        result = cursor.fetchone()

        if not result:
            return jsonify({'error': 'Faculty not found'}), 404

        available_leaves = result['available_leaves']

        if available_leaves <= 0:
            return jsonify({'error': 'No available leaves left'}), 400

        # Insert leave application into the Leaves_Taken table
        cursor.execute('''
            INSERT INTO Leaves_Taken (Faculty_id, Leave_Date, Approval_Status)
            VALUES (%s, %s, %s)
        ''', (faculty_id, leave_date, 'Pending'))

        db.commit()
        return jsonify({'message': 'Leave application submitted successfully'})
    except Exception as e:
        print("Error submitting leave application:", str(e))  # Debugging
        db.rollback()
        return jsonify({'error': 'Database error'}), 500
    finally:
        cursor.close()
        
#reset leaves
@app.route('/api/faculty/<int:faculty_id>/reset-leaves', methods=['POST'])
@login_required
def reset_leaves(faculty_id):
    if session.get('user_type') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    db = mysql.connection
    cursor = db.cursor()
    try:
        # Reset available_leaves to 5
        cursor.execute('UPDATE Faculty SET available_leaves = 5 WHERE Faculty_id = %s', (faculty_id,))
        db.commit()
        return jsonify({'message': 'Available leaves reset successfully'})
    except Exception as e:
        print("Error resetting leaves:", str(e))  # Debugging
        db.rollback()
        return jsonify({'error': 'Database error'}), 500
    finally:
        cursor.close()
                
# Faculty APIs
@app.route('/api/timetable/<int:faculty_id>')
@login_required
def get_timetable(faculty_id):
    if session.get('user_type') != 'faculty' or session.get('user_id') != faculty_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db = mysql.connection
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT t.*, hc.Course_Name
        FROM Timetable t
        JOIN Handles_Courses hc ON t.Course_id = hc.Course_id
        WHERE t.Faculty_id = %s
        ORDER BY FIELD(t.Day, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'), t.Timeslot
    ''', (faculty_id,))
    
    timetable = cursor.fetchall()
    cursor.close()
    return jsonify(timetable)

# Student APIs

#available courses for student
@app.route('/api/courses/available')
@login_required
def get_available_courses():
    if session.get('user_type') != 'student':
        return jsonify({'error': 'Unauthorized'}), 403

    student_id = session.get('user_id')
    
    # Fetch the student's semester from the database
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT semester_id FROM Student WHERE S_id = %s', (student_id,))
    student = cursor.fetchone()

    if not student:
        return jsonify({'error': 'Student not found'}), 404

    semester_id = student['semester_id']

    # Fetch courses for the student's semester
    cursor.execute('''
    SELECT 
        hc.Course_id, 
        hc.Course_Name, 
        hc.Credits, 
        f.Name AS Faculty_Name
    FROM Handles_Courses hc
    JOIN Faculty f ON hc.Faculty_id = f.Faculty_id
    WHERE hc.semester_id = 5  -- Hardcoded for testing
''')
    courses = cursor.fetchall()
    cursor.close()

    return jsonify(courses)

@app.route('/api/courses/registered')
@login_required
def get_registered_courses():
    if session.get('user_type') != 'student':
        return jsonify({'error': 'Unauthorized'}), 403

    student_id = session.get('user_id')
    db = mysql.connection
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute('''
            SELECT hc.Course_id, hc.Course_Name, f.Name AS Faculty_Name, f.Faculty_id
            FROM Registration r
            JOIN Handles_Courses hc ON r.Course_id = hc.Course_id
            JOIN Faculty f ON hc.Faculty_id = f.Faculty_id
            WHERE r.S_id = %s
        ''', (student_id,))
        registered_courses = cursor.fetchall()
        return jsonify(registered_courses)
    except Exception as e:
        print("Error fetching registered courses:", str(e))  # Debugging
        return jsonify({'error': 'Database error'}), 500
    finally:
        cursor.close()
        
        
@app.route('/api/courses/register/<int:course_id>', methods=['POST'])
@login_required
def register_course(course_id):
    if session.get('user_type') != 'student':
        return jsonify({'error': 'Unauthorized'}), 403
    
    student_id = session.get('user_id')
    db = mysql.connection
    cursor = db.cursor()
    try:
        # Check if the student is already registered for the course
        cursor.execute('''
            SELECT 1 FROM Registration WHERE S_id = %s AND Course_id = %s
        ''', (student_id, course_id))
        if cursor.fetchone():
            return jsonify({'error': 'Already registered for this course'}), 400
        
        # Register the student for the course
        cursor.execute('''
            INSERT INTO Registration (S_id, Course_id) VALUES (%s, %s)
        ''', (student_id, course_id))
        db.commit()
        return jsonify({'message': 'Course registration successful'})
    except Exception as e:
        print("Error during registration:", str(e))  # Debugging statement
        db.rollback()
        return jsonify({'error': 'Database error'}), 500
    finally:
        cursor.close()

"""

#give feedback
@app.route('/give_feedback/<int:faculty_id>')
@login_required
def give_feedback(faculty_id):
    if session.get('user_type') != 'student':
        return redirect(url_for('login'))
    
    # Fetch faculty details (optional, if you want to display faculty info on the feedback page)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT Name FROM Faculty WHERE Faculty_id = %s', (faculty_id,))
    faculty = cursor.fetchone()
    cursor.close()

    if not faculty:
        return render_template('error.html', error='Faculty not found'), 404

    return render_template('give_feedback.html', faculty_id=faculty_id, faculty_name=faculty['Name'])

#submit feedback
@app.route('/submit-feedback', methods=['POST'])
@login_required
def submit_feedback():
    if session.get('user_type') != 'student':
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get JSON data instead of form data
    data = request.get_json()
    faculty_id = data.get('faculty_id')
    rating = data.get('rating')
    feedback_date = data.get('feedback_date')
    student_id = session.get('user_id')

    if not all([faculty_id, rating, feedback_date]):
        return jsonify({'error': 'Missing required fields'}), 400

    db = mysql.connection
    cursor = db.cursor()
    try:
        feedback_id = cursor.lastrowid
        cursor.execute('''
            INSERT INTO Feedback (Faculty_id, Rating, Date)
            VALUES (%s, %s, %s, %s)
        ''', (feedback_id, faculty_id, rating, feedback_date))

        feedback_id = cursor.lastrowid
        cursor.execute('''
            INSERT INTO Gives (S_id, Feedback_id)
            VALUES (%s, %s)
        ''', (student_id, feedback_id))

        db.commit()
        return jsonify({'success': True, 'message': 'Feedback submitted successfully'})
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
"""

@app.route('/give_feedback/<int:faculty_id>')
@login_required
def show_feedback_form(faculty_id):
    if session.get('user_type') != 'student':
        return redirect(url_for('dashboard'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT Name FROM Faculty WHERE Faculty_id = %s', (faculty_id,))
    faculty = cursor.fetchone()
    cursor.close()
    
    return render_template('give_feedback.html', faculty_id=faculty_id, faculty_name=faculty['Name'])

@app.route('/api/feedback/submit', methods=['POST'])
@login_required
def submit_feedback():
    if session.get('user_type') != 'student':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    faculty_id = data.get('faculty_id')
    rating = data.get('rating')
    feedback_date = data.get('feedback_date')
    student_id = session.get('user_id')

    cursor = mysql.connection.cursor()
    try:
        cursor.execute('''
            INSERT INTO Feedback (Faculty_id, Rating, Date)
            VALUES (%s, %s, %s)
        ''', (faculty_id, rating, feedback_date))
        
        feedback_id = cursor.lastrowid
        
        cursor.execute('''
            INSERT INTO Gives (S_id, Feedback_id)
            VALUES (%s, %s)
        ''', (student_id, feedback_id))
        
        mysql.connection.commit()
        return jsonify({'success': True, 'message': 'Feedback submitted successfully'})
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)