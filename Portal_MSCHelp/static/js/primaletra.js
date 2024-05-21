var usernameElement = document.getElementById('username');
var username = usernameElement.textContent;
usernameElement.textContent = username.charAt(0).toUpperCase() + username.slice(1);
