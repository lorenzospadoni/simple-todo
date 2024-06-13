class TodoNavbar extends HTMLElement {
    constructor() {
        super();


    }
    connectedCallback() {

    }
    disconnectedCallback() {

    }
    attributeChangedCallback(name, oldValue, newValue) {

    }
    updateContent() {
        this.cleanContent();
        this.nav_header = document.createElement('h2');
        this.nav_header.innerText = 'Projects';
        let nav_list = document.createElement('ul');
        this.appendChild(this.nav_header);
        this.appendChild(nav_list);
        let children = this.container.item_array;
        children.forEach((child) => {
            let content = child.title_box.textContent;
            let new_li = document.createElement('li');
            new_li.textContent = content;
            nav_list.appendChild(new_li);
            new_li.onclick = () => {
                try {
                    this.container.openProject( child ); 
                    STATE_MANAGER.state = 'single'; 
                } catch (ReferenceError) {
                    this.container.openProject( child ); 
                    STATE_MANAGER.state = 'single'; }
                }})};
    cleanContent() {
        this.children_array.forEach((child) => {
            child.remove();
        });
    }

    get children_array() {
        return Array.prototype.slice.call(this.children);
    }

}

customElements.define('todo-navbar', TodoNavbar);