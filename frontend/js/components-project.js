class TodoProject extends HTMLElement {
    static observedAttributes = ["title", "state"];
    constructor() {
        super();
        this.title_box = document.createElement('h2'); // tie this to a title attribute in the tag
        this.item_box = document.createElement('div');
        this.new_button = document.createElement('button');
        this.info_box = document.createElement('div'); // this will contain how many items are left from item box

        this.new_button.textContent = '+';
        this.new_button.onclick = () => {
            this.newChild()
        }


    }
    connectedCallback() {
        console.log('TodoProject added to document');

        let tags = this.innerHTML;
        this.innerHTML = ""; 
        this.item_box.innerHTML = tags; // TODO: implement a setter for this

        // item box is shared between the two states
        // this way I don't need to clone nodes and worry
        // about keeping them synced up

        this.appendChild(this.title_box);
        this.appendChild(this.item_box);
        this.appendChild(this.new_button);
        this.appendChild(this.info_box);

        this.title_box.classList.add('title');
        this.item_box.classList.add('items')
        this.info_box.classList.add('info_box')
        
        initDraggable();
    }
    disconnectedCallback() {
        console.log('TodoProject remove from document');
        destroyDraggable();
    }
    newChild() {
        let el = document.createElement( 'todo-item' ); 
        this.item_box.appendChild( el ); 
        el.editContent();
        return el;
    }
    attributeChangedCallback(name, oldValue, newValue) {
        if ( name === "state" ) {
            if ( newValue === 'open' ) {
                this.setStyleOpen();
                console.log('open')
            } else if (newValue === 'closed') {
                this.setStyleClosed();
                console.log('closed');
            } else if (newValue === 'hidden') {
                this.setStyleHidden();
                console.log('hidden');
            }
        } else if (name === 'title') {
            this.title_box.textContent = newValue;
        }
    }
    get obj() {
        let items = [];
        let items_html = Array.prototype.slice.call( this.item_box.children );
        items_html.forEach( (item) => {
            items.push( item.obj );
        })
        return {
            'title' : this.title_box.textContent,
            'children' : items
        }
    }
    set obj( object_arg ) {
        this.title_box.textContent = object_arg.title;
        object_arg.children.forEach( ( child_obj ) => {
            let child_html = this.newChild();
            child_html.obj =  child_obj ;
        });
    }
    setStyleOpen() {
        this.classList.add('project-open');
        this.classList.remove('project-closed');
        this.classList.remove('project-hidden');
    }
    setStyleClosed() {
        this.classList.remove('project-open');
        this.classList.add('project-closed');
        this.classList.remove('project-hidden');
    }
    setStyleHidden() {
        this.classList.remove('project-open');
        this.classList.remove('project-closed');
        this.classList.add('project-hidden');
    }
    moveChildren(el0, el1) {
        for (let i = 0; 0 > el0.children.length; i++) {
            let current_element = el0.children[i];
            el1.appendChild( current_element );
        }
        return;
    }
}
customElements.define('todo-project', TodoProject);
