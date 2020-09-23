interface TabConfig {
    activeClass: string;
}

interface TabState {
    currentTabIndex: number;
    currentTabLink: HTMLElement | null;
    currentTabPanel: HTMLElement | null;
}

class Tabs {
    protected element: HTMLElement;
    protected config: TabConfig;
    protected state: TabState;

    constructor(element: HTMLElement, config: TabConfig) {
        this.element = element;
        this.config = config || {activeClass: 'is-active'};
        this.state = {
            currentTabIndex: -1,
            currentTabLink: null,
            currentTabPanel: null
        };
        this.clickHandler = this.clickHandler.bind(this);
    }

    initialize() {
        var tabLinks: NodeListOf<HTMLElement> = this.element.querySelectorAll('[role="tab"]');
        for (var i: number = 0; i < tabLinks.length; i++) {
            var tabLink: HTMLElement = tabLinks[i];
            tabLink.addEventListener('click', this.clickHandler);
        }
    }

    destroy() {
        var tabLinks: NodeListOf<HTMLElement> = this.element.querySelectorAll('[role="tab"]');
        for (var i: number = 0; i < tabLinks.length; i++) {
            var tabLink: HTMLElement = tabLinks[i];
            tabLink.removeEventListener('click', this.clickHandler);
        }
    }

    clickHandler(event: MouseEvent): void {
        var target: HTMLElement = <HTMLElement>event.currentTarget,
            panelId: string | null = target.getAttribute('aria-controls');
        if (!panelId || target.classList.contains(this.config.activeClass)) {
            return;
        }
        var panelElement: HTMLElement | null = document.getElementById(panelId);
        if (!panelElement) {
            return;
        }
        if (this.state.currentTabLink && this.state.currentTabPanel) {
            var tabLink: HTMLElement = this.state.currentTabLink;
            tabLink.setAttribute('aria-selected', 'false');
            tabLink.classList.remove(this.config.activeClass);
            this.state.currentTabPanel.classList.remove(this.config.activeClass);
        }

        var tabLinks: NodeListOf<HTMLElement> = this.element.querySelectorAll('[role="tab"]');
        for (var i: number = 0; i < tabLinks.length; i++) {
            var tabLink: HTMLElement= tabLinks[i];
            if (tabLink === target) {
                this.state.currentTabIndex = i;
                break;
            }
        }
        target.classList.add(this.config.activeClass);
        target.setAttribute('aria-selected', 'true');
        panelElement.classList.add(this.config.activeClass);
        this.state.currentTabLink = target;
        this.state.currentTabPanel = panelElement;
    }
}
