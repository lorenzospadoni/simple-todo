import { hasToken } from './users.js';
import { redirectLogin } from './redirects.js';
import { 
    fetchProjects,
    postProject,
    postProjects,
    postProjectNewTitle,
    postProjectNewOrder,
    postNewItemOrder,
    deleteProject,
    postItem,
    postItemContentChange, 
    deleteItem 
} from './todos.js'
import {Draggable, Sortable, Plugins} from './dist/draggable.bundle.js'

export class StateManager {
    constructor(frontend, backend, _container, _arrow, _navbar, _section, startup_routine) {
        this.frontend = frontend;
        this.backend = backend;
        this._container = _container;
        this._arrow = _arrow;
        this._navbar = _navbar;
        this._section = _section;
        this._state = 0;

        this._arrow.container = this._container;
        this._navbar.container = this._container;

        this._project_draggable = null;
        this.project_draggable_active = false;
        this.project_is_dragging = null;

        this._item_draggable = null;
        this.item_is_dragging = null;

        if (startup_routine === true) {
            this.startUpRoutine();
        }

    }
    async startUpRoutine() {
        this.getSave();

        this._container.state_manager = this;
        this._arrow.state_manager = this;
        this._navbar.state_manager = this;

        
        this._navbar.updateContent();
        this._arrow.initOnClick();
        this._section.renderData( this.backend );
    }
    
    async getSave() {
        let projects = await fetchProjects(this.backend)
        this.container.json = projects;

    } 
    postSave() {
        //this.saveToLocalStorage()
        const projects = this.container.obj;
        postProjects(this.backend, projects);
        console.log('[postSave] POST request sent');
    }
    async handleNewProjectOnDb(project) {
        const response = postProject(this.backend);
        response.then((result) => {
            project._id = result.project_id;
        })

    }
    postNewProjectOnDb(project) {
        this.handleNewProjectOnDb(project)
    }

    async handleDeleteProjectOnDb(project) {
        const response = deleteProject(this.backend, project._id);
        response.then((result) => {
            console.log()
        })
    }

    deleteProjectOnDb(project) {
        this.handleDeleteProjectOnDb(project)
    }

    async handleProjectTitleChange(project) {
        const response = postProjectNewTitle(this.backend, project._id, project.title_box.textContent);
    }
    postProjectTitleChange(project) {
        if (project._id != null) {
            this.handleProjectTitleChange(project);
        }
    }
    async postOrder(project_id, item_order) {
        const response = postNewItemOrder(project_id, item_order, this.backend);
        return response;
    }
    postItemOrderOnDb(project) {
        this.handleItemOrder(project);
    }
    async handleItemOrder(project) {
        const response = postNewItemOrder(project._id, project.item_order, this.backend);
        console.log(project.item_order);
        return response;
    }
    async handleItemContentChange(item) {
        const response = postItemContentChange(this.backend, item._id, item.label.textContent)
    }
    postItemContentChange(item) {
        if (item._id != null) {
            this.handleItemContentChange(item)
        }
    }
    async handleDeleteItem(id) {
        const response = deleteItem(this.backend, id)
    }
    postNewItemOnDb(project) {
        this.handlePostNewItemOnDb(project)
    }
    async handlePostNewItemOnDb(project) {
        const response = postItem(this.backend, project._id);
        //console.log(result)
        response.then((result) => {
            console.log('handlePostNewItemOnDb(): ' + JSON.stringify(result))
            if (result.created == true) {
                this.destroyItemDraggable()
                let item = project.newChild();
                item._id = result.item_id;
                this.initItemDraggable() 
            } else if (result.created == false) {
                console.log('[StateManager] COULD NOT CREATE NEW ITEM ON DB ');
            } else {
                throw new Error('result.created is nor equal to true nor to false');
            }
        })
        
    }
    async handleNewProjectOrder(arr) {
        const response = postProjectNewOrder(arr, this.backend)
        return response;
    }
    newProjectOrder(container) {
        return this.handleNewProjectOrder(container.item_array_ids)
    }
    deleteItemOnDb(item) {
        if (item._id != null) {
            this.handleDeleteItem(item._id)
        }

    }
    saveToLocalStorage() {
        let container_data = this.container.json;
        localStorage.setItem('data', container_data);
    }
    getFromLocalStorage() {
        let data = localStorage.getItem('data');
        if (data === null) {
            data = '[]';
        }
        this.container.json = data;
    }
    cleanLocalStorage() {
        localStorage.clear();
    }

