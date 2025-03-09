// your_script.js
var map = L.map("map").setView([51.505, -0.09], 17);

L.tileLayer(
  "https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
  {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: "abcd",
    maxZoom: 20,
  }
).addTo(map);
var svgIcon = `
<svg id="parking-area-icon" xmlns="http://www.w3.org/2000/svg" width="43.334" height="37.051" viewBox="0 0 73.334 62.051">
  <path id="Path_8" data-name="Path 8" d="M9.639,0H48.654a9.663,9.663,0,0,1,9.639,9.639V30.913H44.944a6.165,6.165,0,0,0-4.854,2.263,10.186,10.186,0,0,0-1.9,3.6l-.252.783a6.066,6.066,0,0,0-2.561.842,4.308,4.308,0,0,0-1.959,2.713,4.389,4.389,0,0,0,.458,3.163l.072.129c-1.746,2.889-1.468,6.372-1.167,10.145l.024.3,0,.156v1.723H9.639A9.663,9.663,0,0,1,0,47.085V9.639A9.663,9.663,0,0,1,9.639,0Z" fill="#6046c1"/>
  <path id="Path_9" data-name="Path 9" d="M73.308,32.415H37.488a5.1,5.1,0,0,0-5.073,5.073V71.74a5.1,5.1,0,0,0,5.073,5.073H58.809c0,.58.027,1.173.062,1.775H37.488A6.871,6.871,0,0,1,30.64,71.74V37.488a6.871,6.871,0,0,1,6.848-6.848h35.82a6.871,6.871,0,0,1,6.848,6.848V57.165H78.38V37.488a5.093,5.093,0,0,0-5.072-5.073Z" transform="translate(-26.251 -26.251)" fill="#fff"/>
  <path id="Path_10" data-name="Path 10" d="M138.779,125.358v-5.364h6.289a4.239,4.239,0,0,0,1.954-.392,2.5,2.5,0,0,0,1.094-1.071,3.35,3.35,0,0,0,.357-1.565,4.515,4.515,0,0,0-.357-1.79,2.962,2.962,0,0,0-1.094-1.336,3.411,3.411,0,0,0-1.954-.508h-3.81v20.429H134.6v-25.8h10.469a11.692,11.692,0,0,1,5.413,1.173,8.559,8.559,0,0,1,3.508,3.187,8.677,8.677,0,0,1,1.233,4.609,7.907,7.907,0,0,1-1.233,4.409,8.154,8.154,0,0,1-3.508,2.956,12.6,12.6,0,0,1-5.413,1.064Zm16.632.315a6.165,6.165,0,0,1,4.854-2.263h17.162a6.312,6.312,0,0,1,4.6,1.916,8.933,8.933,0,0,1,2.226,4.175l.152.612a5.785,5.785,0,0,1,2.209.821,4.286,4.286,0,0,1,1.922,2.809,4.424,4.424,0,0,1-.539,3.147,5.352,5.352,0,0,1-.48.695c1.4,2.527,1.232,5.272.927,10.218-.043.7-.014,1.431-.014,2.138a4.636,4.636,0,0,1-4.609,4.608H179.3a4.562,4.562,0,0,1-2.862-1.01,3.531,3.531,0,0,1-.4-.341,4.677,4.677,0,0,1-.477-.559H160.981a4.534,4.534,0,0,1-.476.559l-.007-.007-.007.007a4.58,4.58,0,0,1-3.244,1.351H152.73a4.572,4.572,0,0,1-2.863-1.01,3.687,3.687,0,0,1-.4-.341,4.6,4.6,0,0,1-1.351-3.257V147.5l0-.156-.024-.3c-.3-3.773-.579-7.256,1.167-10.145l-.072-.129a4.389,4.389,0,0,1-.458-3.163A4.308,4.308,0,0,1,150.7,130.9a6.066,6.066,0,0,1,2.561-.842l.252-.783a10.186,10.186,0,0,1,1.9-3.6Z" transform="translate(-115.321 -92.497)" fill="#fff"/>
  <path id="Path_11" data-name="Path 11" d="M261.026,240.61c-1.865,0-2.814,1.613-3.386,3.392l-1.452,4.517-.7-1.321c-3.15-.186-3.509,1.59-.375,3.183-3.49,2.26-3.008,6.216-2.665,10.6a1.566,1.566,0,0,0-.011.165v2.442a1.063,1.063,0,0,0,1.06,1.058h4.517a1.063,1.063,0,0,0,1.06-1.058v-.851H279v.851a1.062,1.062,0,0,0,1.058,1.058h4.519a1.061,1.061,0,0,0,1.058-1.058v-1.879c.352-5.718.563-8.028-1.689-10.344l-.557-.852c3.425-1.626,3.137-3.506-.1-3.317l-.627,1.182L281.575,244c-.45-1.808-1.524-3.389-3.387-3.389Zm-1.381,3.029a1.977,1.977,0,0,1,.51-.649,2.078,2.078,0,0,1,1.487-.6H277.38c1.421,0,2.283,1.2,2.584,2.582l1.093,4.545H257.694v0l1.365-4.545A6.194,6.194,0,0,1,259.645,243.639Zm1.232,11.944-4.013-.5c-.947-.106-1.2.294-.879,1.11l.434,1.053a1.521,1.521,0,0,0,.543.606,1.842,1.842,0,0,0,.9.248l3.579.029c.864,0,1.239-.348.968-1.142a1.941,1.941,0,0,0-1.531-1.4Zm16.311,0,4.013-.5c.948-.106,1.2.294.879,1.11l-.434,1.053a1.51,1.51,0,0,1-.543.606,1.841,1.841,0,0,1-.9.248l-3.579.029c-.865,0-1.239-.348-.968-1.142a1.939,1.939,0,0,1,1.53-1.4Z" transform="translate(-216.082 -206.148)" fill="#1a1a1a" fill-rule="evenodd"/>
</svg>
    `;

