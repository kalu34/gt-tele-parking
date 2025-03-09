const logoutButton = document.getElementById('logout-button');

const accessToken = document.cookie
  .split("; ")
  .find((row) => row.startsWith("access_token="))
  ?.split("=")[1];

if (!accessToken) {
  console.error("No access token found in cookie. Redirecting to login.");
  window.location.href = "user-login";
}

logoutButton.addEventListener('click', function (event) {
  event.preventDefault();

  fetch(`${window.API_URL}/user-logout`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json", 
      'X-CSRFToken': csrfToken,
    },
  })
  .then((response) => {
    if (response.status === 204) {
      document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; SameSite=Strict; HttpOnly"; // Clear the cookie
      window.location.href = "/user-login"; // Redirect after logout
    } else {
      console.error("Logout failed");
    }
  })
  .catch((error) => {
    console.error("Logout Error:", error);
  });
});