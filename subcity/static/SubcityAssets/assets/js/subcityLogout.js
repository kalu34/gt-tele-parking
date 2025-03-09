const accessToken = document.cookie
.split("; ")
.find((row) => row.startsWith("access_token="))
?.split("=")[1];

if (!accessToken) {
console.error("No access token found in cookie. Redirecting to login.");
window.location.href = "admin"; // Redirect after logout
}

const logoutButtons = document.querySelectorAll('#logout-button');
logoutButtons.forEach((item) => {
  item.addEventListener('click', function (event) {
    event.preventDefault();
    console.log('button clicked')
    fetch(`${window.API_URL}/user-logout`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${accessToken}`,
        "Content-Type": "application/json", // Important for most API requests
      },
    })
    .then((response) => {
      if (response.status === 204) {
        document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; SameSite=Strict; HttpOnly"; // Clear the cookie
        window.location.href = "/admin"; // Redirect after logout
      } else {
        console.error("Logout failed");
      }
    })
    .catch((error) => {
      console.error("Logout Error:", error);
    });
  });
})
