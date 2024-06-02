class OverviewContainer extends HTMLElement {
    constructor() {
        this.title_box = document.createElement('h1');
        this.item_box = document.createElement('div');
        this.new_button = document.createElement('button');


    }
    connectedCallback() {
        this.appendChild(this.title_box);
        this.appendChild(this.item_box);
        this.appendChild(this.new_button);

        this.new_button.innerText = "+";
        this.new_button.onclick = () => { this.createOverviewItem(); }

        //TODO: add a draggable callback
    }
    disconnectedCallback() {
        
    }
    attributeChangedCallback() {

    }
}
class OverviewItem extends HTMLElement {
    static observedAttributes = ["title"];

    constructor() {
        super()
        this.title_box = document.createElement("h2");
        this.children_objects = [];
    }
    connectedCallback() {
        this.appendChild(this.title_box);
    }
    disconnectedCallback() {

    }
    attributeChangedCallback(name, oldValue, newValue) {
        if ( name === "title" ) {
            this.title_box.textContent = newValue;
        }

    }
    get obj() {
        return children_objects;
    }
    set obj( object_arg ) {
        this.title_box.innerContent = object_arg.title;
        this.children_objects = object_arg.children;
        return;
    }
}

customElements.define('overview-item', OverviewItem);
customElements.define('overview-container', OverviewContainer);
