let draggable = null;
let is_dragging = false;
let list_items = document.querySelectorAll("todo-item");
// const list_container = document.querySelector('todo-container > div');

function initDraggable() {
    let list_container = document.querySelector('todo-container > div');
    draggable = new Draggable.Sortable(( list_container ), {
        draggable : 'todo-item',
        mirror: {
            constrainDimensions: true,
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
    
    draggable.on('sortable:sorted', (evt) => {
        console.log('sortable:sorted')
    })
    draggable.on('sortable:start', ( evt ) => {
        console.log('sortable:start', evt);
        is_dragging = true;
    })
    
    draggable.on('sortable:move', (evt) => {
        console.log('sortable:move', evt);
    });
    
    draggable.on('sortable:stop', (evt) => {
        console.log('sortable:stop', evt);
        is_dragging = false;
    });
}
function destroyDraggable() {
    if (draggable) {
        // Remove all event listeners
        draggable.off('sortable:sorted');
        draggable.off('sortable:start');
        draggable.off('sortable:move');
        draggable.off('sortable:stop');

        // Clean up any draggable-specific attributes or styles (if necessary)
        document.querySelectorAll('todo-item').forEach(item => {
            item.removeAttribute('draggable');
            item.classList.remove('is-dragging', 'is-mirror');
        });

        // Destroy the draggable instance
        draggable.destroy();
        draggable = null;
    }
}

class TodoItem extends HTMLElement {
    // static observedAttributes = 
    constructor() {
        super();

        this.label = document.createElement("label");
        this.checkbox = document.createElement("input");
        this.checkbox_styled = document.createElement('span')
        this.paragraph = document.createElement("span");
    }

    
    connectedCallback() {
        console.log( 'TodoItem added to document.' );
        let text_content = this.textContent;
        this.textContent = "";
        this.paragraph.textContent = text_content;
        this.checkbox.type = "checkbox";

        this.appendChild(this.label);
        this.label.appendChild(this.checkbox);
        this.label.appendChild(this.checkbox_styled);
        this.label.appendChild(this.paragraph);


        this.label.classList.add("todo-label")
        this.checkbox_styled.classList.add('checkbox');
        this.classList.add(".list_item")

        this.checkbox_styled.onmouseover = () => {
            if (is_dragging === false) {
                destroyDraggable()
            }}
        this.checkbox_styled.onmouseout = () => {
            {
                if (is_dragging === false) {
                    initDraggable()
                }}
        }
        this.checkbox_styled.onclick = () => {console.log("ciaoo")}

        this.paragraph.onmouseover = () => {
            {
                if (is_dragging === false) {
                    destroyDraggable()
                }}
        }
            
        this.paragraph.onmouseout = () => {
            {
                if (is_dragging === false) {
                    initDraggable()
                }}
        }
        this.paragraph.onclick = () =>{ this.editContent() }

        this.checkbox.addEventListener('click', (event) => {
            if (event.target.type === 'checkbox') {
                event.stopPropagation();
            }
        })
        this.addEventListener('click', (event) => {
            if (event.target.tagName === 'TODO-ITEM') {
                event.stopPropagation();
            }
        });
    

        this.addEventListeners();

    }
    disconnectedCallback() {
        console.log('TodoItem removed from document');
    }
    attributeChangedCallback( name ) {
        console.log(`Attribute ${name} has changed.`);
    }
    editContent() {
        this.paragraph.contentEditable = true;
        this.paragraph.focus();
    }
    addEventListeners() {
        this.oncontextmenu = () => { this.editContent() }
    }
    get obj() {
        return {
            'content' : this.paragraph.textContent,
            'checked' : this.checkbox.checked
        }
    }
    set obj( object_arg ) {
        this.paragraph.textContent = object_arg.content;
        this.checkbox.checked = object_arg.checked; 
    }
}

class TodoContainer extends HTMLElement {
    static observedAttributes = ["title", "state"];
    constructor() {
        super();
        this.open_title_box = document.createElement('h1'); // tie this to a title attribute in the tag
        this.item_box = document.createElement('div');
        this.open_new_button = document.createElement('button');

        this.closed_title_box = document.createElement('h2');
        this.closed_info_box = document.createElement('div'); // this will contain how many items are left from item box

        this.open_new_button.textContent = '+';
        this.open_new_button.onclick = () => {
            this.newChild()
        }


    }
    connectedCallback() {
        console.log('TodoContainer added to document');
        let tags = this.innerHTML;
        this.innerHTML = ""; 
        this.item_box = tags; // TODO: implement a setter for this

        this.appendChild(this.open_title_box);
        this.appendChild(this.closed_title_box);

        // item box is shared between the two states
        // this way I don't need to clone nodes and worry
        // about keeping them synced up

        this.appendChild(this.item_box);

        this.appendChild(this.open_new_button);
        this.appendChild(this.closed_info_box);
        initDraggable();
    }
    disconnectedCallback() {
        console.log('TodoContainer remove from document');
        destroyDraggable();
    }
    newChild() {
        let el = document.createElement('todo-item'); 
        this.appendTagToItemBox(el); 
        el.editContent();
        return el;
    }
    attributeChangedCallback(name, oldValue, newValue) {
        if ( name === "state" ) {
            if ( newValue === 'open' ) {
                this.closedHide();
                this.openShow();
                console.log('open')
            } else if (newValue === 'closed') {
                this.openHide();
                this.closedShow();
                console.log('closed');
            } else if (newValue === 'hidden') {
                this.closedHide();
                this.openHide();
                console.log('hidden');
            }
        } else if (name === 'title') {
            this.title_box = newValue;
        }
    }
    get obj() {
        let items = [];
        let items_html = Array.prototype.slice.call( this.open_item_box.children );
        items_html.forEach( (item) => {
            items.push( item.obj );
        })
        return {
            'title' : this.title_box,
            'children' : items
        }
    }
    set obj( object_arg ) {
        this.title_box = object_arg.title;
        object_arg.children.forEach( ( child_obj ) => {
            let child_html = this.newChild();
            child_html.obj =  child_obj ;
        });
    }
    openHide() {
        this.open_title_box.style.display = 'none';
        this.open_item_box.style.display = 'none';
        this.open_new_button.style.display = 'none';
    }
    openShow() {
        this.open_title_box.style.display = 'initial';
        this.open_item_box.style.display = 'initial';
        this.open_new_button.style.display = 'initial';
    }
    closedHide() {
        this.closed_title_box.style.display = 'none';
        this.closed_item_box.style.display = 'none';
        this.closed_info_box.style.display = 'none';
    }
    closedShow() {
        this.closed_title_box.style.display = 'initial';
        this.closed_item_box.style.display = 'initial';
        this.closed_info_box.style.display = 'initial';
    }
}


customElements.define('todo-item', TodoItem);
customElements.define('todo-container', TodoContainer);
