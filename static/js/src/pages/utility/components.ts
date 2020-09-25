var dropdownElements: NodeList = document.querySelectorAll('.dropdown:not(.is-hover)');

if (dropdownElements) {
    for (var i:number = 0; i < dropdownElements.length; i++) {
        var dropdownElement: HTMLElement = <HTMLElement>dropdownElements[i],
            triggerElement: HTMLElement | null,
            menuElement: HTMLElement | null;

            if (!dropdownElement) {
                continue;
            }
            triggerElement = dropdownElement.querySelector('.dropdown-trigger');
            menuElement = dropdownElement.querySelector('.dropdown-menu');
        if (!triggerElement || !menuElement){
          continue;
        }
        var dropdownInstance = new DropdownMenu(dropdownElement, triggerElement, menuElement);
        dropdownInstance.initialize();
    }
}

var fileDrops: NodeList = document.querySelectorAll('.drag-drop');

if (fileDrops) {
    for (var i:number = 0; i < fileDrops.length; i++) {
        var fileDrop: HTMLElement = <HTMLElement>fileDrops[i],
            inputElement: HTMLInputElement | null = fileDrop.querySelector('input');
            if (!fileDrop || !inputElement) {
                continue;
            }
        var dragAndDropInstance = new DragAndDrop(fileDrop, inputElement);
        dragAndDropInstance.initialize();
    }
}
