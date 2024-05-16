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
 * Register a new blood donnor 
 */
window.onload=function(){
  document.getElementById('patient-button').addEventListener('click', function() {
    var name = document.getElementById('patient-name').value;
    var btype = document.getElementById('patient-type').value;
    console.log('User %s with Blood type %s',name,btype)
    if (name == '') {
      alert('No name was provided');
    } else {
      axios.post('create-patient', {
        name: name,
        btype: btype
      })
        .then(function(response) {
          document.getElementById('patient-name').value = '';
          document.getElementById('patient-type').value = '';
        })
        .catch(function(response) {
          alert('URI /create-patient not properly implemented in Flask');
        });
    }
  });
}

/**
 * Retrieve stocks from database 
 */
window.onload =function LookupStocks() {
  axios.post('/lookup-blood-stock', {}).then(function(response) {
    $('#stocks').empty();

    var stocks = response.data.stocks;
    console.log(stocks);
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


// function LookupObservations(event) {
//   $('#patients > a').removeClass('active');
//   $(event.currentTarget).addClass('active');

//   axios.post('/lookup-observations', {
//     'patient-id' : $(event.currentTarget).attr('fhir-id'),
//   }).then(function(response) {
//     $('#observations').empty();
//     $('#content').empty();

//     observations = response.data;
    
//     for (var i = 0; i < observations.length; i++) {
//       var dom = $('#observation-template').clone();
//       dom.attr('index', i);
//       $('.observation-index', dom).text(i + 1);
//       $('.observation-count', dom).text(observations.length);
//       $('.observation-time', dom).text(observations[i]['time']);
//       $(dom.click(DisplayContent));
//       $('#observations').append(dom);
//     }
//   });  
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
