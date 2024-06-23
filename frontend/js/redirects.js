function removeSlash( domain ) {
    let last_char = domain[domain.length]
    if (last_char === '/') {
        domain = domain.substring(0, domain.length - 1);
    }
    return domain;
}
export function redirectTodo( domain ) {
    domain = removeSlash(domain);
    const url = domain + '/frontend/todo.html';
    window.location.href = url;
}

export function redirectIndex( domain ) {
    domain = removeSlash(domain);
    const url = domain + '/frontend/index.html';
    window.location.href = url;
}

export function redirectLogin( domain ) {
    domain = removeSlash(domain);
    const url = domain + '/frontend/login.html';
    window.location.href = url;
}

export function redirectLogout( domain ) {
    domain = removeSlash(domain);
    const url = domain + '/frontend/logout.html';
    window.location.href = url;
}

export function redirectProfile( domain ) {
    domain = removeSlash(domain);
    const url = domain + '/frontend/';
    window.location.href = url;
}
