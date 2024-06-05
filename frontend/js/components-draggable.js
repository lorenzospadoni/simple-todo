let draggable = null;
let is_dragging = false;
let list_items = document.querySelectorAll("todo-item");
// const list_container = document.querySelector('todo-container > div');

function initDraggable() {
    // list_container: use querySelector for a single container and querySelectorAll for multiple
    let list_container = document.querySelectorAll('todo-project > div'); 
    draggable = new Draggable.Sortable(( list_container ), {
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
    
    draggable.on('sortable:sorted', ( evt ) => {
        console.log('sortable:sorted')
    })
    draggable.on('sortable:start', ( evt ) => {
        console.log('sortable:start', evt);
        is_dragging = true;
    })
    
    draggable.on('sortable:move', (evt) => {
        console.log('sortable:move', evt);
    });
    
    draggable.on('sortable:stop', (evt) => {
        console.log('sortable:stop', evt);
        is_dragging = false;
    });
}
function destroyDraggable() {
    if (draggable) {
        // Remove all event listeners
        draggable.off('sortable:sorted');
        draggable.off('sortable:start');
        draggable.off('sortable:move');
        draggable.off('sortable:stop');

        // Clean up any draggable-specific attributes or styles (if necessary)
        document.querySelectorAll('todo-item').forEach(item => {
            item.removeAttribute('draggable');
            item.classList.remove('is-dragging', 'is-mirror');
        });

        // Destroy the draggable instance
        draggable.destroy();
        draggable = null;
    }
}