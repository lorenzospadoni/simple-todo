
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
    const url = domain + '/todos/projects/new';
    console.log(url)
    const request = {
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
    const url = domain + '/todos/projects/' + id;
    console.log(url)
    const request = {
        new_title : title
    }
    const options = {
        headers: {
            'Content-Type' : 'application/json'
        },
        body: JSON.stringify(request),
        method: 'PUT',
        credentials: 'include'
    }
    const response = await fetch(url, options);
    const result = response.json()
    console.log(result)
    return result;
}

export async function postProjectNewOrder(project_order, domain) {
    domain = removeSlash(domain);
    const url = domain + '/todos/projects/project_order';
    console.log(url)
    const request = {
        project_order: project_order
    }
    const options = {
        headers: {
            'Content-Type' : 'application/json'
        },
        body: JSON.stringify(request),
        method: 'PUT',
        credentials: 'include'
    }
    const response = await fetch(url, options);
    const result = response.json()
    console.log(result)
    return result;
}

export async function postNewItemOrder(project_id, item_order, domain) {
    domain = removeSlash(domain);
    const url = domain + '/todos/projects/' + project_id + '/item_order';
    console.log(url)
    const request = {
        operation_type : 'new_item_order',
        item_order: item_order
    }
    const options = {
        headers: {
            'Content-Type' : 'application/json'
        },
        body: JSON.stringify(request),
        method: 'PUT',
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
    }
    const url = domain + '/todos/projects/' + id;
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
    const url = domain + '/todos/items/new';
    const request = {
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
    const url = domain + '/todos/items/' + id;
    console.log(url)
    const request = {
        new_content : content
    }
    const options = {
        headers: {
            'Content-Type' : 'application/json'
        },
        body: JSON.stringify(request),
        method: 'PUT',
        credentials: 'include'
    }
    const response = await fetch(url, options);
    const result = response.json()
    console.log(result)
    return result;
}

export async function deleteItem(domain, id) {
    let obj = {
    }
    domain = removeSlash(domain);
    const url = domain + '/todos/items/' + id;
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

