function myFunc() {
    return CORE_N5, CORE_N4, CORE_N3, CORE_N2, CORE_N1
}
CORE_N5, CORE_N4, CORE_N3, CORE_N2, CORE_N1 = myFunc()

var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['N5', 'N4', 'N3', 'N2', 'N1'],
        datasets: [{
            label: '% of words by JLPT level (N5 = Easy --> N1 = Hard)',
            data: [CORE_N5, CORE_N4, CORE_N3, CORE_N2, CORE_N1],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});