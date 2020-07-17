var ctx = document.getElementById('myChart').getContext('2d');


checkins = checkins.slice(1, -1).split(",");
let date = new Date(date_created)
console.log(checkins);

let data = []
let num = 1;
if (checkins[0] != 0){
    for (let i = 0; i < checkins[0]; i++){
        data.push(0);
    }
}

for (let i = 0; i < checkins.length-1; i++){
    let x = parseInt(checkins[i])+1;
    data.push(num);
    let next = parseInt(checkins[i+1])+1
    while (x+1 < next){
        data.push(num);
        x++;
    }
    num++;
}
data.push(num++);

let labels = [date.getMonth()+1 + "/" + date.getDate()];
for (var i = 1; i < data.length; i++){
    date.setDate(date.getDate() + 1)
    let x = new Date(date);
    labels.push(x.getMonth()+1 + "/" + x.getDate())
}
let x = new Date(date.setDate(date.getDate() + 1));
let nextDate = x.getMonth()+1 + "/" + x.getDate();


console.log(data)
console.log(labels);

var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: "Check In Progression",
            backgroundColor: 'rgb(125, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: data,
            lineTension: 0,
    }]},
    options: {
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
                    suggestedMax: 66,
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
var width = parseFloat(style.getPropertyValue('--width'))
progressBar.style.setProperty('--width', checkins.length);

function addData() {
    // Doesn't work when you missed days, as it adds one on as if theres a streak
    // myChart.data.labels.push(nextDate);
    // myChart.data.datasets.forEach((dataset) => {
    //     dataset.data.push(num);
    // });
    // myChart.update();
    let width = parseFloat(style.getPropertyValue('--width'))
    progressBar.style.setProperty('--width', width + 1);
}
