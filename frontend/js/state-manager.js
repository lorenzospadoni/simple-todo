class StateManager {
    constructor(_container, _arrow, _navbar) {
        this._container = _container;
        this._arrow = _arrow;
        this._navbar = _navbar;
        this._state = 0;

        this._arrow.container = this._container;
        this._navbar.container = this._container;

        this.getFromLocalStorage();

        this._navbar.updateContent();
        this._arrow.initOnClick();

    }
    saveToLocalStorage() {
        let container_data = this.container.json;
        localStorage.setItem('data', container_data);
    }
    getFromLocalStorage() {
        let data = localStorage.getItem('data');
        this.container.json = data;
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
        this.navbar.updateContent();
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