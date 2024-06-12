class ProjectMenu extends HTMLElement {
    static observedAttributes = ['state'];

    constructor() {
        super();
        this.project_element = null;
        this.container_element = null;

        this.edit_button = document.createElement('button');
        this.delete_button = document.createElement('button');

        this.edit_button.classList.add('edit');
        this.delete_button.classList.add('delete');
    }
    connectedCallback() {
        this.appendChild(this.edit_button);
        this.appendChild(this.delete_button);

        this.edit_button.innerText = 'Edit';
        this.delete_button.innerText = 'Delete';

    }
    disconnectedCallback() {

    }
    attributeChangedCallback(name, oldValue, newValue) {
        if (name === 'state') {
            if (newValue === 'open') {
                this.style.display = 'block';
            } else if (newValue === 'closed') {
                this.style.display = 'none';
            } else {
                this.setAttribute('state', 'closed');
            }
        }
    }
    toggleState() {
        const currentState = this.getAttribute('state');
        console.log('PROJECT MENU STATE IS ->', currentState);
    
        if (currentState === 'open') {
            console.log('Closing menu');
            this.setAttribute('state', 'closed');
        } else if (currentState === 'closed') {
            console.log('Opening menu');
            this.setAttribute('state', 'open');
        }
    }
}

customElements.define('project-menu', ProjectMenu);