class TodoContainer extends HTMLElement {

    static observedAttributes = ['state'];

    constructor() {
        super();
        this.tags_appended = false;

        this.title_box = document.createElement('h2');
        this.item_box = document.createElement('div');
        this.new_button = document.createElement('button');

        this.new_button.onclick = () => { this.newChild() }

        this._draggable = null;
    }

    connectedCallback()   {       
        if (this.tags_appended === false) {
            console.log('[container] tags_appended is equal to false')
            let tags = this.innerHTML;
            this.innerHTML = ""; 
            this.item_box.innerHTML = tags;
        } else if (this.tags_appended === true) {
            console.log('[container] tags_appended is equal to true')
            console.log('[container] nothing to do')
        } else {
            throw new Error('[container] tags_appended has a value different from true/false: ' + this.tags_appended)
        }

        this.title_box.innerText = "Your Projects";
        this.new_button.innerText = 'Create a new project';
    
        this.appendChild(this.title_box);
        this.appendChild(this.item_box);
        this.appendChild(this.new_button);

        this.setDoubleClick();

        if (this.attributes['state'] == null) {
            this.setAttribute('state', 'overview')
        }
    }

    disconnectedCallback() {

    }
    attributeChangedCallback(name, oldValue, newValue) {
        console.log('[CONTAINER]:   attribute ' + name + ' changed from ' + oldValue + ' to ' + newValue);
        if (name === 'state') {
            if (newValue === 'overview') {
                this.classList.add('container-overview');
                this.classList.remove('container-single');
                this.setChildrenStateOverview();

            } else if (newValue === 'single') {
                this.classList.add('container-single');
                this.classList.remove('container-overview');
            } 
        }
    }
    setDoubleClick() {
        let children = Array.prototype.slice.call(this.item_box.children);
        children.forEach( ( child ) => {
            child.ondblclick = () => { 
                this.openProject( child );
                STATE_MANAGER.state = 'single';
            }
        });
    }
    setChildrenStateOverview() {
        let children = Array.prototype.slice.call(this.item_box.children);
        children.forEach( ( child ) => {
            child.setAttribute('state', 'closed');
        });
    }
    openProject( elem ) {
        let children = Array.prototype.slice.call(this.item_box.children);
        children.forEach( ( child ) => {
            child.setStyleHidden();
        });
        elem.setAttribute('state', 'open');
        // elem.setStyleOpen();
    }
    newChild() {
        let new_child = document.createElement('todo-project');
        new_child.setAttribute('state', 'closed');
        this.item_box.appendChild(new_child);
        this.setDoubleClick();
        new_child.title_box.contentEditable = true;
        new_child.title_box.focus();
        new_child.title_box.onblur = () => { 
            if (new_child.title_box.textContent == "") {
                new_child.remove();
                STATE_MANAGER.saveToLocalStorage();
                STATE_MANAGER.updateNavbarContent();
                STATE_MANAGER.state = 'overview';
            } else {
                try {
                    STATE_MANAGER.saveToLocalStorage();
                    STATE_MANAGER.updateNavbarContent();
                } catch (ReferenceError) {
                    console.log("[CONTAINER] caught ReferenceError: this is normal if it's happening on startup and web app runs smoothly")
                }
            }
        }

        return new_child;
    }
    initDraggable() {
        // list_container: use querySelector for a single container and querySelectorAll for multiple
        this._draggable = new Draggable.Sortable(( this.item_box ), {
            draggable : '.project-closed',
            mirror: {
                constrainDimensions: true,
                create: (originalElement) => {
                    const mirror = originalElement.cloneNode(true);
                    // Ensure the content is fully cloned
                    mirror.style.position = 'absolute';
                    mirror.style.pointerEvents = 'none';
                    document.body.appendChild(mirror);
                    return mirror;
                }
            },
            classes: {
                'source:dragging': 'is-dragging',
                'mirror': 'is-mirror',
            },
            plugins: [
                Draggable.Plugins.SortAnimation
            ],
        
            swapAnimation: {
              duration: 200,
              easingFunction: 'ease-in-out',
            },
        });
        
        this._draggable.on('sortable:sorted', ( evt ) => {
            console.log('sortable:sorted')
        })
        this._draggable.on('sortable:start', ( evt ) => {
            console.log('sortable:start', evt);
            is_dragging = true;
        })
        
        this._draggable.on('sortable:move', (evt) => {
            console.log('sortable:move', evt);
        });
        
        this._draggable.on('sortable:stop', (evt) => {
            console.log('sortable:stop', evt);
            is_dragging = false;
        });
    }
    destroyDraggable() {
        if (this._draggable) {
            // Remove all event listeners
            this._draggable.off('sortable:sorted');
            this._draggable.off('sortable:start');
            this._draggable.off('sortable:move');
            this._draggable.off('sortable:stop');
    
            // Clean up any draggable-specific attributes or styles (if necessary)
            document.querySelectorAll('todo-project').forEach(project => {
                project.removeAttribute('draggable');
                project.classList.remove('is-dragging', 'is-mirror');
            });
    
            // Destroy the draggable instance
            this._draggable.destroy();
            this._draggable = null;
        }
    }
    get item_array() {
        return Array.prototype.slice.call(this.item_box.children);
    }
    set obj(container_object) {
        container_object.forEach((project) => {
            let returned_element = this.newChild();
            returned_element.obj = project;
        })
    }
    get obj() {
        let data = [];
        let children = Array.prototype.slice.call(this.item_box.children);
        children.forEach( ( child ) => {
            data.push(child.obj);
        });
        return data;
    }
    get json() {
        return JSON.stringify(this.obj);
    }
    set json(json_data) {
        this.obj = JSON.parse(json_data);
    }


}

customElements.define('todo-container', TodoContainer);