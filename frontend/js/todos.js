
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

export async function postProject(domain) {
    domain = removeSlash(domain);
    const url = domain + '/todos/projects';
    console.log(url)
    const request = {
        operation_type : 'new_project',
    }
    const options = {
        headers: {
            'Content-Type' : 'application/json'
        },
        body: JSON.stringify(request),
        method: 'POST',
        credentials: 'include'
    }
    const response = await fetch(url, options);
    const result = response.json()
    console.log(result)
    return result;
}

export async function postProjectNewTitle(domain, id, title) {
    domain = removeSlash(domain);
    const url = domain + '/todos/projects';
    console.log(url)
    const request = {
        operation_type : 'update_title',
        project_id : id,
        new_title : title
    }
    const options = {
        headers: {
            'Content-Type' : 'application/json'
        },
        body: JSON.stringify(request),
        method: 'POST',
        credentials: 'include'
    }
    const response = await fetch(url, options);
    const result = response.json()
    console.log(result)
    return result;
}

export async function postProjects(domain, obj) {
    domain = removeSlash(domain);
    const url = domain + '/todos';
    const options = {
        headers: {
            'Content-Type' : 'application/json'
        },
        body: JSON.stringify(obj),
        method: 'POST',
        credentials: 'include'
    }
    const response = await fetch(url, options);
    const result = response.json()
    return result;
}

export async function deleteProject(domain, id) {
    domain = removeSlash(domain);
    const request = {
        project_id : id
    }
    const url = domain + '/todos/projects';
    const options = {
        headers: {
            'Content-Type' : 'application/json'
        },
        body: JSON.stringify(request),
        method: 'DELETE',
        credentials: 'include'
    }
    const response = await fetch(url, options);
    const result = response.json()
    return result;
}

export async function postItem(domain, project_id) {
    domain = removeSlash(domain);
    const url = domain + '/todos/items';
    const request = {
        operation_type : 'new_item',
        parent_project : project_id
    }
    console.log('[postItem()]   parent_project = ' + project_id)
    const options = {
        headers: {
            'Content-Type' : 'application/json'
        },
        body: JSON.stringify(request),
        method: 'POST',
        credentials: 'include' 
    }
    const response = await fetch(url, options);
    const result = response.json()
    console.log(result)
    return result;
}

export async function postItemContentChange(domain, id, content) {
    domain = removeSlash(domain);
    const url = domain + '/todos/items';
    console.log(url)
    const request = {
        operation_type : 'update_content',
        id : id,
        new_content : content
    }
    const options = {
        headers: {
            'Content-Type' : 'application/json'
        },
        body: JSON.stringify(request),
        method: 'POST',
        credentials: 'include'
    }
    const response = await fetch(url, options);
    const result = response.json()
    console.log(result)
    return result;
}

export async function deleteItem(domain, id) {
    let obj = {
        'id' : id
    }
    domain = removeSlash(domain);
    const url = domain + '/todos/items';
    const options = {
        headers: {
            'Content-Type' : 'application/json'
        },
        body: JSON.stringify(obj),
        method: 'DELETE',
        credentials: 'include'
    }
    const response = await fetch(url, options);
    const result = response.json()
    return result;
}

