import { hasToken } from './users.js';
import { redirectLogin } from './redirects.js';
import { 
    fetchProjects,
    postProject,
    postProjects,
    postProjectNewTitle,
    deleteProject,
    postItem,
    postItemContentChange, 
    deleteItem 
} from './todos.js'

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
                let item = project.newChild();
                item._id = result.item_id;   
            } else if (result.created == false) {
                console.log('[StateManager] COULD NOT CREATE NEW ITEM ON DB ');
            } else {
                throw new Error('result.created is nor equal to true nor to false');
            }
        })
        
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