const progressBarContainer = document.querySelector('.progress-bar__container');

 

const progressBar = document.querySelector('.progress-bar');

 

const progressBarText = document.querySelector('.progress-bar__text');

 

 

 

const targetPercentage = 10; // You can set the desired percentage here

 

 

 

const getColor = (percentage) => {

 

    if (percentage <= 30) {

 

        return 'green';

 

    } else if (percentage >= 100) {

 

        return 'red';

 

    } else {

 

        return 'yellow';

 

    }

 

};

 

 

 

const setColor = (percentage) => {

 

    const color = getColor(percentage);

 

    progressBar.style.backgroundColor = color;

 

};

 

 

 

gsap.to(progressBar, {

 

    width: `${targetPercentage}%`,

 

    duration: 2,

 

    onUpdate: () => {

 

        const currentWidth = parseFloat(progressBar.style.width);

 

        const displayText = currentWidth === 100 ? 'Parking Full' : `${Math.round(currentWidth)}% full`;

 

        progressBarText.textContent = displayText;

 

        setColor(currentWidth);

 

    },

 

    onComplete: () => {

 

        progressBarText.style.display = "initial";

 

        progressBarContainer.style.boxShadow = '0 0 5px #4895ef';

 

    }

 

});
var bikecount = 20
var carcount = 30
document.getElementById('biketext').innerHTML = (bikecount)
document.getElementById('cartext').innerHTML = (carcount)

 