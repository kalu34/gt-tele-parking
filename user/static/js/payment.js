// Chapa Payment  
const chapabutton = document.getElementById('btn-deposit');
const deposit = document.getElementById('deposit-amount');

const accessToken = document.cookie
  .split("; ")
  .find((row) => row.startsWith("access_token="))
  ?.split("=")[1];

if (!accessToken) {
  console.error("No access token found in cookie. Redirecting to login.");
  window.location.href = "user-login";
}

chapabutton.addEventListener('click', function () {
  const depositAmount = deposit.value; // Get the value *inside* the click handler

  console.log(depositAmount);

  if (depositAmount === "" || isNaN(depositAmount) || parseFloat(depositAmount) <= 0) {
      alert("Please enter a valid deposit amount.");
      return; // Stop execution if amount is invalid
  }

  fetch(`${window.API_URL}/chapa_deposit`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      amount: depositAmount,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        return response.text().then(err => {throw new Error(err || 'Invalid Response')});
      }
      return response.json();
    })
    .then((data) => {
      console.log("Chapa Response:", data); // Log the full response for debugging

      if (data && data.response && data.response.status === "success" && data.response.data && data.response.data.checkout_url) {
        window.location.href = data.response.data.checkout_url;
      } else {
        console.error("Invalid Chapa response:", data); // Log the error
        alert("An error occurred during payment initiation. Please try again."); // User-friendly message
      }
    })
    .catch((error) => {
      console.error("Fetch Error:", error); // Log fetch errors
      alert("A network error occurred. Please check your connection and try again."); // User-friendly message
    });
});

