class TodoProject extends HTMLElement {
    static observedAttributes = ["title", "state"];
    constructor() {
        super();
        this.tags_appended = false;

        this.title_box = document.createElement('h3'); // tie this to a title attribute in the tag
        
        this.edit_box = document.createElement('div');
        this.edit_field = document.createElement('input');
        this.button_box = document.createElement('div');
        this.cancel_button = document.createElement('button');
        this.save_button = document.createElement('button');

        this.menu_button = document.createElement('button');
        this.menu_section = document.createElement('section');
        this.edit_button = document.createElement('button');
        this.delete_button = document.createElement('button');

        this.item_box = document.createElement('div');
        this.new_button = document.createElement('button');
        this.info_box = document.createElement('div'); // this will contain how many items are left from item box

        this.new_button.textContent = '+';
        this.new_button.onclick = () => {
            this.newChild()
        }



        this.cancel_button.innerText = 'Cancel';
        this.save_button.innerText = 'Save';

        this.cancel_button.classList.add('cancel');
        this.save_button.classList.add('save');

        this.save_button.onclick = () => { this.saveEditor(); }
        this.cancel_button.onclick = () => {
            this.closeEditor();
        }

        this.closeEditor();

        this.menu_button.innerText = '...'
        this.menu = document.createElement('project-menu');
        this.menu_button.onclick = () => {
            let current_state = this.menu.getAttribute('state');
            if (current_state === 'open') {
                this.closeMenu();
            } else if (current_state === 'closed') {
                this.openMenu();
            } else {
                throw new Error('[PROJECT MENU] menu state is neither closed nor open');
            }
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


        // item box is shared between the two states
        // this way I don't need to clone nodes and worry
        // about keeping them synced up

        this.appendChild(this.title_box);

        this.edit_box.classList.add('edit-project-box');
        this.appendChild(this.edit_box);
        this.edit_box.appendChild(this.edit_field);
        this.edit_box.appendChild(this.button_box);
        this.button_box.appendChild(this.cancel_button);
        this.button_box.appendChild(this.save_button);
        
        this.appendChild(this.item_box);
        this.appendChild(this.new_button);
        this.appendChild(this.info_box);
        this.appendChild(this.menu);

        this.new_button.classList.add('new-button')
        this.title_box.classList.add('title');
        this.item_box.classList.add('items');
        this.info_box.classList.add('info_box');

        this.menu_button.classList.add('menu-button');

        this.appendChild(this.menu_button);

        this.menu.setAttribute('state', 'closed')
        this.setMenuOnClicks();

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
                //this.title_box.contentEditable = true;
                this.title_box.onclick = () => { this.renderEditor() }
                this.setStyleOpen();
                console.log('open')
            } else if (newValue === 'closed') {
                // destroyDraggable();
                // this.title_box.contentEditable = false;
                this.title_box.onclick = () => {}; // disables title editor on state change
                this.setStyleClosed();
                this.closeEditor();
                console.log('closed');
            } else if (newValue === 'hidden') {
                this.title_box.onclick = () => {}; // disables title editor on state change
                // destroyDraggable();
                this.setStyleHidden();
                console.log('hidden');
            } else if (newValue === 'edit') {
                // destroyDraggable();
                this.setStyleEdit();
                console.log('edit');
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
        this.classList.remove('project-edit');

    }
    setStyleEdit() {
        this.setStyleOpen();
        this.classList.add('project-edit');
    }
    setStyleClosed() {
        this.classList.remove('project-open');
        this.classList.add('project-closed');
        this.classList.remove('project-hidden');
        this.classList.remove('project-edit');

    }
    setStyleHidden() {
        this.classList.remove('project-open');
        this.classList.remove('project-closed');
        this.classList.add('project-hidden');
        this.classList.remove('project-edit');

    }
    moveChildren(el0, el1) {
        for (let i = 0; 0 > el0.children.length; i++) {
            let current_element = el0.children[i];
            el1.appendChild( current_element );
        }
        return;
    }
    editorIsEmpty() {
        const hasLettersOrNumbers = /[a-zA-Z0-9]/.test(this.edit_field.value);
        return !hasLettersOrNumbers;
    }
    renderEditor() {
        this.title_box.style.display = 'none';
        this.edit_box.style.display = 'flex';
        this.edit_field.value = this.title_box.textContent;
        this.edit_field.addEventListener('keydown', (event) => {
            if (event.key === 'Enter') {
                this.save_button.click();
            }
        })
        this.edit_field.onkeyup = () => {
            if (this.editorIsEmpty() === true) {
                this.save_button.disabled = true;
            } else if (this.editorIsEmpty() === false) {
                this.save_button.disabled = false;
            }
        }

    }
    closeEditor() {
        this.title_box.style.display = 'block';
        this.edit_box.style.display = 'none';
    }
    saveEditor() {
        this.title_box.textContent = this.edit_field.value;
        STATE_MANAGER.saveToLocalStorage();
        STATE_MANAGER.updateNavbarContent();
        this.closeEditor();
    }
    safelyRemove() {
        this.remove();
        STATE_MANAGER.saveToLocalStorage();
        STATE_MANAGER.updateNavbarContent();
    }
    setMenuOnClicks() {
        this.menu.edit_button.onclick = () => {
            this.renderEditor();
        }
        this.menu.delete_button.onclick = () => {
            this.safelyRemove();
        }
    }
    openMenu() {
        this.menu_button.innerText = 'x';
        this.menu.setAttribute('state', 'open');
    }
    closeMenu() {
        this.menu_button.innerText = '...';
        this.menu.setAttribute('state', 'closed')
    }
}
customElements.define('todo-project', TodoProject);
