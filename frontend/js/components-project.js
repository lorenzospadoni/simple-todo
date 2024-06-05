class TodoProject extends HTMLElement {
    static observedAttributes = ["title", "state"];
    constructor() {
        super();
        this.tags_appended = false;

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

        if (this.tags_appended === false) {
            console.log('[project] is equal to false')
            let tags = this.innerHTML;
            this.innerHTML = ""; 
            this.item_box.innerHTML = tags;
            this.tags_appended = true;
        } else if (this.tags_appended === true) {
            console.log('[project] tags_appended is equal to true')
            console.log('[project] tags_appended nothing to do')
        } else {
            throw new Error('[project] tags_appended has a value different from true/false: ' + this.tags_appended)
        }
 // TODO: implement a setter for this

        // item box is shared between the two states
        // this way I don't need to clone nodes and worry
        // about keeping them synced up

        this.appendChild(this.title_box);
        this.appendChild(this.item_box);
        this.appendChild(this.new_button);
        this.appendChild(this.info_box);

        this.title_box.classList.add('title');
        this.item_box.classList.add('items');
        this.info_box.classList.add('info_box');

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
            console.log('[PROJECT] attribute ' + name + ' changed from ' + oldValue + ' to ' + newValue)
            if ( newValue === 'open' ) {
                // destroyDraggable();
                // initDraggable();
                this.title_box.contentEditable = true;
                this.setStyleOpen();
                console.log('open')
            } else if (newValue === 'closed') {
                // destroyDraggable();
                this.title_box.contentEditable = false;
                this.setStyleClosed();
                console.log('closed');
            } else if (newValue === 'hidden') {
                // destroyDraggable();
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
    set title(new_title) {
        this.title_box.innerContent = new_title;
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
