console.log("async")

let myChart;  // This will store the chart instance
const sendConsumerBtn = document.getElementById('sendConsumerBtn');

var currentPage = window.location.pathname.slice(1);
if (currentPage.endsWith('/')) {
    currentPage = currentPage.slice(0, -1);
}
const socket = new WebSocket(`ws://${window.location.host}/ws/${currentPage}/`);

socket.onmessage = function(e) {
    const data = JSON.parse(e.data)
    const time = data["time"]
    const stock_data = data["serialized_data"][0]
    const closes = stock_data["closes"]
    const dates = stock_data["dates"]
    const ticker = stock_data["name"]
    console.log('From Server: ' + ticker)

    let filteredDates = [];
    let filteredCloses = [];
    let count = 0;
    for(let i = dates.length - 1; i >= 0; i--) {  // Start from the most recent date and work backward
            filteredDates.unshift(dates[i]);
            filteredCloses.unshift(closes[i]);
            if( count++ >= time){
                break;
            }
    }

    const ctx = document.getElementById('myChart').getContext('2d');

    if (myChart) {
        myChart.destroy();  // Destroy the previous chart instance if it exists
    }

     myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: filteredDates,
            datasets: [{
                label: ticker,
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

};

socket.onopen = function(e) {
    console.log('on open')
//    socket.send(JSON.stringify({
//        'message': 'hello from client',
//        'sender': 'iris',
//    }));
};

socket.onerror = function(error) {
    console.log('ERROR')
    // Handle any error that occurs
};

socket.onclose = function(event) {
    console.log('socket closed')
    // WebSocket is closed
};

sendConsumerBtn.addEventListener('click', function() {
    const selectedTime = parseInt(document.getElementById('timeSelect').value);
    const selectedData = document.getElementById('dataSelect').value;
    socket.send(JSON.stringify({
        'ticker': selectedData,
        'time': selectedTime,
    }));
});