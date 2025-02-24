let moodChart;

function createMoodChart(dates, moodValues) {
    const ctx = document.getElementById('moodChart');
    
    if (ctx) {
        // Destroy existing chart if it exists
        if (moodChart) {
            moodChart.destroy();
        }

        moodChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Mood',
                    data: moodValues,
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.1,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 6,
                        title: {
                            display: true,
                            text: 'Mood'
                        },
                        ticks: {
                            stepSize: 1,
                            callback: function(value, index, values) {
                                return ['', 'Sad', 'Neutral', 'Calm', 'Grateful', 'Happy', 'Excited'][value];
                            }
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    }
                }
            }
        });
    }
}

function updateMoodChart(dates, moodValues) {
    if (moodChart) {
        moodChart.data.labels = dates;
        moodChart.data.datasets[0].data = moodValues;
        moodChart.update();
    } else {
        console.error('Mood chart not initialized');
    }
}