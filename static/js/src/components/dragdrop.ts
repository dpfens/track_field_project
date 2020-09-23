interface DragAndDropConfig {
    fileElement: HTMLElement;
    validationFunc: any;
}


class DragAndDrop {
    protected element: HTMLElement;
    protected inputElement: HTMLInputElement;
    protected config: DragAndDropConfig;

    constructor(element: HTMLElement, inputElement: HTMLInputElement, config: DragAndDropConfig) {
        this.element = element;
        this.inputElement = inputElement;
        this.config = config;

        this.clickHandler = this.clickHandler.bind(this);
        this.dragEnterHandler = this.dragEnterHandler.bind(this);
        this.dragLeaveHandler = this.dragLeaveHandler.bind(this);
        this.dragOverHandler = this.dragOverHandler.bind(this);
        this.dropHandler = this.dropHandler.bind(this);
    }

    initialize() {
        this.element.addEventListener('click', this.clickHandler);
        this.element.addEventListener('dragenter', this.dragEnterHandler);
        this.element.addEventListener('dragleave', this.dragLeaveHandler);
        this.element.addEventListener('dragover', this.dragOverHandler);
        this.element.addEventListener('drop', this.dropHandler);
    }

    destroy() {
        this.element.removeEventListener('click', this.clickHandler);
        this.element.removeEventListener('dragenter', this.dragEnterHandler);
        this.element.removeEventListener('dragleave', this.dragLeaveHandler);
        this.element.removeEventListener('dragover', this.dragOverHandler);
        this.element.removeEventListener('drop', this.dropHandler);
    }

    clickHandler() {
        this.inputElement.click();
    }

    dragEnterHandler(event: DragEvent) {
        event.stopPropagation();
    }

    dragOverHandler(event: DragEvent) {
        event.stopPropagation();
        event.preventDefault();
    }

    dragLeaveHandler(event: DragEvent) {
        console.log(event);
    }

    dropHandler(event: DragEvent) {
        if (event.dataTransfer) {
            var files: FileList = event.dataTransfer.files
            if (this.config.validationFunc && !this.config.validationFunc(files)) {
                return;
            }
            this.inputElement.files = event.dataTransfer.files;
        }
        event.preventDefault();
    }
}
