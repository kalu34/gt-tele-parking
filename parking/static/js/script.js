
const menu = document.querySelector('.menu');
const close = document.querySelector('.close-x');
const menuBar = document.querySelector('.left_menu');

menu.addEventListener('click', function () {
  menuBar.classList.toggle('d-block');
});

close.addEventListener('click', function () {
  menuBar.classList.toggle('d-block');
});
