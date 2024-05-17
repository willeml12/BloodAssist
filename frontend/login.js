src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"


/**
 * Login check if the combination user-password exists in our database
 */
window.onload = function(){
document.getElementById('login-button').addEventListener('click',function(event){
    event.preventDefault(); // Prevent the form from submitting via the browser

      var email = document.getElementById('user-email').value;
      var password = document.getElementById('password').value;
      if (email === '' || password === '') {
        alert('Email or password missing');
        return;
      }
      axios.post('/check-login', {
        email: email,
        password: password
    })
    .then(function(response){
      if(response.data['success']){
        alert('Successfully logged in');
        //TODO : redirect on a pre-completed question sheet (with modification possibilities)
        window.location.href = "http://127.0.0.1:5000/questions";
      } else {
        alert('Invalid email or password');
      }
    })
    .catch(function(error){
      alert("Error in login request");
    });
    });
};
    
function showPassword() {
    var x = document.getElementById("password");
    if (x.type === "password") {
    x.type = "text";
    } else {
    x.type = "password";
    }
};