    handleStateOverview() {
        this.arrow.setAttribute('state', 'overview');
        this.container.setAttribute('state', 'overview');
    }
    handleStateSingle() {
        this.arrow.setAttribute('state', 'single');
        this.container.setAttribute('state', 'single');    
    }
    
    updateNavbarContent() {
        this._navbar.updateContent();
    }

    updateSectionContent() {
        this._section.renderData( this.backend )
    }
    async isLoggedIn() {
        let response = await hasToken( this.backend );
        if (response.has_token === true) {
            console.log('STATE MANAGER HAS TOKEN');
        } else if (response.has_token === false) {
            console.log('STATE MANAGER DOES NOT HAVE TOKEN');
            redirectLogin(this.frontend);
        } else {
            console.log('STATE MANAGER HAS... ?');
        }
    }

    initProjectDraggable() {
        console.log('[ACTIVATING PROJECT DRAGGABLE]')
        if (this.project_draggable_active === false) {
            // list_container: use querySelector for a single container and querySelectorAll for multiple
            let list_container = document.querySelector('todo-container > div'); 
            this._project_draggable = new Sortable(( list_container ), {
                draggable : 'todo-project',
                mirror: {
                    constrainDimensions: true,
                },
                classes: {
                    'source:dragging': 'is-dragging',
                    'mirror': 'is-mirror',
                },
                plugins: [Plugins.SortAnimation],
                swapAnimation: {
                    duration: 200,
                    easingFunction: 'ease-in-out',
                },
            });

            this._project_draggable.on('sortable:sorted', ( evt ) => {
                console.log('sortable:sorted');
                //this.postItemOrderOnDb(evt.newContainer.parentElement);

            })
            this._project_draggable.on('sortable:start', ( evt ) => {
                console.log('sortable:start', evt);
                this.project_is_dragging = true;
                // this ensures that the copy that stays still when the drag event occurs
                // aka 'source' has as title the same textContent as the original source
                // aka the real element that is hidden by Draggable during drag events
                //this is basically sorcery don't touch it for your life
                const source_element = evt.data.dragEvent.data.source;
                const og_element = evt.data.dragEvent.data.originalSource;
                source_element.title_box.textContent = og_element.title_box.textContent;
                // this serves no purpose other than to avoid polluting the dev console with errors:
                source_element.state_manager = og_element.state_manager;
            })

            this._project_draggable.on('sortable:move', (evt) => {
                console.log('sortable:move', evt);
            });

            this._project_draggable.on('sortable:stop', (evt) => {
                console.log('sortable:stop', evt);
                this.project_is_dragging = false;
                //console.log(evt.newContainer.parentElement);
            });
            this._project_draggable.on('mirror:create'), (evt) => {
                console.log('AAAAAAAmirror:create', evt);
            }
            this._project_draggable.on('mirror:created', function (evt) {
                //let mirror = evt.data.mirror;
                console.log('mirror:created', evt);
                console.log(evt.originalSource.title);
                // this ensures that the mirror element, that is the element that
                // follows the pointer around when dragging has the title
                // of the original element that is hidden during Draggable events
                // again, it's badly-documented magic don't touch it.
                const mirror_element = evt.data.mirror;
                const og_element = evt.originalSource;
                mirror_element.title_box.textContent = og_element.title_box.textContent;
                mirror_element.state_manager = og_element.state_manager;
                console.log('mirror:created og state_manager', og_element.state_manager);
                console.log('mirror:created mirror state_manager', mirror_element.state_manager);
                console.log('mirror:created this object', this)
                //evt.data.mirror.title_box.textContent = evt.originalSource.title;
            });
            this._project_draggable.on('mirror:destroy', (evt) => {
                console.log('mirror:destroy', evt);
                const container = evt.sourceContainer.parentElement;
                // ugliest shit I've ever seen
                // but I'm short on ideas on how to save to the db AFTER draggable has ended
                setTimeout(() => {this.newProjectOrder(container);}, 600)
                
            });
            this.project_draggable_active = true;
        }
        
    }
    destroyProjectDraggable() {
        console.log('[DEACTIVATING PROJECT DRAGGABLE]')
        if (this._project_draggable !== null) {
            // Remove all event listeners
            this._project_draggable.off('sortable:sorted');
            this._project_draggable.off('sortable:start');
            this._project_draggable.off('sortable:move');
            this._project_draggable.off('sortable:stop');
    
            // Clean up any draggable-specific attributes or styles (if necessary)
            document.querySelectorAll('todo-project').forEach(project => {
                project.removeAttribute('draggable');
                project.classList.remove('is-dragging', 'is-mirror');
            });
    
            // Destroy the draggable instance
            this._project_draggable.destroy();
            this._project_draggable = null;
            this.project_draggable_active = false;
        }
    }

