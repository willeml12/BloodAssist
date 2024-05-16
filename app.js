/**
 * Copyright (c) 2024, Sebastien Jodogne, ICTEAM UCLouvain, Belgium
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use, copy,
 * modify, merge, publish, distribute, sublicense, and/or sell copies
 * of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
 * BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
 * ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 **/


var observations = {};
src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"

/**
 * TODO : When a user is logged in, allow the possibility to change values like weight, ...
 */

/**
 * Register client information in database
 * Information comes from the inputs on the question page
 */
// document.getElementById('register-btn').addEventListener('click', function() {

//   console.log("Inside app.js")
//   var name = document.getElementById('name').value;
//   var dob = document.getElementById('dob').value;
//   var gender = document.getElementById('gender').value;
//   var btype = document.getElementById('btype').value;

//   if (!name) {
//       alert('No name was provided');
//       return;
//   }

//   console.log("Document info collected");

//   var date = new Date(dob);
//   var today = new Date();
//   var age = today.getFullYear() - date.getFullYear();
//   var m = today.getMonth() - date.getMonth();
//   if (m < 0 || (m === 0 && today.getDate() < date.getDate())) {
//       age--;
//   }

//   axios.post('register-user', {
//       name: name,
//       dob: dob,
//       age: age,
//       gender: gender,
//       btype: btype
//   })
//   .then(function(response) {
//       document.getElementById('name').value = '';
//       document.getElementById('dob').value = '';
//       document.getElementById('gender').value = '';
//       document.getElementById('type').value = '';
//       console.log("Response sent")
//   })
//   .catch(function(response) {
//       alert('Error at /questions : Failed to register user');
//   });
// });

/**
 * Retrieve stocks from database 
 */
// window.onload =function LookupStocks() {
//   axios.post('/lookup-blood-stock', {}).then(function(response) {
//     $('#stocks').empty();
//     var stocks = response.data;
//     var critical = false; // flag to indicate critical stock levels

//     for (var i = 0; i < stocks.length; i++) {
//       var dom = $('#stock-template').clone();
//       dom.attr('type', stocks[i]['type']);
//       $('.type', dom).text(stocks[i]['type']);
//       $('.stock', dom).text(stocks[i]['stock']);
//       $('.criticalstock', dom).text(stocks[i]['criticalstock']);

//       if (parseInt(stocks[i]['stock']) < parseInt(stocks[i]['criticalstock'])) {
//         critical = true;
//         $('.stock', dom).addClass('text-danger'); // Adding a class for low stock visualization
//       }

//       $('#stocks').append(dom);
//     }

//   });
// }

document.addEventListener("DOMContentLoaded", function(){
  if(document.getElementById('stock-chart')){
    loadStocks();
  }
})

function loadStocks(){
    axios.post('/lookup-blood-stock', {}).then(function(response) {
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
  });
};