var svgicon2 = `<svg version="1.0" xmlns="http://www.w3.org/2000/svg"
 width="30pt" height="30pt" viewBox="0 0 512.000000 512.000000"
 preserveAspectRatio="xMidYMid meet">

<g transform="translate(0.000000,512.000000) scale(0.100000,-0.100000)"
fill="#000000" stroke="none">
<path d="M2430 5114 c-314 -36 -534 -114 -767 -270 -355 -238 -592 -593 -685
-1024 -33 -154 -33 -421 0 -569 101 -452 429 -1198 925 -2106 245 -450 642
-1135 657 -1135 15 0 412 685 657 1135 496 908 824 1654 925 2106 33 148 33
415 0 569 -93 431 -330 786 -685 1024 -198 133 -388 209 -632 252 -80 14 -329
26 -395 18z m314 -375 c513 -68 942 -483 1042 -1008 20 -101 22 -323 5 -422
-88 -517 -474 -916 -991 -1026 -118 -25 -362 -25 -480 0 -519 111 -906 512
-992 1031 -17 104 -14 314 6 421 107 555 573 974 1128 1014 105 7 168 5 282
-10z"/>
<path d="M2361 4190 c-51 -4 -108 -11 -127 -15 l-34 -6 0 -724 0 -725 95 0 95
0 0 293 0 292 126 -3 c150 -4 241 13 343 64 155 77 241 217 241 394 0 159 -72
293 -195 366 -99 58 -320 84 -544 64z m374 -170 c121 -46 182 -146 173 -284
-8 -127 -71 -213 -187 -257 -63 -24 -190 -35 -275 -25 l-56 7 0 289 0 289 38
4 c20 3 84 4 142 2 80 -2 119 -8 165 -25z"/>
</g>
</svg>`;

// Use the iconUrl variable defined in the HTML template
var customIcon = L.divIcon({
  className: "custom-icon",
  html: svgIcon, // Use the SVG content here
  iconSize: [25, 41], // Size of the icon [width, height]
  iconAnchor: [12, 41], // Point of the icon which will correspond to marker's location
  popupAnchor: [1, -34], // Point from which the popup should open relative to the iconAnchor
});
//

var customIcon1 = L.divIcon({
  className: "custom-icon",
  html: svgicon2, // Use the SVG content here
  iconSize: [25, 41], // Size of the icon [width, height]
  iconAnchor: [22, 41], // Point of the icon which will correspond to marker's location
  popupAnchor: [1, -34], // Point from which the popup should open relative to the iconAnchor
});

getUserLocation();

// Function to get the user's current location
function getUserLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      sendLocationToBackend,
      handleError
    );
    console.log();
  } else {
    alert("Geolocation is not supported by this browser.");
  }
}

