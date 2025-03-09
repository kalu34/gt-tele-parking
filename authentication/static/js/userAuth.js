document.addEventListener("DOMContentLoaded", function () {
  // Wait for the DOM to load
  const loginForm = document.getElementById("token-login-form");
  const loginButton = document.getElementById("token-login-button");
  const loginError = document.getElementById("token-login-error");


  loginForm.addEventListener("submit", function (event) {
    // Listen for form submission
    event.preventDefault(); // Prevent default form submission
    const phone = document.getElementById("token-phone-number").value;
    const password = document.getElementById("token-password").value;
    loginError.textContent = "";

    
    fetch(`${window.API_URL}/user-login-api`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ phone: phone, password: password }),
    })
      .then((response) => response.json()) // Parse JSON properly
      .then((data) => {
        loginError.textContent = data.detail
        if (data.role === 1) {
          window.location.href = "user_home";
        } else if (data.role === 2) {
          window.location.href="parking_home"
        } else if (data.role === 3) {
          window.location.href="woreda_dashboard"
        } else if (data.role === 4) {
          window.location.href="subcity_dashboard"
        } else if (data.role === 5) {
          window.location.href="City_Dashboard"
        }
        console.log(data.role)
      })
      .catch((error) => {
        console.error("Login Error:", error);
      });
    
  });

});

