document.addEventListener('DOMContentLoaded', function () {
            fetch('/get_chart_data/')
                .then(response => response.json())
                .then(data => {
                    // Wydobywanie danych
                    var timeLabels = data.time_labels;
                    var temperatures = data.temperatures;
                    var hTotal = data.H_Total;
                    var eTotal = data.E_Total;
                    var eToday = data.E_Today;

                    // Tworzenie wykresu liniowego
                    const ctx = document.getElementById('myChart');

                    new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: timeLabels,
                            datasets: [{
                                label: 'Temperature',
                                data: temperatures,
                                borderColor: 'rgba(75, 192, 192, 1)',
                                borderWidth: 1,
                                fill: false,
                            },
                            {
                                label: 'H_Total',
                                data: hTotal,
                                borderColor: 'rgba(255, 99, 132, 1)',
                                borderWidth: 1,
                                fill: false,
                            },
                            {
                                label: 'E_Total',
                                data: eTotal,
                                borderColor: 'rgba(31, 12, 242, 1)',
                                borderWidth: 1,
                                fill: false,
                            },
                            {
                                label: 'E_Today',
                                data: eToday,
                                borderColor: 'rgba(0, 255, 8, 1)',
                                borderWidth: 1,
                                fill: false,
                            }]
                        },
                        options: {
                            scales: {
                                x: [{
                                    display: true,
                                    scaleLabel: {
                                        display: true,
                                        labelString: 'Time Labels'
                                    }
                                }],
                                y: [{
                                    display: true,
                                    scaleLabel: {
                                        display: true,
                                        labelString: 'Temperature and H_Total'
                                    }
                                }]
                            }
                        }
                    });
                });
        });