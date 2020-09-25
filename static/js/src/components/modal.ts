interface ModalConfig {
    activeClass: string | null;
}


class Modal {
    protected buttonElement: HTMLElement;
    protected modalElement: HTMLElement;
    private config: ModalConfig;

    constructor(buttonElement: HTMLElement, modalElement: HTMLElement, config: ModalConfig) {
        this.buttonElement = buttonElement;
        this.modalElement = modalElement;
        this.config = config;
        this.openHandler = this.openHandler.bind(this);
        this.closeHandler = this.closeHandler.bind(this);
    }

    initialize() {
        this.buttonElement.addEventListener('click', this.openHandler);

        var closeElement: HTMLElement | null = this.modalElement.querySelector('.close');
        if (closeElement) {
            closeElement.addEventListener('click', this.closeHandler);
        }
        var backdropElement: HTMLElement | null = this.modalElement.querySelector('.backdrop');
        if (backdropElement) {
            backdropElement.addEventListener('click', this.closeHandler);
        }
    }

    destroy() {
        this.buttonElement.removeEventListener('click', this.openHandler);
        var closeElement: HTMLElement | null = this.modalElement.querySelector('.close');
        if (closeElement) {
            closeElement.removeEventListener('click', this.closeHandler);
        }
    }

    openHandler() {
        var activeClass: string = this.config.activeClass || 'is-active';
        this.modalElement.classList.toggle(activeClass);
    }

    closeHandler() {
        var activeClass: string = this.config.activeClass || 'is-active';
        this.modalElement.classList.toggle(activeClass);
    }
}
