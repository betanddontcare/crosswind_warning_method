let startDiv = document.querySelector('#start')
let stopDiv = document.querySelector('#stop')
let startButton = document.querySelector('#startButton');
let stopButton = document.querySelector('#stopButton');
let computeButton = document.querySelector('#toData');

class MainComponent {
    constructor() {
      this.frontSide = document.querySelector('.main-component__side--front');
      this.backSide = document.querySelector('.main-component__side--back');
    }
  
    rotateComponent() {
      this.frontSide.style.transform = "rotateY(-180deg)";
      this.backSide.style.transform = "rotateY(0)";
    }
  }

const mainComponent = new MainComponent();

startButton.addEventListener('click', function (e) {
    e.preventDefault();
    startDiv.parentElement.classList.toggle('active');
})
stopButton.addEventListener('click', function (e) {
    e.preventDefault();
    stopDiv.parentElement.classList.toggle('active');
})
computeButton.addEventListener('click', function (e) {
    let max_velocity = Number(document.querySelector('#max_velocity').value);
    let front_area = Number(document.querySelector('#front_area').value);
    let distance_axles = Number(document.querySelector('#distance_axles').value);
    let front_axle_load = Number(document.querySelector('#front_axle_load').value);
    let weight = Number(document.querySelector('#weight').value);
    let wheel_radius = Number(document.querySelector('#wheel_radius').value);
    let altitude = Number(document.querySelector('#altitude').value);
    let rear_axle_load = Number(document.querySelector('#rear_axle_load').value);
    let start = document.querySelector('#start').value;
    let stop = document.querySelector('#stop').value;
    let rough = document.querySelector('input[name="menu"]:checked').value;
    let resCoe = Number(document.querySelector('#resCoe').value);
    e.preventDefault();
    runLoader();
    fetch('http://127.0.0.1:8000/', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "max_velocity": max_velocity,
            "front_area": front_area,
            "distance_axles": distance_axles,
            "front_axle_load": front_axle_load,
            "weight": weight,
            "wheel_radius": wheel_radius,
            "altitude": altitude,
            "rear_axle_load": rear_axle_load,
            "start" : parseCoords(start),
            "stop": parseCoords(stop),
            "rough" : roughCoe(rough),
            "resCoe" : resCoe   
        })
    }).then(res => res.json()).then(res => console.log(res));
    setTimeout(stopLoader, 5000);
    setTimeout(reverse, 6000);
})

let rangeSlider = function() {
    let slider = $('.range-slider'),
        range = $('.range-slider__range'),
        value = $('.range-slider__value');

    slider.each(function() {

        value.each(function() {
            let value = $(this).prev().attr('value');
            $(this).html(value);
        });

        range.on('input', function() {
            $(this).next(value).html(this.value);
        });
    });
};

let roughCoe = function(coe) {
    if (coe == 'coastal') {
        return 0.003 ;
    }
    else if (coe == 'plain') {
        return 0.01;
    }
    else if (coe == 'lowland') {
        return 0.05;
    }
    else if (coe == 'varied') {
        return 0.3;
    }
    else {
        return 1
    }
}

let parseCoords = function(coords) {
    return coords.split(',').map(a => {
        return parseInt(a, 10);
    });
}

let runLoader = function() {
    let loader = document.querySelector('.loader-opa');
    loader.className = 'loader';
}

let stopLoader = function() {
    let loader = document.querySelector('.loader');
    loader.className = 'loader-opa';
}

function reverse() {
    mainComponent.rotateComponent();
}

rangeSlider();