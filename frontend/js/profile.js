import { redirectLogin } from './redirects.js';
import { hasToken, getUserData } from './users.js'

const username_field = document.getElementById('username_field');
const date_field = document.getElementById('date_field');
const notodos = document.getElementById('notodos');
const FRONTEND = 'http://127.0.0.1:3000';
const BACKEND = 'http://127.0.0.1:5000';

async function updateUserFields() {
    let response = await getUserData(BACKEND);
    if (response.logged_in === true){
        username_field.innerText = response.username;
        date_field.innerText = response.date_of_subscription;
    } else {
        redirectLogin(FRONTEND)
    }

}

let result = hasToken(BACKEND)
result.then((output) => {
    if (output.has_token === false) {
        redirectLogin()
    }
})
updateUserFields();