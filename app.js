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

// /**
//  * Register a new blood donnor 
//  */
// window.onload=function(){
//   document.getElementById('submit-btn').addEventListener('click', function() {
//     var fname = document.getElementById('Fname').value;
//     var lname = document.getElementById('Lname').value;
//     var email = document.getElementById('email').value;
//     var btype = document.getElementById('btype').value;
//     console.log('User %s %s with Blood type %s',fname,lname,btype)
//     if (fname == '' || lname == '') {
//       alert('Name is not complete');
//     } else {
//       axios.post('create-user', {
//         fname: fname,
//         lname: lname,
//         email: email,
//         btype: btype
//       })
//         .then(function(response) {
//           document.getElementById('fname').value = '';
//           document.getElementById('lname').value = '';
//           var gender = document.getElementById('email').value;
//           var btype = document.getElementById('btype').value;
//         })
//         .catch(function(response) {
//           alert('URI /create-user not properly implemented in Flask');
//         });
//     }
//   });
// }

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
function LookupStocksV1() {
  axios.post('/lookup-blood-stock', {}).then(function(response) {
    $('#stocks').empty();
    var stocks = response.data;
    var critical = false; // flag to indicate critical stock levels

    for (var i = 0; i < stocks.length; i++) {
      var dom = $('#stock-template').clone();
      dom.attr('type', stocks[i]['type']);
      $('.type', dom).text(stocks[i]['type']);
      $('.stock', dom).text(stocks[i]['stock']);
      $('.criticalstock', dom).text(stocks[i]['criticalstock']);

      if (parseInt(stocks[i]['stock']) < parseInt(stocks[i]['criticalstock'])) {
        critical = true;
        $('.stock', dom).addClass('text-danger'); // Adding a class for low stock visualization
      }

      $('#stocks').append(dom);
    }

  });
}

document.addEventListener("DOMContentLoaded", function(){
    axios.post('/lookup-blood-stock', {}).then(function(response) {
    var stocks = response.data;
    var bloodTypes = [];
    var currentStocks = [];
    var criticalStocks = [];

    for (var i = 0; i < stocks.length; i++) {
      // Collect data for the chart
      bloodTypes.push(stocks[i]['type']);
      currentStocks.push(stocks[i]['stock']);
      criticalStocks.push(stocks[i]['criticalstock']);
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
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
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
});

// /**
//  * Load and display blood stocks
// //  */
// document.addEventListener("DOMContentLoaded", function(){
//   const ctx = document.getElementById('stock-chart').getContext('2d');
//   const chart = new Chart(ctx, {
//     type: 'bar',
//       data: {
//         labels: [],
//         datasets: [
//           {
//             label: 'Current Stock',
//             backgroundColor: 'rgba(75, 192, 192, 0.2)',
//             borderColor: 'rgba(75, 192, 192, 1)',
//             borderWidth: 1,
//             data: []
//           },
//           {
//             label: 'Critical Stock',
//             backgroundColor: 'rgba(255, 99, 132, 0.2)',
//             borderColor: 'rgba(255, 99, 132, 1)',
//             borderWidth: 1,
//             data: []
//           }
//         ]
//       },
//       options: {
//         scales: {
//           y: {
//             beginAtZero: true
//           }
//         }
//       }
//     });  
// });

// function DisplayContent(event) {
//   $('#observations > a').removeClass('active');
//   $(event.currentTarget).addClass('active');

//   $('#content').empty();

//   var index = $(event.currentTarget).attr('index');
//   var content = observations[index].parameters;
  
//   for (var i = 0; i < content.length; i++) {
//     var tr = $('<tr>');
//     tr.append($('<th>').text(content[i]['name']));
//     tr.append($('<td>').text(content[i]['value']));
//     $('#content').append(tr);
//   }
// }

// function LookupPatients() {
//   axios.post('/lookup-patients', {
//     'family' : document.getElementById('patient-family').value,
//     'ehr-id' : document.getElementById('patient-ehr-id').value,
//   }).then(function(response) {
//     $('#patients').empty();
//     $('#observations').empty();
//     $('#content').empty();

//     if (response.data.complete) {
//       $('#incomplete').hide();
//     } else {
//       $('#incomplete').show();
//     }

//     var patients = response.data.patients;
    
//     for (var i = 0; i < patients.length; i++) {
//       var dom = $('#patient-template').clone();
//       dom.attr('fhir-id', patients[i]['fhir-id']);
//       $('.patient-family', dom).text(patients[i]['family']);
//       $('.patient-first-name', dom).text(patients[i]['first-name']);
//       $('.patient-fhir-id', dom).text(patients[i]['fhir-id']);
//       $('.patient-ehr-ids', dom).text(patients[i]['ehr-ids'].join(', '));
//       $(dom.click(LookupObservations));
//       $('#patients').append(dom);
//     }
//   });
// }


// document.addEventListener('DOMContentLoaded', function() {
//   document.getElementById('lookup').addEventListener('click', function(event) {
//     LookupPatients();
//     event.preventDefault();
//   });
// });
