class TodoItem extends HTMLElement {
    constructor() {
        super();

        this.label = document.createElement("span");
        this.checkbox = document.createElement("button");

    }

    connectedCallback() {
        console.log('TodoItem added to document.');
        let text_content = this.textContent;
        this.textContent = "";
        this.label.textContent = text_content;

        this.appendChild(this.checkbox);
        this.appendChild(this.label);


        this.label.classList.add("todo-label");
        this.checkbox.classList.add('checkbox');
        this.checkbox.classList.add('checkbox-not-checked');
        this.classList.add("list_item");

        this.checkbox.onmouseover = () => {
            if (is_dragging === false) {
                destroyDraggable();
            }
        };

        this.checkbox.onmouseout = () => {
            if (is_dragging === false) {
                initDraggable();
            }
        };

        this.checkbox.onclick = (event) => {
            event.stopPropagation();
            this.checkbox.classList.remove('checkbox-not-checked');
            this.checkbox.classList.add('checkbox-checked');
            this.classList.add('item-fade-out')

        };

        this.label.onmouseover = () => {
            if (is_dragging === false) {
                destroyDraggable();
            }
        };

        this.label.onmouseout = () => {
            if (is_dragging === false) {
                initDraggable();
            }
        };

        this.label.onclick = (event) => {
            event.preventDefault();
            event.stopPropagation();
            this.editContent();
        };

        this.checkbox.addEventListener('click', (event) => {
            if (event.target.type === 'checkbox') {
                this.handleCheckboxChange(event.target.checked);
                event.stopPropagation();
            }
        });

        this.label.addEventListener('click', (event) => {
            if (event.target !== this.checkbox) {
                event.preventDefault();
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
        this.label.contentEditable = true;
        this.label.focus();
        this.label.onblur = () => { STATE_MANAGER.saveToLocalStorage() }
    }
    addEventListeners() {
        this.oncontextmenu = () => { this.editContent() }
        this.addEventListener('animationend', () => {
            this.remove();
            STATE_MANAGER.saveToLocalStorage();
        });
    }
    handleCheckboxChange(isChecked) {
        if (isChecked) {
            this.classList.add('item-fade-out');
            this.addEventListener('animationend', () => {
                this.remove();
                STATE_MANAGER.saveToLocalStorage();
            });
        }
    }
    get obj() {
        return {
            'content' : this.label.textContent,
        }
    }
    set obj( object_arg ) {
        this.label.textContent = object_arg.content;
    }
}

customElements.define('todo-item', TodoItem);
