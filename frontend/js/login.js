import { loginUser, hasToken } from './users.js';
import { redirectTodo } from './redirects.js';

const FRONTEND = 'http://127.0.0.1:3000';
const BACKEND = 'http://127.0.0.1:5000';

const username_field = document.getElementById('username-field');
const password_field = document.getElementById('password-field');
const submit_button = document.getElementById('submit-button');
const login_form = document.getElementById('login-form');

async function submitForm(){
    let response = loginUser(username_field.value, password_field.value, BACKEND)
    response.then((result) => {
        if (result.login_successful === true) {
            // you could send a message on screen and then set a timeout for a redirect
            redirectTodo(FRONTEND);
        } else if (result.login_successfull === false) {
            password_field.value = '';
            console.log('login failed');
        }
    })
}

login_form.addEventListener('submit', (evt) => {evt.preventDefault(); submitForm();}, true);
let response = hasToken( BACKEND )
response.then((result) => {
    if (result.has_token === true) {
        redirectTodo(FRONTEND);
    }
})


