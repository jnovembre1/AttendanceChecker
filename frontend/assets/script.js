const loginForm = document.getElementById("loginForm");
const errorMessageEl = document.getElementById("result");

if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
      const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
      });

      const result = await response.json();
      if (!response.ok) {
        errorMessageEl.innerText = "Error: " + result.detail;
      } else {
        // store the instructor data in session storage.
        sessionStorage.setItem("username", username);
        sessionStorage.setItem("authToken", "dummy_token"); 
        sessionStorage.setItem("instructorName", username);

        errorMessageEl.innerText = result.message;
        setTimeout(() => {
          window.location.href = "/assets/dashboard.html";
        }, 1000);
      }
    } catch (error) {
      console.error("Error fetching login:", error);
      errorMessageEl.innerText = "Request failed: " + error;
    }
  });
}