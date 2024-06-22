const username_field = document.getElementById('username-field');
const password_field = document.getElementById('password-field');
const submit_button = document.getElementById('submit-button');
const login_form = document.getElementById('login-form');

async function submitForm(){
    const data = {
        'username' : username_field.value,
        'password' : password_field.value
    }
    const url = 'http://127.0.0.1:5000/users/login';
    const options = {
        method : 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }
    try {
        const response = await fetch(url, options);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json();
        if (result.login_successful === true) {
            window.location.href = 'http://127.0.0.1:3000/frontend/todo.html';
        }
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

async function hasToken() {
    const url = 'http://127.0.0.1:5000/users/has_token'
    const options = {
        headers: {
            'Content-Type': 'application/json'
        },
        method: 'GET',
        credentials: 'include'
    }
    const response = await fetch(url, options)
    const result = await response.json();
    if (result.has_token === true) {
        window.location.href = 'http://127.0.0.1:3000/frontend/todo.html';
    } else if (result.has_token === false) {
        console.log('User has no auth token, please login')
    } else {
        console.error(result)
        throw new Error('response.has_token is neither True nor false')
    }
}


login_form.addEventListener('submit', (evt) => {evt.preventDefault(); submitForm();}, true);
hasToken()


