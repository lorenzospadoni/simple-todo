const main_section = document.getElementById("main_section");
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


const todo_container0 = document.createElement( 'todo-container' );
main_section.appendChild( todo_container0 );
console.log(todo_obj)
todo_container0.obj = todo_obj ;

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