var startDiv = document.querySelector('#start')
var stopDiv = document.querySelector('#stop')
var startButton = document.querySelector('#startButton');
var stopButton = document.querySelector('#stopButton');
startButton.addEventListener('click', function (e) {
    e.preventDefault();
    startDiv.parentElement.classList.toggle('active');
})
stopButton.addEventListener('click', function (e) {
    e.preventDefault();
    stopDiv.parentElement.classList.toggle('active');
})