<<<<<<< HEAD
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
=======
document.addEventListener("DOMContentLoaded", function() {
    const messageEl = document.getElementById("message");
    if (messageEl) {
      fetch("http://127.0.0.1:8000/")
        .then(response => response.json())
        .then(data => {
          messageEl.innerText = data.message;
        })
        .catch(error => {
          console.error("Error fetching message:", error);
          messageEl.innerText = "Failed to load message.";
        });
    }
  
    const loginForm = document.getElementById("loginForm");
    if (!loginForm) {
      console.error("No element with id 'loginForm' found.");
      return;
    }
  
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault(); 
  
      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;
      
      try {
        const response = await fetch("http://localhost:8000/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ username, password })
        });
        
        const result = await response.json();
        if (!response.ok) {
          document.getElementById("result").innerText = "Error: " + result.detail;
        } else {
          document.getElementById("result").innerText = result.message;
          setTimeout(() => {
            window.location.href = "assets/dashboard.html";
          }, 1000);
        }
      } catch (error) {
        console.error("Error fetching login:", error);
        document.getElementById("result").innerText = "Request failed: " + error;
      }
    });
  });
  
>>>>>>> a94253b51376ed0b8d02ec16fe8e36faa12f1512
