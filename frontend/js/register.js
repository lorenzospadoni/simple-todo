import { registerUser, hasToken } from './users.js';
import { redirectLogin } from './redirects.js';
import { FRONTEND, BACKEND } from './vars.js'

const register_form = document.getElementById('register-form');
const username_field = document.getElementById('username');
const password_field = document.getElementById('password');


async function submitForm(){
    let response = registerUser(username_field.value, password_field.value, BACKEND)
    response.then((result) => {
        if (result.success === true) {
            // you could send a message on screen and then set a timeout for a redirect
            redirectLogin(FRONTEND);
        } else if (result.success === false) {
            password_field.value = '';
            console.log('register failed');
        }
    })
}

register_form.addEventListener('submit', (evt) => {evt.preventDefault(); submitForm();}, true);
// let response = hasToken( BACKEND )
// response.then((result) => {
//     if (result.has_token === true) {
//         redirectTodo(FRONTEND);
//     }
// })


