//import StateManager from './state-manager.js';
import { fetchProjects } from './todos.js';

// import components
import {
    TodoArrow,
    TodoContainer,
    TodoItem,
    TodoNavbar, 
    ProjectMenu, 
    TodoProject, 
    UserSection, 
    StateManager
} from './webcomponents.js';

customElements.define('todo-arrow', TodoArrow);
customElements.define('todo-container', TodoContainer);
customElements.define('todo-item', TodoItem);
customElements.define('todo-navbar', TodoNavbar);
customElements.define('project-menu', ProjectMenu);
customElements.define('todo-project', TodoProject);
customElements.define('user-section', UserSection);


const FRONTEND = 'http://127.0.0.1:3000/';
const BACKEND = 'http://127.0.0.1:5000/';

const main_section = document.getElementById("main_section");
const arrow = document.querySelector('todo-arrow');
const container = document.createElement( 'todo-container');
const navbar = document.querySelector('todo-navbar');
const section = document.querySelector('user-section');
main_section.appendChild( container );

const STATE_MANAGER = new StateManager(FRONTEND, BACKEND, container, arrow, navbar, section, false);
STATE_MANAGER.startUpRoutine();
STATE_MANAGER.initItemDraggable();

//console.log(fetchProjects(BACKEND)) 
// needed to stop the arrow from appearing on start up

