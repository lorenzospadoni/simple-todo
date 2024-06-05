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
                this.handleCheckboxChange(event.target.checked);
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
        this.paragraph.onblur = () => { todo_arrow.saveToLocalStorage() }
    }
    addEventListeners() {
        this.oncontextmenu = () => { this.editContent() }
    }
    handleCheckboxChange(isChecked) {
        if (isChecked) {
            this.classList.add('item-fade-out');
            this.addEventListener('animationend', () => {
                this.remove();
                todo_arrow.saveToLocalStorage();
            });
        }
    }
    get obj() {
        return {
            'content' : this.paragraph.textContent,
        }
    }
    set obj( object_arg ) {
        this.paragraph.textContent = object_arg.content;
    }
}

customElements.define('todo-item', TodoItem);
