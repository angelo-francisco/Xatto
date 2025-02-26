const usernameInput = document.getElementById('username');

usernameInput.addEventListener('input', (event) => {
    usernameInput.value = event.target.value.replace(' ', '');
});