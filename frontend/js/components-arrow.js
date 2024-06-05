class TodoArrow extends HTMLElement {

    static observedAttributes = ['state'];

    constructor() {
        super();
        this.container = null;
    }
    connectedCallback() {
        this.innerText = '<';
        this.onclick = () => { 
            this.container.setAttribute('state', 'overview');
            this.setAttribute('state', 'overview')
        }
        if (this.attributes['state'] === 'overview') {
            this.style.opacity = 0;
        } else if (this.attributes['state'] == null) {
            this.setAttribute('state', 'overview')
        } else {
            console.log('weird');
        }
    }
    disconnectedCallback() {

    }
    attributeChangedCallback(name, oldValue, newValue) {
        console.log('[ARROW]:   attribute ' + name + ' changed from ' + oldValue + ' to ' + newValue);
        if (name === 'state') {
            if (newValue === 'overview') {
                this.style.opacity = 0;
                this.container.setAttribute('state', 'overview');
            } else if (newValue === 'single') {
                this.style.opacity = 1;
                this.container.setAttribute('state', 'single');
            }
        }
    }
    saveToLocalStorage() {
        let container_data = this.container.json;
        localStorage.setItem('data', container_data);
    }
    getFromLocalStorage() {
        let data = localStorage.getItem('data');
        this.container.json = data;
    }
    
}

customElements.define('todo-arrow', TodoArrow)