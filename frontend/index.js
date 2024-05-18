
src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"


document.addEventListener("DOMContentLoaded", function(){
  if(document.getElementById('stock-chart')){
    loadStocks();
  }
})

function createChart(bloodTypes,currentStocks,criticalStocks,backgroundColors){
  // Create the chart
  var ctx = document.getElementById('stock-chart').getContext('2d');
  console.log(currentStocks);
  var chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: bloodTypes,
      datasets: [
        {
          label: 'Current Stock',
          data: currentStocks,
          backgroundColor: backgroundColors,
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        },
        {
          label: 'Critical Stock',
          data: criticalStocks,
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

function loadStocks(){
    axios.get('/lookup-blood-stock', {}).then(function(response) {
    var stocks = response.data;
    var bloodTypes = [];
    var currentStocks = [];
    var criticalStocks = [];
    var backgroundColors = []

    for (var i = 0; i < stocks.length; i++) {
      // Collect data for the chart
      bloodTypes.push(stocks[i]['type']);
      currentStocks.push(stocks[i]['stock']);
      criticalStocks.push(stocks[i]['criticalstock']);
      if (stocks[i]['stock'] < stocks[i]['criticalstock']) {
        backgroundColors.push('rgba(255, 99, 132, 0.6)'); // Vivid color for low stock
      } else {
        backgroundColors.push('rgba(54, 162, 235, 0.2)'); // Default color
      }
    }
    createChart(bloodTypes,currentStocks,criticalStocks,backgroundColors);
    
  });
};

