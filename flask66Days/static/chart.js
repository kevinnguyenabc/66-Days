var ctx = document.getElementById('myChart').getContext('2d');


checkins = checkins.slice(1, -1).split(",");
let date = new Date(date_created)
console.log(checkins);

let data = []
let num = 1;
for (let i = 0; i < checkins.length-1; i++){
    let x = parseInt(checkins[i])+1;
    data.push(num);
    let next = parseInt(checkins[i+1])+1
    while (x+1 < next){
        console.log(x, next, "true")
        data.push(num);
        x++;
    }
    num++;
}
data.push(num);

let labels = [];
for (var i = 0; i < data.length; i++){
    date.setDate(date.getDate() + 1)
    let x = new Date(date);
    labels.push(x.getMonth()+1 + "/" + x.getDate())
}


console.log(data)
console.log(labels);

var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: "easdf",
            backgroundColor: 'rgb(125, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: data,
            lineTension: 0,
    }]},
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    suggestedMax: 66,
                    stepSize: 2,
                    beginAtZero: true
                }
            }]
        }
    }
});


