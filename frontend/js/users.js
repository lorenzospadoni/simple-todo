import { BACKEND, FRONTEND } from './vars.js';

function removeSlash( domain ) {
    let last_char = domain[domain.length]
    if (last_char === '/') {
        domain = domain.substring(0, domain.length - 1);
    }
    return domain;
}

export async function hasToken( domain ) {
    domain = removeSlash(domain);
    const url = domain + '/users/has_token'
    const options = {
        headers: {
            'Content-Type': 'application/json'
        },
        method: 'GET',
        credentials: 'include'
    }
    const response = await fetch(url, options)
    const result = await response.json()
    return result
    
}

export async function getUserData( domain ) {
    domain = removeSlash(domain);
    const url = domain + '/users/current_user/data';
    console.log(url);
    const options = {
        method: 'GET',
        credentials: 'include'
    }
    let response = await fetch(url, options);
    let result = await response.json();
    return result;
}

export async function loginUser(username, password, domain){
    domain = removeSlash(domain);
    const data = {
        'username' : username,
        'password' : password
    }
    const url = domain + '/users/login';
    const options = {
        method : 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }
    const response = await fetch(url, options)
    const result = await response.json();
    return result;
}

export async function logoutUser( domain = BACKEND ) {
    domain = removeSlash( domain );
    const url = domain + '/users/logout'
    const options = {
        headers: {
            'Content-Type' : 'application/json'
        },
        method: 'POST',
        credentials: 'include'
    }
    const response = await fetch(url, options);
    const result = await response.json()
    return result;
}