    initItemDraggable() {
        // list_container: use querySelector for a single container and querySelectorAll for multiple
        let list_container = document.querySelectorAll('todo-project > div'); 
        this._item_draggable = new Sortable(( list_container ), {
            draggable : 'todo-item',
            mirror: {
                constrainDimensions: true,
            },
            classes: {
                'source:dragging': 'is-dragging',
                'mirror': 'is-mirror',
            },
            plugins: [Plugins.SortAnimation],
            swapAnimation: {
                duration: 200,
                easingFunction: 'ease-in-out',
            },
        });
        
        this._item_draggable.on('sortable:sorted', ( evt ) => {
            console.log('sortable:sorted');
            //this.postItemOrderOnDb(evt.newContainer.parentElement);

        })
        this._item_draggable.on('sortable:start', ( evt ) => {
            console.log('sortable:start', evt);
            this.item_is_dragging = true;
            const source_item = evt.data.dragEvent.data.source;
            const og_item = evt.data.dragEvent.data.originalSource;
            // this serves no purpose other than to avoid polluting the dev console with errors:
            source_item.state_manager = og_item.state_manager;
            
        })
        
        this._item_draggable.on('sortable:move', (evt) => {
            console.log('sortable:move', evt);
        });
        
        this._item_draggable.on('sortable:stop', (evt) => {
            console.log('sortable:stop', evt);
            this.item_is_dragging = false;
            console.log(evt.newContainer.parentElement);
        });
        this._item_draggable.on('mirror:destroy', (evt) => {
            console.log('mirror:destroy', evt);
            const container = evt.sourceContainer.parentElement;
            // ugliest shit I've ever seen
            // but I'm short on ideas on how to save to the db AFTER draggable has ended
            setTimeout(() => {this.postItemOrderOnDb(container);}, 600)
            
        });


    }
    destroyItemDraggable() {
        if (this._item_draggable) {
            // Remove all event listeners
            this._item_draggable.off('sortable:sorted');
            this._item_draggable.off('sortable:start');
            this._item_draggable.off('sortable:move');
            this._item_draggable.off('sortable:stop');
    
            // Clean up any draggable-specific attributes or styles (if necessary)
            document.querySelectorAll('todo-item').forEach(item => {
                item.removeAttribute('draggable');
                item.classList.remove('is-dragging', 'is-mirror');
            });
    
            // Destroy the draggable instance
            this._item_draggable.destroy();
            this._item_draggable = null;
        }
    }
    get state() {
        if ( this._state === 0 ) {
            return 'overview';
        } else if ( this._state === 1) {
            return 'single';
        } else {
            throw new TypeError('state should be either 0 or 1');
        }
    }

    set state( value ) {
        if ( value === 'overview' || value === 0) {
            this._state = 0;
            this.handleStateOverview()

        } else if ( value === 'single' || value === 1) {
            this._state = 1;
            this.handleStateSingle();
        } else {
            throw new TypeError('state setter accepts either "overview"/0 or "single"/1');
        }
    }
    get navbar() {
        return this._navbar;
    }
    set navbar( el ) {
        this._navbar = el;
        this._navbar.container = this.container;
    }

    get container() {
        return this._container;
    }

    set container( el ) {
        // setter may be needed to perform extra actions later
        this._container = el;
    }

    get arrow() {
        return this._arrow;
    }

    set arrow( el ) {
        this._arrow = el;
        this._arrow.initOnClick();
    }

    get isInitialized() {
        if (this._container !== null && this._arrow !== null) {
            return true;
        } else {
            return false;
        }
    }

}