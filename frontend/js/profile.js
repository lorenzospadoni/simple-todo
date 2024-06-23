import { hasToken, getUserData } from './users.js'

const username_field = document.getElementById('username_field');
const date_field = document.getElementById('date_field');
const notodos = document.getElementById('notodos');

async function updateUserFields() {
    let response = await getUserData();
    username_field.innerText = response.username;
    date_field.innerText = response.date_of_subscription;
}

let result = hasToken()
result.then((output) => {console.log(output.username)})
updateUserFields();