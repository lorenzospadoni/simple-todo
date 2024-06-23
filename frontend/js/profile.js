import { hasToken, getUserData } from './users.js'

const username_field = document.getElementById('username_field');
const date_field = document.getElementById('date_field');
const notodos = document.getElementById('notodos');

async function updateUserFields() {
    let response = await getUserData();
    if (response.logged_in === true){
        username_field.innerText = response.username;
        date_field.innerText = response.date_of_subscription;
    } else {
        window.location.href = 'http://127.0.0.1:3000/frontend/login.html';
    }

}

let result = hasToken()
result.then((output) => {console.log(output.username)})
updateUserFields();