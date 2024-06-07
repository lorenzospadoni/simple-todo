const main_section = document.getElementById("main_section");
const arrow = document.querySelector('todo-arrow');
const container = document.createElement( 'todo-container');
const navbar = document.querySelector('todo-navbar');
main_section.appendChild( container );

const STATE_MANAGER = new StateManager(container, arrow, navbar, true);
 // needed to stop the arrow from appearing on start up