function sendLocationToBackend(position) {
  var latitude = position.coords.latitude;
  var longitude = position.coords.longitude;

  const userMarker = L.marker([latitude, longitude]).addTo(map);
  document.querySelector("#loader").classList.remove("d-none");

  // Create a div element for radar animation
  let radarDiv = L.divIcon({
    className: "radar-icon",
    html: '<div class="radar"></div>',
    iconSize: [100, 100],
  });

  // Add the radar icon to the map at the same location as the circular polygon
  let radarMarker = L.marker([latitude, longitude], { icon: radarDiv }).addTo(
    map
  );
  const value = document.querySelector("#status").value;
  if (value === "True") {
    console.log("If Value " + value);
    radarMarker = L.marker([latitude, longitude], { icon: radarDiv }).addTo(
      map
    );
  } else {
    console.log("else value " + value);
    radarMarker.remove();
  }

  // Send the location to the backend
  fetch(`${window.API_URL}/near_parking/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken, // Ensure csrfToken is defined
    },
    body: JSON.stringify({
      latitude: latitude,
      longitude: longitude,
    }),
  })
    .then((response) => {
      if (response.ok) {
        return response.json(); // Parse the JSON response
      } else {
        throw new Error("Error sending location.");
      }
    })
    .then((data) => {
      // Handle the data received from the backend
      console.log("Nearest parking:", data.parkings);
      data.parkings.forEach((element) => {
        var marker = L.marker([element.latitude, element.longitude], {
          icon: customIcon1,
        }).addTo(map);

        marker.bindPopup(`
                  <div class="card" style="width: 18rem; border:none;">
                    <img class="card-img-top" src="${element.image1}" alt="Card image cap">
                    <div class="card-body">
                     <h5 class="card-title">${element.name}</h5>
                     <p class="card-text">${element.address}</p>
                     <p class="card-text">${element.distance} km</p>

                      <button class="btn btn-dark rounded" id="reserve_now" onclick="window.location.href='${window.API_URL}/reserve_parkng/${element.id}' ">Reserve Now</button>
                    </div>
                  </div>
            `);
      });

      const listingsContainer = document.getElementById("listings-container"); // Make sure this ID matches your HTML
      listingsContainer.innerHTML = ""; // Clear previous listings

      data.parkings.forEach((element) => {
        // Create the HTML for each listing
        const listingHTML = `
            <div class="listing-box">
                <div class="image-listing">
                    <img src="${element.image1}" alt="">
                    <img src="${element.image2}" alt="">
                </div>
                <div class="text-listing">
                    <h6>${element.name}</h6>
                    <div class="d-flex align-items-center justify-content-between">
                        <div class="">
                            <div class="d-flex align-items-center py-1">
                                <svg xmlns="http://www.w3.org/2000/svg" class="mx-3" width="33.667" height="14.655" viewBox="0 0 33.667 14.655">
                                <path id="cars-icon" d="M25.6.258h3.562c1.1,0,1.726.929,1.992,1.992l.63,2.578.367-.7c1.9-.11,2.074,1,.06,1.951l.334.493c1.326,1.37,1.2,2.721.995,6.085v1.1a.622.622,0,0,1-.622.622h-2.66a.622.622,0,0,1-.622-.622v-.482h-.986V12.7c.049-.8.093-1.5.115-2.134l1.57-.014a1.063,1.063,0,0,0,.529-.145.9.9,0,0,0,.321-.356l.255-.619c.189-.482.038-.715-.518-.655l-2.151.26a5.444,5.444,0,0,0-.726-2.589,3.178,3.178,0,0,0,.384-.523h0a2.891,2.891,0,0,0,.2-.43h2.23L30.21,2.825C30.035,2,29.528,1.3,28.69,1.3H26.026A5.967,5.967,0,0,0,25.6.258ZM8.566,5.956c-1.918-.97-1.69-2.052.227-1.94l.43.806.885-2.74C10.456.984,11.037,0,12.174,0H22.191c1.137,0,1.789.964,2.066,2.066l.674,2.671.384-.721c1.973-.115,2.151,1.033.06,2.022l.34.521c1.37,1.411,1.244,2.819,1.03,6.3v1.145a.647.647,0,0,1-.644.647H23.333a.647.647,0,0,1-.644-.647v-.515H10.98v.518a.647.647,0,0,1-.647.647H7.593a.647.647,0,0,1-.647-.647V12.42c-.208-2.674-.5-5.085,1.625-6.463Zm3.518,3.173-2.447-.31C9.059,8.756,8.9,9,9.089,9.5l.274.644a.921.921,0,0,0,.329.367,1.121,1.121,0,0,0,.548.153l2.192.016c.526,0,.753-.211.589-.7a1.178,1.178,0,0,0-.932-.852Zm9.5,0,2.447-.31c.575-.063.732.181.548.677l-.277.641a.926.926,0,0,1-.332.367,1.112,1.112,0,0,1-.548.153l-2.192.016c-.529,0-.756-.211-.592-.7a1.181,1.181,0,0,1,.934-.852ZM10.136,5.43h13.8l-.652-2.773c-.2-.844-.723-1.562-1.589-1.562H12.549c-.866,0-1.318.737-1.575,1.562L10.136,5.43ZM8.807.258h-4.3c-1.1,0-1.726.929-1.992,1.992L1.875,4.828l-.367-.7c-1.9-.11-2.074,1-.06,1.951l-.326.493c-1.326,1.37-1.2,2.74-.995,6.1v1.1a.622.622,0,0,0,.622.622h2.66a.622.622,0,0,0,.622-.622v-.493h.992v-.847l-.016-.2c-.044-.57-.09-1.126-.115-1.669l-1.57-.014a1.063,1.063,0,0,1-.526-.132.9.9,0,0,1-.332-.37l-.255-.619c-.178-.482-.019-.715.529-.655L4.9,9.041a6.008,6.008,0,0,1,.874-2.973c-.047-.068-.085-.137-.123-.2a3.11,3.11,0,0,1-.17-.37H2.82l.644-2.674C3.64,2,4.146,1.3,4.985,1.3h3.37A7.307,7.307,0,0,1,8.807.258Z" transform="translate(0.002)" fill="#6046c1" fill-rule="evenodd"/>
                                </svg>
                                <span>${element.available_slots} Spots</span>
                            </div>
                            <div class="d-flex">
                                <svg xmlns="http://www.w3.org/2000/svg" class="mx-4"  width="18.162" height="17.067" viewBox="0 0 18.162 17.067">
                                    <g id="time-alarm" transform="translate(-0.086 -0.086)">
                                        <path id="Path_7" data-name="Path 7" d="M12,7v3.651l2.19,2.19" transform="translate(-2.833 -1.484)" fill="none" stroke="#6046c1" stroke-linecap="square" stroke-width="2"/>
                                        <line id="Line_1" data-name="Line 1" y1="1.825" x2="1.825" transform="translate(2.595 13.913)" fill="none" stroke="#6046c1" stroke-linecap="square" stroke-width="2"/>
                                        <line id="Line_2" data-name="Line 2" x1="1.825" y1="1.825" transform="translate(13.913 13.913)" fill="none" stroke="#6046c1" stroke-linecap="square" stroke-width="2"/>
                                        <circle id="Ellipse_3" data-name="Ellipse 3" cx="6.571" cy="6.571" r="6.571" transform="translate(2.595 2.595)" fill="none" stroke="#6046c1" stroke-linecap="square" stroke-width="2"/>
                                        <line id="Line_3" data-name="Line 3" x1="2.19" y1="2.19" transform="translate(14.643 1.5)" fill="none" stroke="#6046c1" stroke-linecap="square" stroke-width="2"/>
                                        <line id="Line_4" data-name="Line 4" y1="2.19" x2="2.19" transform="translate(1.5 1.5)" fill="none" stroke="#6046c1" stroke-linecap="square" stroke-width="2"/>
                                    </g>
                                    </svg>

                                <span>${Math.round(
                                  element.distance
                                )} mins</span>
                            </div>
                        </div>
                        <div class="white-line"></div>
                        <div class="value">
                            <h5>${element.price} Birr/hr</h5>
                        </div>
                    </div>
                </div>
                <div class="d-flex flex-column align-items-center justify-content-center py-3">
                    <button class="btn btn-primary rounded w-100" onclick="reserve_function(${
                      element.id
                    })">Reserve Now <i class="fa-solid fa-square-parking"></i></button>
                    <button class="btn btn-outline-primary rounded w-100 mt-2" onclick="window.location.href='${
                      window.API_URL
                    }/reserve_parkng/${element.id}'">Send Request <i class="fa-solid fa-paper-plane"></i> </button>
                </div>
                <div class="horizontal-line"></div>
            </div>
        `;

        // Insert the generated HTML into the DOM
        listingsContainer.innerHTML += listingHTML;
      });

      // Set the center of the map to the current location of the user
      map.setView([position.coords.latitude, position.coords.longitude], 15);
    })

    .catch((error) => {
      console.error("Error:", error);
    })
    .finally(() => {
      // Hide the loading indicator
      document.querySelector("#loader").classList.add("d-none");
    });
}
// Function to handle errors
function handleError(error) {
  switch (error.code) {
    case error.PERMISSION_DENIED:
      alert("User  denied the request for Geolocation.");
      break;
    case error.POSITION_UNAVAILABLE:
      alert("Location information is unavailable.");
      break;
    case error.TIMEOUT:
      alert("The request to get user location timed out.");
      break;
    case error.UNKNOWN_ERROR:
      alert("An unknown error occurred.");
      break;
  }
}

// Call the function to get the user's location

// Funciont To visibity
function showSection(section) {
  // Hide all sections
  var sections = document.querySelectorAll(".content-section");
  sections.forEach(function (sec) {
    sec.classList.add("d-none");
    sec.classList.remove("d-block");
  });

  // Show the selected section
  var activeSection = document.getElementById(section);
  activeSection.classList.remove("d-none");
  activeSection.classList.add("d-block");

  // Optionally, update the active class for the nav links
  var navLinks = document.querySelectorAll(".nav-link");
  navLinks.forEach(function (link) {
    link.classList.remove("active");
  });
  document
    .querySelector(`a[onclick="showSection('${section}')"]`)
    .classList.add("active");
}

const showDirection = document.querySelectorAll("#show_direction");
showDirection.forEach((item) => {
  item.addEventListener("click", function (e) {
    console.log("item clicked");
    console.log(e);
  });
});
