class TodoItem extends HTMLElement {
    // static observedAttributes = 
    constructor() {
        super();

        this.label = document.createElement("label");
        this.checkbox = document.createElement("input");
        this.paragraph = document.createElement("span");

        this.mutationHandler = null;
        this.observer = null;

    }

    addMutationObservers() {
        // I found this in the HTML specifications on 
        //  whatwg.org, I don't really know what that site is
        // but it was linked on MDN so they must be some  specification big shots
        // btw the documentations were some of the 
        // driest I've ever seen it felt like shitting rocks
        // TODO:
        // -FOR THE LOVE OF GOD TEST THIS I DON'T KNOW WHAT
        //  I'M DOING
        this.mutationHandler = (mutationsList, observer) => {
            for (let mutation of mutationsList) {
                if (mutation.type === 'childList' || mutation.type === 'characterData'  || mutation.type === 'subtree' ) {
                    console.log('mutationObserver thriggered')
                    this.paragraph.textContent = this.textContent;
                }
            }
        }

        this.observer = new MutationObserver(this.mutationHandler)
        // subtree is necessary for triggering the observer when 
        // I change content from firefox dev tools
        // don't really know why
        this.observer.observe( this, 
            { childList: true,
                characterData: true, 
                subtree: true
            });
    }

    connectedCallback() {
        console.log( 'TodoItem added to document.' );
        this.checkbox.type = "checkbox";

        this.root.appendChild(this.label);
        this.label.appendChild(this.checkbox);
        this.label.appendChild(this.paragraph);


        this.paragraph.textContent = this.textContent;
        // this.addMutationObservers();

    }
    disconnectedCallback() {
        console.log('TodoItem removed from document');
        this.observer.disconnect();
    }
    attributeChangedCallback( name ) {
        console.log(`Attribute ${name} has changed.`);
    }
    

}

class TodoContainer extends HTMLElement {
    constructor() {
        super();
    }
    connectedCallback() {
        console.log('TodoContainer added to document')
    }
    disconnectedCallback() {
        console.log('TodoContainer remove from document')
    }
}

customElements.define('todo-item', TodoItem)