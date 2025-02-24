let moodChart;

function createMoodChart(dates, moodValues) {
    const ctx = document.getElementById('moodChart');

    if (ctx) {
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
                            callback: function (value, index, values) {
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

function updateMoodChart() {
    fetch('/get_mood_data')
        .then(response => response.json())
        .then(data => {
            if (moodChart) {
                moodChart.data.labels = data.dates;
                moodChart.data.datasets[0].data = data.mood_values;
                moodChart.update();
            } else {
                createMoodChart(data.dates, data.mood_values);
            }
        })
        .catch(error => console.error('Error fetching mood data:', error));
}

function addEntry(event) {
    event.preventDefault();
    const form = event.target;

    fetch(form.action, {
        method: form.method,
        body: new FormData(form)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Entry added successfully:', data);
            alert(data.message);
            updateMoodChart();
            form.reset();
            window.location.href = data.redirect;
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while saving your entry. Please try again.');
        });
}

function initializePage() {
    updateMoodChart();

    const entryForm = document.getElementById('addEntryForm');
    if (entryForm) {
        entryForm.addEventListener('submit', addEntry);
    }
}

document.addEventListener('DOMContentLoaded', initializePage);