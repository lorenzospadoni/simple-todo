export class TodoItem extends HTMLElement {
    constructor() {
        super();

        this._id = null;
        this.state_manager = null;

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
        this.label.onblur = () => {
            console.log('TodoItem onblur')
            if (this.isLabelEmpty() == true) {
                console.log('isLabelEmpty() returned true')
                this.state_manager.deleteItemOnDb(this);
                this.remove()
            } else if (this.isLabelEmpty() == false) {
                console.log('isLabelEmpty() returned false')
                this.state_manager.postItemContentChange(this) 
            }
            this.label.removeEventListener('keydown', this.blurOnEnter.bind(this));
        }
        this.label.addEventListener('keydown', this.blurOnEnter.bind(this))
    }
    blurOnEnter( event ) {
        if (event.key === 'Enter') {
            this.label.blur();
        }
    }
    isLabelEmpty() {
        const hasLettersOrNumbers = /[a-zA-Z0-9]/.test(this.label.textContent);
        return !hasLettersOrNumbers;
    }
    addEventListeners() {
        this.oncontextmenu = () => { this.editContent() }
        this.addEventListener('animationend', () => {
            this.remove();
            this.state_manager.deleteItemOnDb(this);
        });
    }
    handleCheckboxChange(isChecked) {
        if (isChecked) {
            this.classList.add('item-fade-out');
            this.addEventListener('animationend', () => {
                this.remove();
                this.state_manager.saveToLocalStorage();
            });
        }
    }
    get obj() {
        return {
            'id' : this._id,
            'content' : this.label.textContent,
        }
    }
    set obj( object_arg ) {
        this._id = object_arg.id
        this.label.textContent = object_arg.content;
    }
}

//customElements.define('todo-item', TodoItem);
