console.log(habits);

let data = [];
let labels = [];
let bgcolors = [];
let bdcolors = [];
for (const [key, value] of Object.entries(habits)) {
    labels.push(key);
    data.push(value);
    if (value >= 66) {
        bgcolors.push('rgba(157, 197, 124, .6)')
        bdcolors.push('rgb(144, 206, 93, .9)')
    } else {
        bgcolors.push('rgb(125, 99, 132)');
        bdcolors.push('rgb(255, 99, 132)')
    }
}

var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [{
            label: "Your Habits",
            backgroundColor: bgcolors,
            borderColor: bdcolors,
            borderWidth: 1.3,
            barPercentage: .5,
            data: data,
    }]},
    options: {
        maintainAspectRatio: false, 
        legend: {
            onClick: (e) => e.stopPropagation(),
            labels: {
                boxWidth: 0,
                fontColor: 'white',
                fontSize: 18,
            }
         },
        scales: {
            yAxes: [{
                drawTicks: false,
                ticks: {
                    fontColor: "rgb(198, 209, 248)",
                    stepSize: 2,
                    beginAtZero: true,
                    suggestedMax: 10,
                }
            }],
            xAxes: [{
                ticks: {
                    fontColor: "rgb(198, 209, 248)",
                }
            }]
        }
    }
});



const progressBar = document.getElementsByClassName('progress-bar')[0];
const style = getComputedStyle(progressBar);
progressBar.style.setProperty('--width', v);
progressBar.style.setProperty('--scale', 100 / s + "%");

if (v === s && v > 0){
    setTimeout( function() {
        progressBar.style.setProperty("animation", "1s pulse");
    }, 2000);

}