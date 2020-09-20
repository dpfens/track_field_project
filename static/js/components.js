(function(w, d) {
    function DragDrop(element, inputElement) {
        this.element = element;
        this.inputElement = inputElement;
    }

    DragDrop.prototype.initialize = function() {
        var dragListener = this.dragListener.bind(this),
            dropListener = this.dropListener.bind(this);
        this.element.addEventListener('ondrag', dragListener);
        this.element.addEventListener('ondrop', dropListener);
    }

    DragDrop.prototype.dragListener = function(event) {

    }

    DragDrop.prototype.dropListener = function(event) {

    }


    return window.DragDrop = DragDrop;
})(window, document);
