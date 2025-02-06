// Admin dashboard functions
function showAssignCourseModal(facultyId) {
    const modal = document.getElementById('assignCourseModal');
    modal.style.display = 'block';
    modal.dataset.facultyId = facultyId;
}

function assignCourse(event) {
    event.preventDefault();
    const facultyId = document.getElementById('assignCourseModal').dataset.facultyId;
    const courseName = document.getElementById('courseName').value;
    const semester = document.getElementById('semester').value;
    const credits = document.getElementById('courseCredits').value;

    fetch('/api/courses/assign', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            faculty_id: facultyId,
            course_name: courseName,
            credits: parseInt(credits)
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert('Course assigned successfully');
            location.reload();
        }
    })
    .catch(error => console.error('Error:', error));
}

// Faculty dashboard functions
function showLeaveForm() {
    const modal = document.getElementById('leaveModal');
    modal.style.display = 'block';
}

function submitLeave(event) {
    event.preventDefault();
    const leaveDate = document.getElementById('leaveDate').value;

    fetch('/api/leave/apply', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            leave_date: leaveDate
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert('Leave application submitted successfully');
            location.reload();
        }
    })
    .catch(error => console.error('Error:', error));
}

function loadTimetable() {
    const facultyId = document.getElementById('facultyId').value;
    fetch(`/api/timetable/${facultyId}`)
        .then(response => response.json())
        .then(data => {
            const timetableBody = document.querySelector('#timetableTable tbody');
            timetableBody.innerHTML = '';
            data.forEach(slot => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${slot.Day}</td>
                    <td>${slot.Timeslot}</td>
                    <td>${slot.Course_Name}</td>
                    <td>${slot.Room_No}</td>
                `;
                timetableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error:', error));
}

// Student dashboard functions
function registerCourse(courseId) {
    fetch('/api/courses/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            course_id: courseId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert('Course registration successful');
            location.reload();
        }
    })
    .catch(error => console.error('Error:', error));
}

function submitFeedback(event, facultyId) {
    event.preventDefault();
    
    const rating = document.getElementById('rating').value;
    const feedbackDate = document.getElementById('feedback_date').value;

    if (!rating || !feedbackDate) {
        alert('Please fill all required fields');
        return;
    }

    fetch('/submit-feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            faculty_id: facultyId,
            rating: rating,
            feedback_date: feedbackDate
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            window.location.href = '/dashboard';
        } else {
            alert(data.error);
        }
    })
    .catch(error => {
        alert('Error submitting feedback');
    });
}

/*
function submitFeedback(facultyId) {
    const rating = document.getElementById(`rating_${facultyId}`).value;

    fetch('/api/feedback/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            faculty_id: facultyId,
            rating: parseInt(rating)
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert('Feedback submitted successfully');
            location.reload();
        }
    })
    .catch(error => console.error('Error:', error));
}
*/

// Modal handling
document.addEventListener('DOMContentLoaded', function() {
    // Close modal when clicking on X or outside the modal
    const modals = document.getElementsByClassName('modal');
    const closeButtons = document.getElementsByClassName('close');

    Array.from(closeButtons).forEach(button => {
        button.onclick = function() {
            const modal = button.closest('.modal');
            modal.style.display = 'none';
        }
    });

    window.onclick = function(event) {
        Array.from(modals).forEach(modal => {
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        });
    } 
});

document.getElementById('feedbackForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const data = {
        faculty_id: document.getElementById('facultyId').value,
        rating: document.getElementById('rating').value,
        feedback_date: document.getElementById('feedbackDate').value
    };
    
    fetch('/api/feedback/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Feedback submitted successfully');
            window.location.href = '/dashboard';
        } else {
            alert(data.error || 'Error submitting feedback');
        }
    })
    .catch(error => alert('Error submitting feedback'));
});

// Apply for a leave
function applyLeave() {
    console.log("applyLeave function triggered"); // Debugging
    const facultyId = session.get('user_id'); // Get faculty_id from session
    const leaveDate = document.getElementById('leaveDate').value;

    fetch('/api/leave/apply', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ faculty_id: facultyId, leave_date: leaveDate }),
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response from server:", data); // Debugging
        if (data.message) {
            alert(data.message);
        } else if (data.error) {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error applying for leave:', error);
        alert('An error occurred while applying for leave.');
    });
}