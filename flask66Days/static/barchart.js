console.log(habits);

let data = [];
let labels = []
let num = 0;
for (const [key, value] of Object.entries(habits)) {
    labels.push(key);
    data.push(value);
    if (value >= 66) {
        num++;
    }
}
$("#num").text(num);

var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [{
            label: "Your Habits",
            backgroundColor: 'rgb(125, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            borderWidth: 1.3,
            barPercentage: .7,
            data: data,
    }]},
    options: {
        maintainAspectRatio: false, 
        legend: {
            onClick: (e) => e.stopPropagation(),
            labels: {
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

if (v === s){
    setTimeout( function() {
        progressBar.style.setProperty("animation", "1s pulse");
    }, 2000);

}