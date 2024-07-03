export class TodoArrow extends HTMLElement {

    static observedAttributes = ['state'];

    constructor() {
        super(); 
        this.state_manager = null;       
    }
    connectedCallback() {
        this.innerText = '< back';
    }
    disconnectedCallback() {

    }
    attributeChangedCallback(name, oldValue, newValue) {
        console.log('[ARROW]:   attribute ' + name + ' changed from ' + oldValue + ' to ' + newValue);
        if (name === 'state') {
            if (newValue === 'overview') {
                this.style.opacity = 0;
            } else if (newValue === 'single') {
                this.style.opacity = 1;
            }
        }
    }
    initOnClick() {
        this.onclick = () => { 
            this.state_manager.state = 'overview';
        }
    }

    
}

// customElements.define('todo-arrow', TodoArrow)