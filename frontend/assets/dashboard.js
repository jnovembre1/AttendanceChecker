document.addEventListener('DOMContentLoaded', function() {
    // Retrieve authentication details from session storage.
    const token = sessionStorage.getItem('authToken');
    const username = sessionStorage.getItem('username');

    console.log("authToken:", token);
    console.log("username:", username);

    if (!token || !username) {
        // If no credentials are found, redirect to the login page.
        window.location.href = "/index.html";
        return;
    }

    // Update UI with the logged-in instructor's name.
    const usernameDisplay = document.getElementById('username-display');
    const welcomeMessage = document.getElementById('welcome-message');
    const instructorName = sessionStorage.getItem('instructorName') || username;
    if (usernameDisplay) usernameDisplay.textContent = instructorName;
    if (welcomeMessage) welcomeMessage.textContent = `Welcome, ${instructorName}!`;

    // Set up mobile menu functionality.
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Set up the course selection dropdown.
    setupCourseDropdown();

    // Initialize the attendance chart.
    initializeAttendanceChart();

    // Fetch attendance data from the backend.
    fetchAttendanceData();

    // Set up auto-refresh every 2 minutes.
    setInterval(fetchAttendanceData, 120000);

    // Update the "last updated" timestamp on load.
    updateTimestamp();
});

// Sets up the course selection dropdown.
function setupCourseDropdown() {
    const courseSelect = document.getElementById('course-select');
    if (!courseSelect) return;

    // Listen for changes on the dropdown.
    courseSelect.addEventListener('change', function() {
        fetchAttendanceData(this.value);
    });

    //static example courses for when that is built
    const sampleCourses = [
        { id: 1, name: 'Web Development' },
        { id: 2, name: 'Database Systems' },
        { id: 3, name: 'Software Engineering' }
    ];

    sampleCourses.forEach(course => {
        const option = document.createElement('option');
        option.value = course.id;
        option.textContent = course.name;
        courseSelect.appendChild(option);
    });
}

// Initializes the Chart.js attendance chart whenever its built.
function initializeAttendanceChart() {
    const ctx = document.getElementById('attendance-chart');
    if (!ctx) return;

    window.attendanceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Attendance Rate (%)',
                data: [],
                backgroundColor: 'rgba(59, 130, 246, 0.2)',
                borderColor: 'rgba(59, 130, 246, 1)',
                borderWidth: 2,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: false,
                    min: 0,
                    max: 100,
                    title: { display: true, text: 'Attendance Percentage' }
                },
                x: {
                    title: { display: true, text: 'Date' }
                }
            }
        }
    });
}

// Updates the attendance chart with data from the backend.
function updateAttendanceChart(data) {
    if (!window.attendanceChart) return;

    
    const labels = [];
    const attendanceData = [];

    if (data.dailyAttendance && Array.isArray(data.dailyAttendance)) {
        data.dailyAttendance.forEach(item => {
            labels.push(item.date);
            attendanceData.push(item.rate);
        });
    } else {
        // Use last 7 days as fallback labels.
        for (let i = 6; i >= 0; i--) {
            const date = new Date();
            date.setDate(date.getDate() - i);
            labels.push(date.toLocaleDateString('en-US', {
                weekday: 'short', month: 'short', day: 'numeric'
            }));
            attendanceData.push(70 + Math.floor(Math.random() * 10));
        }
    }

    window.attendanceChart.data.labels = labels;
    window.attendanceChart.data.datasets[0].data = attendanceData;
    window.attendanceChart.update();
}

// Fetches attendance data from the real API endpoint.
function fetchAttendanceData(courseId = 'all') {
    updateTimestamp();

    const token = sessionStorage.getItem('authToken');
    const username = sessionStorage.getItem('username');

    // Build the API URL using the instructor's username.
    let apiUrl = `http://localhost:8000/api/attendance/instructor/${username}`;
    if (courseId !== 'all') {
        apiUrl += `/course/${courseId}`;
    }

    fetch(apiUrl, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch attendance data');
        }
        return response.json();
    })
    .then(data => {
        // keys from the backend: 
        // totalStudents, presentToday, absentToday, attendanceRate, recentActivity, dailyAttendance (optional)
        updateDashboardStats(data);
        updateActivityTable(data.recentActivity);
        updateAttendanceChart(data);
    })
    .catch(error => {
        console.error('Error fetching attendance data:', error);
        const tableBody = document.getElementById('activity-table-body');
        if (tableBody) {
            tableBody.innerHTML = `<tr>
                <td colspan="4" class="px-6 py-4 text-center text-sm text-red-600">
                    Error loading attendance data.
                </td>
            </tr>`;
        }
    });
}

// Updates the dashboard stat cards.
function updateDashboardStats(data) {
    document.getElementById('total-students').textContent = data.totalStudents;
    document.getElementById('present-count').textContent = data.presentToday;
    document.getElementById('absent-count').textContent = data.absentToday;
    document.getElementById('attendance-rate').textContent = `${data.attendanceRate}%`;
}

// Updates the recent activity table with the latest attendance records.
function updateActivityTable(activities) {
    const tableBody = document.getElementById('activity-table-body');
    if (!tableBody) return;
    
    tableBody.innerHTML = ''; // Clear existing rows.

    if (activities && activities.length > 0) {
        activities.forEach(activity => {
            const row = document.createElement('tr');
            const dateTime = activity.dateTime ? new Date(activity.dateTime) : null;
            const formattedDateTime = dateTime
                ? dateTime.toLocaleDateString() + ' ' + dateTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                : '--';

            row.innerHTML = `
                <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm font-medium text-gray-900">${activity.studentName}</div>
                    <div class="text-sm text-gray-500">ID: ${activity.studentId}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${activity.courseName}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        activity.status === 'present' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    }">${activity.status === 'present' ? 'Present' : 'Absent'}</span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${formattedDateTime}</td>
            `;
            tableBody.appendChild(row);
        });
    } else {
        tableBody.innerHTML = `<tr>
            <td colspan="4" class="px-6 py-4 text-center text-sm text-gray-500">
                No attendance records found.
            </td>
        </tr>`;
    }
}

// Updates the "last updated" timestamp.
function updateTimestamp() {
    const updateTimeElement = document.getElementById('update-time');
    if (updateTimeElement) {
        const now = new Date();
        updateTimeElement.textContent = now.toLocaleTimeString();
    }
}
