bday = "03/09/2001";


const daysDisplay = document.getElementById("days");
const hoursDisplay = document.getElementById("hours");
const minutesDisplay = document.getElementById("minutes");
const secondsDisplay = document.getElementById("seconds");


function countdown() {
    const today = new Date();
    let birthday = new Date(bday);

    let secondsDifference = (birthday.getTime() - today.getTime()) / 1000;
    let bdayData;

    //Ensures the countdown will never be negative
    while(secondsDifference < 0){
        bdayData = bday.split("/");
        year = Number(bdayData[2]);
        year += 1;
        bday = "03/09/" + year
        birthday = new Date(bday);
        secondsDifference = (birthday.getTime() - today.getTime()) / 1000;
    }

    const seconds = Math.floor(secondsDifference) % 60;
    const minutes = Math.floor(secondsDifference/60) % 60;
    const hours = Math.floor(secondsDifference / 3600) % 24;
    const days = Math.floor(secondsDifference / (60*60*24));

    daysDisplay.innerHTML = days;
    hoursDisplay.innerHTML = addZeros(hours);
    minutesDisplay.innerHTML = addZeros(minutes);
    secondsDisplay.innerHTML = addZeros(seconds);
}

//Ensure that any value under 10 will be padded with an extra zero, e.g. 06 instead of 6
function addZeros(val){
    if(val < 10){
        return `0${val}`;
    }
    else{
        return val;
    }
}

//Every second call the countdown function to refresh the timer
countdown();
setInterval(countdown,1000)