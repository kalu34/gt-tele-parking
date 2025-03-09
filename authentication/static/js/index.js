const menuBtn = document.querySelector('.menu');
const closeBtn = document.querySelector('.menu-close');
const nav_bar = document.querySelector('.nav-bar');

// Open the nav bar
menuBtn.addEventListener('click', function () {
  nav_bar.style.display = 'inline-block';
});

// Close the nav bar
closeBtn.addEventListener('click', function () {
  nav_bar.style.display = 'none';
});

// Close the nav bar when a link is clicked
const navLinks = nav_bar.querySelectorAll('a'); // Select all links inside nav_bar
navLinks.forEach(link => {
  link.addEventListener('click', function () {
    nav_bar.style.display = 'none';
  });
});
