
function removeSlash( domain ) {
    let last_char = domain[domain.length]
    if (last_char === '/') {
        domain = domain.substring(0, domain.length - 1);
    }
    return domain;
}

export async function fetchProjects(domain) {
    domain = removeSlash(domain);
    const url = domain + '/todos';
    const options = {
        headers: {
            'Content-Type' : 'application/json'
        },
        method: 'GET',
        credentials: 'include'
    }
    const response = await fetch(url, options)
    const result = await response.json()
    return result
}