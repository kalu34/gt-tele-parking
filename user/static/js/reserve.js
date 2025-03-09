const reserve_box = document.querySelector(".reserve-box");
const close_btn = document.querySelector(".button_close");
const background = document.querySelector(".background");
const reseve_btn = document.querySelector("#reseve-now");
const reserveBtnContainer = document.querySelector(".reserve-btn-container");
const errorMessage = document.getElementById("errorMessage");
const successMessage = document.getElementById("successMessage");

const accessToken = document.cookie
  .split("; ")
  .find((row) => row.startsWith("access_token="))
  ?.split("=")[1];

if (!accessToken) {
  console.error("No access token found in cookie. Redirecting to login.");
  window.location.href = "user-login";
}

let toggle = false;

function reserve_function(parking_id) {
  background.classList.add("bg-color");
  if (toggle) {
    reserve_box.classList.add("d-none");
    reserve_box.classList.remove("d-block");
    toggle = false;
  }
  reserve_box.classList.remove("d-none");
  reserve_box.classList.add("d-block");
  toggle = true;

  fetch(`${window.API_URL}/api/parking/${parking_id}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("Error Fetching Parking");
      }
    })
    .then((data) => {
      console.log(data);
      updateReserveBox(data.data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function updateReserveBox(parkingData) {
  document.querySelector(".parking_title").textContent = parkingData.name;
  document.querySelector(".parking_location").textContent = parkingData.address;

  document.querySelector(".parking_image_box .box:nth-child(1) img").src =
    parkingData.image1;
  document.querySelector(".parking_image_box .box:nth-child(2) img").src =
    parkingData.image2;

  const parkingInfoList1 = document.getElementById("parking-info-list-1");
  const parkingInfoList2 = document.getElementById("parking-info-list-2");

  parkingInfoList1.innerHTML = "";
  parkingInfoList2.innerHTML = "";

  const priceLi = document.createElement("li");
  priceLi.id = "parking-price";
  priceLi.textContent = `Price: ${parkingData.price_per_hour} Birr/hr`;
  parkingInfoList1.appendChild(priceLi);

  const availableSlotsLi = document.createElement("li");
  availableSlotsLi.id = "parking-available-slots";
  availableSlotsLi.textContent = `Available Slots: ${parkingData.available_slots}`;
  parkingInfoList1.appendChild(availableSlotsLi);

  const slotCapacityLi = document.createElement("li");
  slotCapacityLi.id = "parking-slot-capacity";
  slotCapacityLi.textContent = `Slot Capacity: ${parkingData.slot_capacity}`;
  parkingInfoList1.appendChild(slotCapacityLi);

  const paymentMethodsLi = document.createElement("li");
  paymentMethodsLi.id = "parking-payment-methods";
  paymentMethodsLi.textContent = `Payment Methods: ${parkingData.payment_method.join(
    ", "
  )}`;
  parkingInfoList1.appendChild(paymentMethodsLi);

  parkingData.amenities.forEach((amenity) => {
    const li = document.createElement("li");
    li.textContent = amenity;
    parkingInfoList2.appendChild(li);
  });

  const hasDisabledParkingLi = document.createElement("li");
  hasDisabledParkingLi.id = "parking-disabled";
  hasDisabledParkingLi.textContent = `Disabled Parking: ${
    parkingData.has_disabled_parking ? "Yes" : "No"
  }`;
  parkingInfoList2.appendChild(hasDisabledParkingLi);

  const hasEvChargingLi = document.createElement("li");
  hasEvChargingLi.id = "parking-ev-charging";
  hasEvChargingLi.textContent = `EV Charging: ${
    parkingData.has_ev_charging ? "Yes" : "No"
  }`;
  parkingInfoList2.appendChild(hasEvChargingLi);

  const hasSecurityCamerasLi = document.createElement("li");
  hasSecurityCamerasLi.id = "parking-security-cameras";
  hasSecurityCamerasLi.textContent = `Security Cameras: ${
    parkingData.has_security_cameras ? "Yes" : "No"
  }`;
  parkingInfoList2.appendChild(hasSecurityCamerasLi);

  const hasSecurityGuardLi = document.createElement("li");
  hasSecurityGuardLi.id = "parking-security-guard";
  hasSecurityGuardLi.textContent = `Security Guard: ${
    parkingData.has_security_guard ? "Yes" : "No"
  }`;
  parkingInfoList2.appendChild(hasSecurityGuardLi);

  const reserveBtn = document.createElement("a");
  reserveBtn.className = "reseve_now w-100";
  reserveBtn.textContent = "Reserve Now";
  reserveBtn.onclick = function () {
    reserveParking(parkingData.id);
  };
  reserveBtnContainer.replaceWith(reserveBtn);
}

close_btn.addEventListener("click", function () {
  errorMessage.innerHTML = "";
  background.classList.remove("bg-color");
  reserve_box.classList.add("d-none");
  reserve_box.classList.remove("d-block");
  toggle = false;
});

function reserveParking(parkingData) {
  const start_time = document.getElementById("startTime").value;
  const end_time = document.getElementById("endTime").value;
  const slot = document.getElementById("selectOption").value;

  errorMessage.innerHTML = "";

  fetch(`${window.API_URL}/api/reserve-parking-appointment/${parkingData}/`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      start_time: start_time,
      end_time: end_time,
      slot: slot,
    }),
  })
    .then((response) => {
      if (response.status === 201) {
        return response.json();
      } else {
        return response.json().then((errorData) => {
          throw new Error(JSON.stringify(errorData));
        });
      }
    })
    .then((data) => {
      location.reload();
    })
    .catch((error) => {
      try {
        const errorData = JSON.parse(error.message);
        console.error("Error:", errorData);

        let errorMessages = "";
        if (errorData.slot) {
          errorMessages += `<p>Slot: ${extractFirstPart(
            errorData.slot[0]
          )}</p>`;
        }
        if (errorData.start_time) {
          errorMessages += `<p>Start Time: ${extractFirstPart(
            errorData.start_time[0]
          )}</p>`;
        }
        if (errorData.end_time) {
          errorMessages += `<p>End Time: ${extractFirstPart(
            errorData.end_time[0]
          )}</p>`;
        }

        errorMessage.innerHTML = errorMessages;
      } catch (parseError) {
        console.error("Error parsing error message:", error);
        errorMessage.innerHTML = "An unexpected error occurred.";
      }
    });
}

function extractFirstPart(errorMessage) {
  if (errorMessage === undefined || errorMessage === null) {
    return "";
  }
  const dotIndex = errorMessage.indexOf(".");
  if (dotIndex !== -1) {
    return errorMessage.substring(0, dotIndex + 1);
  } else {
    return errorMessage;
  }
}

function removeReserve(parking_id) {
  if (confirm("Are you sure you want to remove this Reservasion?")) {
    fetch(`${window.API_URL}/api/remove-parking-reservasion/${parking_id}/`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${accessToken}`,
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        location.reload();
      })
      .catch((error) => {
        console.log(error);
      });
  }
}

function cancelReserve(reserve_id) {
  if (confirm("Are you sure you want to cancel this Reservasion? only 1/3 will be refunded")) {
    fetch(`${window.API_URL}/api/cancel-reserved-parking/${reserve_id}/`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${accessToken}`,
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        window.location.href = "/user_wallet"
      })
      .catch((error) => {
        console.log(error);
      });
  }
}
