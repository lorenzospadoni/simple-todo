export async function hasToken() {
    const url = 'http://127.0.0.1:5000/users/has_token'
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

export async function getUserData() {
    const url = 'http://127.0.0.1:5000/users/current_user/data';
    const options = {
        method: 'GET',
        credentials: 'include'
    }
    let response = await fetch(url, options);
    let result = await response.json();
    return result;
}
