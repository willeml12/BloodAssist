src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"

window.onload = function() {
    document.getElementById('register-button').addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the form from submitting via the browser

        var firstName = document.getElementById('first-name').value;
        var lastName = document.getElementById('last-name').value;
        var dob = document.getElementById('dob').value;
        var email = document.getElementById('register-email').value;
        var bloodType = document.getElementById('blood-type').value;
        var password = document.getElementById('register-password').value;
        var confirmPassword = document.getElementById('confirm-password').value;
        console.log("Response btype : %s",bloodType);

        if (password !== confirmPassword) {
            displayError('Passwords do not match!');
            return;
        }
        var today = new Date();
        var birthDate = new Date(dob);
        var age = today.getFullYear() - birthDate.getFullYear();
        var m = today.getMonth() - birthDate.getMonth();
        if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
            age--;
        }

        if (age < 18 ) {
            displayError("You are too young, come back when you are 18!");
            return;

    }

        axios.post('/register_user', {
            firstName: firstName,
            lastName: lastName,
            dob: dob,
            email: email,
            bloodType: bloodType,
            password: password
        })
        .then(function(response) {
            //alert('Registration successful!');
            // Redirect the user to eligibility test
            goToQuestions();
            //clearForm();
        })
        .catch(function(error) {
            displayError('Registration failed: ' + (error.response.data.error || 'Unknown error'));
            console.error('Registration error:', error);
        });
    });

    function displayError(message) {
        var errorMessageDiv = document.getElementById('error-message');
        errorMessageDiv.textContent = message;
        errorMessageDiv.style.display = 'block';
    }

    function goToQuestions(){
        window.location.href = "http://127.0.0.1:5000/questions";
    }

    function clearForm() {
        document.getElementById('first-name').value = '';
        document.getElementById('last-name').value = '';
        document.getElementById('dob').value = '';
        document.getElementById('register-email').value = '';
        document.getElementById('blood-type').selectedIndex = 0;
        document.getElementById('register-password').value = '';
        document.getElementById('confirm-password').value = '';
        document.getElementById('error-message').style.display = 'none';
    }
};