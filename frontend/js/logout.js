async function hasToken() {
    let url = 'http://127.0.0.1:5000/users/has_token'
    let options = {
        headers: {
            'Content-Type': 'application/json'
        },
        method: 'GET',
        credentials: 'include'
    }
    const response = await fetch(url, options)
    const result = await response.json();
    if (result.has_token === true) {
        await logout();
    } else if (result.has_token === false) {
        console.log('User has no auth token, please login');
    } else {
        console.error(result)
        throw new Error('response.has_token is neither True nor false');
    }
}

async function logout() {
    console.log('logout()');
    const url = 'http://127.0.0.1:5000/users/logout';
    const options = {
        headers: {
            'Content-Type' : 'application/json'
        },
        method: 'POST',
        credentials: 'include'
    }
    const response = await fetch(url, options);
    const result = await response.json()
    if (result.success === true) {
        console.log('logout successful')
        window.location.href = 'http://127.0.0.1:3000/frontend/login.html';
    } else {
        console.log('Unspecified logout result');
    }
}

hasToken()

