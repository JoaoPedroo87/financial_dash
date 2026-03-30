const data = window.chartData;

const labels = data.map(item => item[0]);
const values = data.map(item => item[1]);

new Chart(document.getElementById('myChart'), {
    type: 'pie',
    data: {
        labels: labels,
        datasets: [{
            data: values
        }]
    }
});