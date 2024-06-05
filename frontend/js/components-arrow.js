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
                this.container.title_box.style.display = 'initial';
                this.container.new_button.style.display = 'initial';
                this.style.opacity = 0;
            } else if (newValue === 'single') {
                this.container.title_box.style.display = 'none';
                this.container.new_button.style.display = 'none';
                this.style.opacity = 1;
            }
        }
    }
    
}

customElements.define('todo-arrow', TodoArrow)