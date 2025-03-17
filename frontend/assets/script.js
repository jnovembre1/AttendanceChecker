document.addEventListener("DOMContentLoaded", function() {
    fetch("http://127.0.0.1:8000/")  // points to backend API setup in pyenv
      .then(response => response.json())
      .then(data => {
          document.getElementById("message").innerText = data.message;
      })
      .catch(error => {
          console.error("Error fetching message:", error);
          document.getElementById("message").innerText = "Failed to load message.";
      });
});
