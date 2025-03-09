// Selecting A spot
const cols = document.querySelectorAll(".spot");
let selectedCol = null;
let selectedColString = null

cols.forEach((col) => {
  col.addEventListener("click", function (e) {
    if (selectedCol) {
      selectedCol.classList.remove("selected");
    }
    this.classList.add("selected");
    selectedCol = this;
    selectedColString = selectedCol.textContent; // Extract the text content of the selected element
  });
});

document.querySelector(".start_time_button").addEventListener("click", () => {
  const url = window.location.href;
  const parts = url.split("/");
  const id = parts[parts.length - 2]; // Get the second-to-last part of the URL

  fetch(`http://127.0.0.1:8000/parking_new_approve_request/${id}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      'X-CSRFToken': csrfToken // Ensure csrfToken is defined
    },
    body: JSON.stringify({ key: selectedColString }), // Add your data here
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      console.log(data);
      // Handle the data from the backend here
    })
    .catch((error) => {
      console.error("There was a problem with your fetch operation:", error);
    });
});
