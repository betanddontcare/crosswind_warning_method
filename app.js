let startDiv = document.querySelector('#start')
let stopDiv = document.querySelector('#stop')
let startButton = document.querySelector('#startButton');
let stopButton = document.querySelector('#stopButton');
let computeButton = document.querySelector('#toData');

startButton.addEventListener('click', function (e) {
    e.preventDefault();
    startDiv.parentElement.classList.toggle('active');
})
stopButton.addEventListener('click', function (e) {
    e.preventDefault();
    stopDiv.parentElement.classList.toggle('active');
})
computeButton.addEventListener('click', function (e) {
    let max_velocity = document.querySelector('#max_velocity').value;
    let front_area = document.querySelector('#front_area').value;
    let distance_axles = document.querySelector('#distance_axles').value;
    let front_axle_load = document.querySelector('#front_axle_load').value;
    let weight = document.querySelector('#weight').value;
    let wheel_radius = document.querySelector('#wheel_radius').value;
    let altitude = document.querySelector('#altitude').value;
    let rear_axle_load = document.querySelector('#rear_axle_load').value;
    let start = document.querySelector('#start').value;
    let stop = document.querySelector('#stop').value;
    e.preventDefault();
    fetch('http://127.0.0.1:8000/', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "start": start,
            "stop": stop,
            "max_velocity": max_velocity,
            "front_area": front_area,
            "distance_axles": distance_axles,
            "front_axle_load": front_axle_load,
            "weight": weight,
            "wheel_radius": wheel_radius,
            "altitude": altitude,
            "rear_axle_load": rear_axle_load
        })
    }).then(res => res.json()).then(res => console.log(res));
})

var rangeSlider = function () {
    var slider = $('.range-slider'),
        range = $('.range-slider__range'),
        value = $('.range-slider__value');

    slider.each(function () {

        value.each(function () {
            var value = $(this).prev().attr('value');
            $(this).html(value);
        });

        range.on('input', function () {
            $(this).next(value).html(this.value);
        });
    });
};

rangeSlider();