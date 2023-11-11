function getDates(ticker){
//        console.log("ticker:" + ticker);
        const entry = data.find(e => e.name === ticker);
        if (entry) {
            return entry.dates;
        } else {
            console.log("NOT found");
            return null;
        }
    }

function getCloses(ticker){
//    console.log("ticker:" + ticker);
    const entry = data.find(e => e.name === ticker);
    if (entry) {
        return entry.closes;
    } else {
        console.log("NOT found");
        return null;
    }
}

const loadChartBtn = document.getElementById('loadChartBtn');
const overlayBtn = document.getElementById('overlayBtn');
let myChart;  // This will store the chart instance

loadChartBtn.addEventListener('click', function() {
    const selectedTime = parseInt(document.getElementById('timeSelect').value);
    const selectedData = document.getElementById('dataSelect').value;
    const selectedDataName = document.getElementById('dataSelect').key;
    const dates = getDates(selectedData)
    const closes = getCloses(selectedData)

    let filteredDates = [];
    let filteredCloses = [];
    let count = 0;
    for(let i = dates.length - 1; i >= 0; i--) {  // Start from the most recent date and work backward
            filteredDates.unshift(dates[i]);
            filteredCloses.unshift(closes[i]);
            if( count++ >= selectedTime){
                break;
            }
    }
//    console.log("checkpoint1");

    const ctx = document.getElementById('myChart').getContext('2d');

    if (myChart) {
        myChart.destroy();  // Destroy the previous chart instance if it exists
    }

    myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: filteredDates,
            datasets: [{
                label: selectedData,
                data: filteredCloses,
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            plugins: {
                zoom: {
                    pan: {
                        enabled: true,
                        mode: 'xy'
                    },
                    zoom: {
                        wheel: {
                            enabled: true, // Enable or disable zooming by mouse wheel
                        },
                        pinch: {
                            enabled: true // Enable or disable zooming by pinch gestures (for touch devices)
                        },
                        mode: 'xy'
                    }
                }
            }
        }
    });
});

overlayBtn.addEventListener('click', function() {
    const selectedTime = parseInt(document.getElementById('timeSelect').value);
    const selectedData = document.getElementById('dataSelect').value;
    const dates = getDates(selectedData)
    const closes = getCloses(selectedData)

    let filteredDates = [];
    let filteredCloses = [];
    let count = 0;
    for(let i = dates.length - 1; i >= 0; i--) {  // Start from the most recent date and work backward
            filteredDates.unshift(dates[i]);
            filteredCloses.unshift(closes[i]);
            if( count++ >= selectedTime){
                break;
            }
    }
//    console.log("checkpoint1");

    const ctx = document.getElementById('myChart').getContext('2d');

    var newDataset = {
        label: selectedData,
        data: filteredCloses,
        borderColor: 'red',
        fill: false
    };

    myChart.data.datasets.push(newDataset);

    myChart.update();
});

