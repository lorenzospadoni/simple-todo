const main_section = document.getElementById("main_section");
const todo_arrow = document.querySelector('todo-arrow');
const todo_obj = [{
    'title' : "Saluti nel mondo",
    'children' : [
        {
            'content' : 'Hello!',
            'checked' :  false
        },        
        {
            'content' : 'Ciao!',
            'checked' :  false
        },
        {
            'content' : 'Bonjour!',
            'checked' :  true
        }
    ] 
},
{
    'title' : "Come stai?",
    'children' : [
        {
            'content' : 'Come stai?',
            'checked' :  false
        },        
        {
            'content' : 'How are you?!',
            'checked' :  false
        },
        {
            'content' : 'Comment ça va?',
            'checked' :  false
        }
    ] 
},
{
    'title' : "Buona sera nel mondo",
    'children' : [
        {
            'content' : 'Buona sera!',
            'checked' :  false
        },        
        {
            'content' : 'Good evening!',
            'checked' :  false
        },
        {
            'content' : 'Bonsoir!',
            'checked' :  false
        }
    ] 
}
];


const container = document.createElement( 'todo-container' );
main_section.appendChild( container );
console.log(todo_obj)
// todo_container0.obj = todo_obj ;

todo_arrow.container = container;
todo_arrow.getFromLocalStorage();
todo_arrow.setAttribute('state', 'overview'); // needed to stop the arrow from appearing on start up

