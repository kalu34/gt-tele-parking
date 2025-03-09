const registerForm = document.querySelector('#userRegisterForm')
const errorMessage = document.getElementById('error-message');

const slidePage = document.querySelector(".slide-page");
const nextBtns = document.querySelectorAll(".next");
const prevBtns = document.querySelectorAll(".prev");
const submitBtn = document.querySelector(".submit");
const progressText = document.querySelectorAll(".step p");
const progressCheck = document.querySelectorAll(".step .check");
const bullet = document.querySelectorAll(".step .bullet");
const pages = document.querySelectorAll(".page");
let current = 1;

// Function to validate fields
function validateStep(pageIndex) {
  let valid = true;
  const inputs = pages[pageIndex].querySelectorAll("input[required]");

  inputs.forEach((input) => {
    const errorMessage = input.nextElementSibling;

    // Remove old error messages if they exist
    if (errorMessage && errorMessage.classList.contains("error-message")) {
      errorMessage.remove();
    }

    if (input.value.trim() === "") {
      showError(input, "This field is required");
      valid = false;
    } else {
      input.classList.remove("error");

      // First Name & Last Name validation (only alphabet letters)
      if ((input.name === "firstName" || input.name === "lastName") && !/^[A-Za-z]+$/.test(input.value)) {
        showError(input, "Only alphabet letters are allowed");
        valid = false;
      }

      // Phone number validation (exactly 10 digits)
      if (input.name === "phone" && !/^\d{10}$/.test(input.value)) {
        showError(input, "Phone number must be exactly 10 digits");
        valid = false;
      }

      // Email validation
      if (input.name === "email" && !/^\S+@\S+\.\S+$/.test(input.value)) {
        showError(input, "Enter a valid email address");
        valid = false;
      }

      // Password validation (8+ characters, at least one letter, number, and symbol)
      // if (input.name === "password" && !/^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/.test(input.value)) {
      //   showError(input, "8+ chars, letters, numbers & symbols.");
      //   valid = false;
      // }

      // Confirm Password validation (must match Password)
      if (input.name === "confirmPassword") {
        const password = pages[pageIndex].querySelector('input[name="password"]').value;
        if (input.value !== password) {
          showError(input, "Passwords do not match");
          valid = false;
        }
      }

      // Plate Number validation (5-7 characters, must include at least 1 letter and 5 digits)
      if (input.name === "plateNumber" && !/^[A-Za-z]\d{5,6}$/.test(input.value)) {
        showError(input, "Plate number must start with a letter, have at least 5 digits");
        valid = false;
      }
    }
  });

  return valid;
}

// Function to display error message
function showError(input, message) {
  input.classList.add("error");
  const errorMsg = document.createElement("p");
  errorMsg.classList.add("error-message");
  errorMsg.innerText = message;
  input.parentElement.appendChild(errorMsg);
}

// Next button event listeners
nextBtns.forEach((btn, index) => {
  btn.addEventListener("click", function (event) {
    event.preventDefault();
    if (validateStep(index)) {
      slidePage.style.marginLeft = `-${(index + 1) * 25}%`;
      bullet[current - 1].classList.add("active");
      progressCheck[current - 1].classList.add("active");
      progressText[current - 1].classList.add("active");
      current += 1;
    }
  });
});

// Previous button event listeners
prevBtns.forEach((btn, index) => {
  btn.addEventListener("click", function (event) {
    event.preventDefault();
    slidePage.style.marginLeft = `-${index * 25}%`;
    bullet[current - 2].classList.remove("active");
    progressCheck[current - 2].classList.remove("active");
    progressText[current - 2].classList.remove("active");
    current -= 1;
  });
});

// Submit button validation
submitBtn.addEventListener("click", function (event) {
  if (validateStep(3)) {
    bullet[current - 1].classList.add("active");
    progressCheck[current - 1].classList.add("active");
    progressText[current - 1].classList.add("active");
    current += 1;
  } else {
    event.preventDefault();
  }
});



registerForm.addEventListener('submit', function(event) {
    event.preventDefault();
    phone_number = document.getElementById('phone').value
    firstName = document.getElementById('firstName').value
    lastName = document.getElementById('lastName').value
    password = document.getElementById('password').value
    email = document.getElementById('email').value
    plateNumber = document.getElementById('plateNumber').value

    console.log('user registerd')

    console.log(phone_number, firstName, lastName, password, email, phone_number)
    fetch(`${window.API_URL}/user-regiseter-api`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            phone_number: phone_number,
            first_name: firstName,
            last_name: lastName,
            password: password,
            email: email,
            plate_number: plateNumber
        })
    })
    .then(response => {
        if (!response.ok) { 
            return response.json().then(err => {throw new Error(JSON.stringify(err))}); // Parse error JSON and throw error
        }
        return response.json();
    })
    .then(data => {
        errorMessage.textContent = ""; 
        window.location.href = "/user-login"
    })
    .catch(error => {
        console.error("Registration Error:", error);
        try {
            const errorData = JSON.parse(error.message); // Parse the error JSON
            let errorMessages = [];

            if (typeof errorData === 'object' && errorData !== null) { // Check if it's an object
                for (const key in errorData) {
                    if (Array.isArray(errorData[key])) { // Check if the value is an array (multiple errors for one field)
                        errorMessages = errorMessages.concat(errorData[key]);
                    } else if (typeof errorData[key] === 'string'){
                        errorMessages.push(errorData[key]); // If it's a string, just add it
                    }
                }
            } else if (typeof errorData === 'string'){
                errorMessages.push(errorData);
            }
            
            errorMessage.textContent = errorMessages.join('\n'); // Display error messages, separated by newlines
        } catch (parseError) {
            console.error("Error parsing error response:", parseError);
            errorMessage.textContent = "An error occurred during registration. Please try again."; // Generic error message
        }
    });
});