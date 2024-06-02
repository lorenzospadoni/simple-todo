const main_section = document.getElementById("main_section");
const todo_obj = {
    'title' : "My first todo project",
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
};


/* const todo_container0 = document.createElement( 'todo-container' );
main_section.appendChild( todo_container0 );
todo_container0.obj = todo_obj ;
 */

// using querySelectorAll because Draggable wants a Node_List, not an HTMLCollection
/* const list_items = document.querySelectorAll("todo-item");
const list_container = document.querySelector('section');
const draggable = new Draggable.Sortable(( list_container ), {
    draggable : 'todo-item',
    mirror: {
        constrainDimensions: true,
    },
    classes: {
        'source:dragging': 'is-dragging',
        'mirror': 'is-mirror',
    },
    plugins: [
        Draggable.Plugins.SortAnimation
    ],

    swapAnimation: {
      duration: 200,
      easingFunction: 'ease-in-out',
    },
});

draggable.on('sortable:sorted', (evt) => {
    console.log('sortable:sorted')
})
draggable.on('sortable:start', ( evt ) => {
    console.log('sortable:start', evt)
})

draggable.on('sortable:move', (evt) => {
    console.log('sortable:move', evt);
});

draggable.on('sortable:stop', (evt) => {
    console.log('sortable:stop', evt);
}); */