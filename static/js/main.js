document.addEventListener('DOMContentLoaded', function () {
    // Load available and registered courses when the page loads
    loadAvailableCourses();
    loadRegisteredCourses();
});

// Fetch and display available courses
function loadAvailableCourses() {
    fetch('/api/courses/available')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('availableCourses');
            tableBody.innerHTML = ''; // Clear existing rows
            data.forEach(course => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${course.Course_Name}</td>
                    <td>${course.Faculty_Name}</td>
                    <td>${course.Credits}</td>
                    <td>${course.department_name}</td>
                    <td>
                        <button onclick="registerCourse(${course.Course_id})" class="action-btn">Register</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching available courses:', error));
}

// Fetch and display registered courses
function loadRegisteredCourses() {
    fetch('/api/courses/registered')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('registeredCourses').querySelector('tbody');
            tableBody.innerHTML = ''; // Clear existing rows
            data.forEach(course => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${course.Course_Name}</td>
                    <td>${course.Faculty_Name}</td>
                    <td>
                        <button onclick="unregisterCourse(${course.Course_id})" class="action-btn">Unregister</button>
                    </td>
                    <td>
                        <a href="/give_feedback/${course.Faculty_id}" class="action-btn">Give Feedback</a>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching registered courses:', error));
}

// Register for a course
function registerCourse(courseId) {
    console.log("Registering for course ID:", courseId); // Debugging

    fetch(`/api/courses/register/${courseId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {
            console.log("Registration Response:", data); // Debugging
            if (data.message) {
                alert(data.message); // Show success message
                loadAvailableCourses(); // Refresh available courses
                loadRegisteredCourses(); // Refresh registered courses
            } else if (data.error) {
                alert(data.error); // Show error message
            }
        })
        .catch(error => {
            console.error("Error registering for course:", error); // Debugging
            alert("An error occurred while registering for the course.");
        });
}

// Unregister from a course
function unregisterCourse(courseId) {
    if (confirm('Are you sure you want to unregister from this course?')) {
        fetch(`/api/courses/unregister/${courseId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert(data.message); // Show success message
                    loadAvailableCourses(); // Refresh available courses
                    loadRegisteredCourses(); // Refresh registered courses
                } else if (data.error) {
                    alert(data.error); // Show error message
                }
            })
            .catch(error => {
                console.error("Error unregistering from course:", error); // Debugging
                alert("An error occurred while unregistering from the course.");
            });
    }
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

// Assign a course to a faculty
/*
function assignCourse(event) {
    event.preventDefault(); // Prevent default form submission
    console.log("assignCourse function triggered"); // Debugging

    const facultyId = document.getElementById('facultySelect').value;
    const courseId = document.getElementById('courseId').value;
    const courseName = document.getElementById('courseName').value;
    const credits = document.getElementById('courseCredits').value;
    console.log("Form data:", { facultyId, courseId, courseName, credits }); // Debuggin

    if (!facultyId || !courseId || !courseName || !credits) {
        alert('Please fill all fields.');
        return;
    }
    console.log("Sending data:", { facultyId, courseId, courseName, credits }); // Debugging

    fetch('/api/courses/assign', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ faculty_id: facultyId, course_id: courseId, course_name: courseName, credits: credits }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            closeModal(); // Close the modal
            location.reload(); // Refresh the page
            loadAvailableCourses(); // Refresh available courses
        } else if (data.error) {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error assigning course:', error);
        alert('An error occurred while assigning the course.');
    });
}
*/

function validateForm() {
    const courseId = document.getElementById('courseId').value;
    const courseName = document.getElementById('courseName').value;
    const semester = document.getElementById('semester').value;
    const credits = document.getElementById('courseCredits').value;
    
    if (!courseId || !courseName || !credits) {
        alert('Please fill all fields');
        return false;
    }
    if (semester < 1 || semester > 8) {
        alert('Semester must be between 1 and 8');
        return false;
    }
    return true;
}

function assignCourse(event) {
    event.preventDefault();
    if (!validateForm()) return false;

    const formData = {
        faculty_id: document.getElementById('facultyId').value,
        course_id: document.getElementById('courseId').value,
        course_name: document.getElementById('courseName').value,
        semester: document.getElementById('semester').value,
        credits: document.getElementById('courseCredits').value
    };

    fetch('/assign-course', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Course assigned successfully!');
            closeModal();
            location.reload();
        } else {
            alert('Error: ' + data.message);
        }
    });
    return false;
}

// Reset leaves for all faculty
function resetLeaves(facultyId) {
    if (confirm('Are you sure you want to reset leaves for this faculty?')) {
        fetch(`/api/faculty/${facultyId}/reset-leaves`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
            } else if (data.error) {
                alert(data.error);
            }
        })
        .catch(error => {
            console.error('Error resetting leaves:', error);
            alert('An error occurred while resetting leaves.');
        });
    }
}

// Approve a leave request
function approveLeave(leaveId) {
    fetch(`/api/leave/${leaveId}/approve`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
        } else if (data.error) {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error approving leave:', error);
        alert('An error occurred while approving the leave.');
    });
}

function rejectLeave(leaveId) {
    fetch(`/api/leave/${leaveId}/reject`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
        } else if (data.error) {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error rejecting leave:', error);
        alert('An error occurred while rejecting the leave.');
    });
}

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
// Show Assign Course Modal
function showAssignCourseModal(facultyId) {
    const modal = document.getElementById('assignCourseModal');
    const facultyIdInput = document.getElementById('facultyId');
    facultyIdInput.value = facultyId; // Set the faculty_id in the hidden input
    modal.style.display = 'block'; // Display the modal
}

// Close Modal
function closeModal() {
    const modal = document.getElementById('assignCourseModal');
    modal.style.display = 'none'; // Hide the modal
}

// Close Modal When Clicking Outside
window.onclick = function (event) {
    const modal = document.getElementById('assignCourseModal');
    if (event.target == modal) {
        modal.style.display = 'none'; // Hide the modal
    }
};
// Close modal when clicking outside of it
window.onclick = function (event) {
    const modals = document.getElementsByClassName('modal');
    Array.from(modals).forEach(modal => {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });
};

// Close modal when the close button is clicked
document.querySelectorAll('.close').forEach(button => {
    button.onclick = function () {
        const modal = button.closest('.modal');
        modal.style.display = 'none';
    };
});



function showLeaveForm() {
    document.getElementById('leaveModal').style.display = 'block';
}

function hideLeaveForm() {
    document.getElementById('leaveModal').style.display = 'none';
}

function submitLeave(event) {
    event.preventDefault();
    const leaveDate = document.getElementById('leaveDate').value;

    fetch('/api/leave/apply', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ leave_date: leaveDate })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            hideLeaveForm();
            location.reload();
        } else {
            alert(data.error);
        }
    })
    .catch(error => {
        alert('Error submitting leave application');
    });
}

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