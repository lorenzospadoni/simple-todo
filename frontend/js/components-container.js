class TodoContainer extends HTMLElement {

    static observedAttributes = ['state'];

    constructor() {
        super();
        this.tags_appended = false;

        this.title_box = document.createElement('h1');
        this.project_box = document.createElement('div');
        this.new_button = document.createElement('button');

    }

    connectedCallback()   {       
        if (this.tags_appended === false) {
            console.log('[container] tags_appended is equal to false')
            let tags = this.innerHTML;
            this.innerHTML = ""; 
            this.project_box.innerHTML = tags;
        } else if (this.tags_appended === true) {
            console.log('[container] tags_appended is equal to true')
            console.log('[container] nothing to do')
        } else {
            throw new Error('[container] tags_appended has a value different from true/false: ' + this.tags_appended)
        }

        this.title_box.innerText = "Your Projects";
        this.new_button.innerText = 'Create a new project';
    
        this.appendChild(this.title_box);
        this.appendChild(this.project_box);
        this.appendChild(this.new_button);

        this.setDoubleClick();

        if (this.attributes['state'] == null) {
            this.setAttribute('state', 'overview')
        }
    }

    disconnectedCallback() {

    }
    attributeChangedCallback(name, oldValue, newValue) {
        console.log('attribute ' + name + ' changed from ' + oldValue + ' to ' + newValue);
        if (name === 'state') {
            if (newValue === 'overview') {
                this.classList.add('container-overview');
                this.classList.remove('container-single');
            } else if (newValue === 'single') {
                this.classList.add('container-single');
                this.classList.remove('container-overview');
            } 
        }
    }
    setDoubleClick() {
        let children = Array.prototype.slice.call(this.project_box.children);
        children.forEach( ( child ) => {
            child.ondblclick = () => { this.openProject( child ); }
        });
    }
    openProject( elem ) {
        let children = Array.prototype.slice.call(this.project_box.children);
        children.forEach( ( child ) => {
            child.setStyleHidden();
        });
        elem.setAttribute('state', 'open');
        // elem.setStyleOpen();

        // remove this in favor of a better global state-based system
        this.title_box.style.display = 'none';
        this.new_button.style.display = 'none';

    }
    newChild() {
        let new_child = document.createElement('todo-project');
        new_child.setAttribute('state', 'closed');
        this.project_box.appendChild(new_child);
        this.setDoubleClick();
        return new_child;
    }
    set obj(container_object) {
        container_object.forEach((project) => {
            let returned_element = this.newChild();
            returned_element.obj = project;
        })
    }


}

customElements.define('todo-container', TodoContainer);