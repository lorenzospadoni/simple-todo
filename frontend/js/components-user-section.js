import { hasToken, getUserData } from './users.js'

class UserSection extends HTMLElement {
    static observedAttributes = ['state']
    constructor() {
        super();
        this.title_element = document.createElement('h2');
        // let usericon = document.createElement('img');
        this.user_element = document.createElement('p');
        this.date_element = document.createElement('p');
        this.username_span = document.createElement('span');
        this.date_span = document.createElement('span');
        this.settings_button = document.createElement('button');

        this.user_element.innerText = 'username: ';
        this.date_element.innerText = 'subscribed on: ';
        this.settings_button.textContent = 'settings';

        this.user_element.appendChild(this.username_span);
        this.date_element.appendChild(this.date_span);


        
    }
    connectedCallback() {
        this.title_element.textContent = 'User';
        this.appendChild(this.title_element);
        this.appendChild(this.user_element);
        this.appendChild(this.date_element);
        this.appendChild(this.settings_button);
    }
    disconnectedCallback() {

    }
    attributeChangedCallback(name, oldValue, newValue) {
        if (name === 'state') {
            if (newValue === 'open') {
                this.settings_button.style.display = 'block';
            } else if (newValue === 'closed') {
                this.settings_button.style.display = 'none';
            }
        }
    }
    updateFields(username, date) {
        this.username_span.textContent = username;
        this.date_span.textContent = date;

    }
    async renderData( backend ) {
        let response = getUserData(backend);
        response.then((result) => {
            console.log(result);
            if (result.logged_in === true){
                this.updateFields(result.username, result.date_of_subscription)
            }
        })
    }
}
customElements.define('user-section', UserSection);

