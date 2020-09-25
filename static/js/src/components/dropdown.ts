interface DropdownConfig {
    activeClass: string;
}

class DropdownMenu {
    protected element: HTMLElement;
    protected triggerElement: HTMLElement;
    protected menuElement: HTMLElement;
    protected config: any;
    protected activeClass: string;

    constructor(element: HTMLElement, triggerElement: HTMLElement, menuElement: HTMLElement, config?: DropdownConfig) {
        this.element = element;
        this.triggerElement = triggerElement;
        this.menuElement = menuElement;
        config = config || {activeClass: 'is-active'};
        this.config = config;
        this.activeClass = config.activeClass;
        this.openHandler = this.openHandler.bind(this);
        this.closeHandler = this.closeHandler.bind(this);
        this.toggleHandler = this.toggleHandler.bind(this);
        this.windowHandler = this.windowHandler.bind(this);

    }

    initialize() {
        this.triggerElement.addEventListener('click', this.toggleHandler);
        window.addEventListener('click', this.windowHandler);
    }

    destroy() {
        if (this.config.click) {
            this.triggerElement.removeEventListener('click', this.toggleHandler);
            window.removeEventListener('click', this.windowHandler);
        } else {
            this.triggerElement.removeEventListener('mouseover', this.openHandler);
            this.triggerElement.removeEventListener('mouseout', this.closeHandler);
        }
    }

    open(): void {
        this.element.classList.add(this.activeClass);
    }

    openHandler(): void {
        this.open();
    }

    close(): void {
        this.element.classList.remove(this.activeClass);
    }

    closeHandler(): void {
        this.close();
    }

    isOpen(): boolean {
        return this.element.classList.contains(this.activeClass);
    }

    toggle(): void {
        if (this.isOpen()) {
            this.close()
        } else {
            this.open();
        }
    }

    toggleHandler(): void {
        this.toggle();
    }

    windowHandler(event: MouseEvent): void {
        // close dropdown if user clicks outside of the dropdown
        var target: HTMLElement = <HTMLElement> event.target,
            menuElement: Node = <Node> this.element,
            targetNode: Node = <Node> target,
            isDropdownElement: boolean = target === this.menuElement || menuElement.contains(targetNode);
        if (!isDropdownElement && this.isOpen()){
            event.stopPropagation();
            this.toggle();
        }
    }
}
