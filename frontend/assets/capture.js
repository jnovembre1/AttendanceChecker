(async function() {
    // DOM element references.
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const studentIdInput = document.getElementById('studentId');
    const courseIdInput = document.getElementById('courseId');
    const resultElement = document.getElementById('result');
    const btnRegister = document.getElementById('capture-register');
    const btnVerify = document.getElementById('capture-verify');
    const btnVerifyAttendance = document.getElementById('verify-attendance');
    const manualFileInput = document.getElementById('manualFile');
    const btnManualUpload = document.getElementById('upload-manual');

    // Start the webcam stream.
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
    } catch (error) {
        resultElement.textContent = 'Error accessing webcam: ' + error;
        return;
    }

    // Capture the current frame from the video and return it as a Blob.
    function captureImage() {
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        return new Promise((resolve) => {
            canvas.toBlob((blob) => {
                if (!blob) {
                    console.error('No blob produced.');
                    resolve(null);
                    return;
                }
                console.log('Captured image blob size:', blob.size);
                resolve(blob);
            }, 'image/jpeg');
        });
    }

    // Helper: set a user-facing message.
    function setResultMessage(message) {
        console.log('Result:', message);
        resultElement.textContent = message;
    }

    // Helper: send a captured image to a given endpoint.
    async function sendImage(endpoint, blob) {
        const formData = new FormData();
        formData.append('file', blob, 'capture.jpg');
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData
            });
            const text = await response.text();
            console.log('Raw response:', text);
            return JSON.parse(text);
        } catch (error) {
            setResultMessage('Error sending image: ' + error);
            return null;
        }
    }

    // Register face via webcam capture.
    btnRegister.addEventListener('click', async () => {
        const studentId = studentIdInput.value.trim();
        if (!studentId) {
            setResultMessage('Please enter a student ID.');
            return;
        }
        const endpoint = `http://localhost:8000/api/students/${studentId}/upload-photo`;
        setResultMessage('Uploading photo...');
        const blob = await captureImage();
        if (!blob) return;
        const data = await sendImage(endpoint, blob);
        if (!data) return;
        if (data.message) {
            setResultMessage(data.message);
        } else if (data.detail) {
            setResultMessage('Error: ' + data.detail);
        } else {
            setResultMessage('Unknown response from server.');
        }
    });

    // Verify face via webcam capture.
    /* btnVerify.addEventListener('click', async () => {
        const studentId = studentIdInput.value.trim();
        if (!studentId) {
            setResultMessage('Please enter a student ID.');
            return;
        }
        const endpoint = `http://localhost:8000/api/students/${studentId}/verify-face`;
        setResultMessage('Verifying face...');
        const blob = await captureImage();
        if (!blob) return;
        const data = await sendImage(endpoint, blob);
        if (!data) return;
        if (data.detail) {
            setResultMessage('Error: ' + data.detail);
            return;
        }
        if (typeof data.verified === 'boolean') {
            if (data.verified) {
                const distanceStr = (typeof data.distance === 'number') ? data.distance.toFixed(3) : 'unknown';
                setResultMessage(`Verified! (Distance: ${distanceStr})`);
            } else {
                if (typeof data.distance === 'number') {
                    setResultMessage(`Not verified. (Distance: ${data.distance.toFixed(3)})`);
                } else {
                    setResultMessage('Not verified (no distance provided).');
                }
            }
        } else if (data.message) {
            setResultMessage('Verification failed: ' + data.message);
        } else {
            setResultMessage('No "verified" property in response. Full response: ' + JSON.stringify(data));
        }
    }); */

    // Verify face and mark attendance via webcam capture.
    btnVerifyAttendance.addEventListener('click', async () => {
        const studentId = studentIdInput.value.trim();
        const courseId = courseIdInput.value.trim();
        if (!studentId) {
            setResultMessage('Please enter a student ID.');
            return;
        }
        if (!courseId) {
            setResultMessage('Please enter a course ID.');
            return;
        }
        const endpoint = `http://localhost:8000/api/students/${studentId}/verify-and-attend/${courseId}`;
        setResultMessage('Verifying face and recording attendance...');
        const blob = await captureImage();
        if (!blob) return;
        const data = await sendImage(endpoint, blob);
        if (!data) return;
        if (data.detail) {
            setResultMessage('Error: ' + data.detail);
            return;
        }
        if (typeof data.verified === 'boolean') {
            if (data.verified) {
                const distanceStr = (typeof data.distance === 'number') ? data.distance.toFixed(3) : 'unknown';
                setResultMessage(`Verified! Attendance recorded. (Distance: ${distanceStr})`);
            } else {
                if (typeof data.distance === 'number') {
                    setResultMessage(`Not verified. (Distance: ${data.distance.toFixed(3)})`);
                } else {
                    setResultMessage('Not verified (no distance provided).');
                }
            }
        } else if (data.message) {
            setResultMessage('Verification failed: ' + data.message);
        } else {
            setResultMessage('No "verified" property in response. Full response: ' + JSON.stringify(data));
        }
    });

    // Manual file upload.
    btnManualUpload.addEventListener('click', async () => {
        const studentId = studentIdInput.value.trim();
        if (!studentId) {
            setResultMessage('Please enter a student ID.');
            return;
        }
        const file = manualFileInput.files[0];
        if (!file) {
            setResultMessage('Please select a file to upload.');
            return;
        }
        const endpoint = `http://localhost:8000/api/students/${studentId}/upload-photo`;
        setResultMessage('Uploading manual photo...');
        const formData = new FormData();
        formData.append('file', file, file.name);
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData
            });
            const text = await response.text();
            console.log('Raw manual upload response:', text);
            const data = JSON.parse(text);
            if (data.message) {
                setResultMessage(data.message);
            } else if (data.detail) {
                setResultMessage('Error: ' + data.detail);
            } else {
                setResultMessage('Unknown response from server.');
            }
        } catch (error) {
            setResultMessage('Error sending manual image: ' + error);
        }
    });
})();
