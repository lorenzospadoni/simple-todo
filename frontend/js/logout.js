import { hasToken, logoutUser } from './users.js';
import {redirectLogin } from './redirects.js'

const FRONTEND = 'http://127.0.0.1:3000';
const BACKEND = 'http://127.0.0.1:5000';

let token_response = hasToken( BACKEND );
token_response.then((result) => {
    if (result.has_token === true) {
        let logout_response = logoutUser( BACKEND )
        logout_response.then((logout_result) => {
            redirectLogin(FRONTEND)
        })
    } else if (result.has_token === false) {
        let message = document.createElement('h1');
        message.textContent = 'user is already logged out';
        document.body.appendChild(message);
        setTimeout(() => {redirectLogin(FRONTEND)}, 5000)

    }
})


