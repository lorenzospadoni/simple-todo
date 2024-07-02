import StateManager from './state-manager.js';
import { fetchProjects } from './todos.js';

const FRONTEND = 'http://127.0.0.1:3000/';
const BACKEND = 'http://127.0.0.1:5000/';

const main_section = document.getElementById("main_section");
const arrow = document.querySelector('todo-arrow');
const container = document.createElement( 'todo-container');
const navbar = document.querySelector('todo-navbar');
const section = document.querySelector('user-section');
main_section.appendChild( container );

const STATE_MANAGER = new StateManager(FRONTEND, BACKEND, container, arrow, navbar, section, true);
STATE_MANAGER.isLoggedIn()

console.log(fetchProjects(BACKEND)) 
// needed to stop the arrow from appearing on start up

