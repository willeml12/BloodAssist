src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"

function showHideQuestions() {
    var gender = document.querySelector('select[name="gender"]').value;
    var femaleQuestions = document.getElementById('femaleQuestions');
    var maleQuestions = document.getElementById('maleQuestions');

    femaleQuestions.style.display = 'none';
    maleQuestions.style.display = 'none';

    if (gender === 'female' || gender === 'other' || gender === 'prefer_not_to_say') {
        femaleQuestions.style.display = 'block';
    } else if (gender === 'male') {
        maleQuestions.style.display = 'block';
    }
}

function validateForm(event) {
    // event.preventDefault(); // Prevent the form from submitting
    
    // Retrieve form data
    var weight = document.getElementById('weight').value;
    var dob = document.getElementById('dob').value;
    var today = new Date();
    var birthDate = new Date(dob);
    var age = today.getFullYear() - birthDate.getFullYear();
    var m = today.getMonth() - birthDate.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }
    // Checking all 'yes' answers
    var yesAnswers = document.querySelectorAll('input[type="radio"][value="yes"]:checked').length;

    if (weight < 50 || age < 18 || age > 66 || yesAnswers > 0) {
        document.getElementById("donationForm").action = 'http://127.0.0.1:5000/ineligible';
        window.location.href = 'http://127.0.0.1:5000/ineligible'; // Redirect to the ineligible page route
    } else {
        document.getElementById("donationForm").action = 'http://127.0.0.1:5000/eligible';
        window.location.href = 'http://127.0.0.1:5000/eligible'; // Redirect to the eligible page route
    }
}

window.onload = function(event) {
    event.preventDefault(); // Prevent the form from submitting via the browser
    document.getElementById('donationForm').onsubmit = validateForm;
};
