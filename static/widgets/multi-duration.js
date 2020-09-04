(function(){

    function isBackSpaceEvent(event) {
        var code = event.key || event.keyCode;
        return code === 'Backspace';
    }

    function isNumberEvent(event) {
        if (event.key !== undefined) {
            var key = event.key;
            isNumber = !isNaN(key) && key !== ' ' && key !== null;
        } else if (event.keyCode !== undefined) {
            var keycode = event.keyCode,
                isKeyPadNumber = keyCode >= 96 && keyCode <= 105,
                isNumberLine = keyCode >= 48 && keyCode <= 57;
            isNumber = isNumberLine || isNumberLine;
        }
        return isNumber;
    }

    function FlowInput(element, previous, next, config) {
        this.element = element;
        this.previous = previous;
        this.next = next;
        this.config = config;
    }

    FlowInput.prototype.validate = function() {}

    FlowInput.prototype.isNavigation = function(event) {
        var code = event.key || event.keyCode;
        return code === 'Backspace' || code === 'Tab' ||
            code === 'ArrowLeft' || code === 'ArrowRight' ||
            code === 'ArrowUp' || code === 'ArrowDown';
    }

    FlowInput.prototype.focusPrevious = function() {
        this.previous.focus();
        var selectionEnd = this.previous.value.length;
        this.previous.setSelectionRange(selectionEnd, selectionEnd);
    }

    FlowInput.prototype.focusNext = function() {
        this.next.focus();
        var selectionEnd = this.next.value.length;
        this.next.setSelectionRange(0, selectionEnd);
    }

    FlowInput.prototype.keyDownListener = function(event){
        var isBackSpace = isBackSpaceEvent(event),
            isNavigation = this.isNavigation(event),
            key = event.key || event.keyCode ,
            isArrowLeft = key === 'ArrowLeft',
            isArrowRight = key === 'ArrowRight',
            value = this.element.value,
            selectionStart = this.element.selectionStart,
            shiftingToPrevious = (!value.length && isBackSpace) || // shifting left using backspace
            (!selectionStart && isArrowLeft && !event.shiftKey), // shifting left using left arrow key
            shiftingToNext = selectionStart === value.length && isArrowRight && !event.shiftKey; // shifting right using right arrow key
        if (value.length >= this.config.limit && !isNavigation) { // if current element is full, add key to next element, if a next element exists
            if (this.next) {
                this.focusNext();
            } else {
                event.preventDefault();
            }
        }
        if (this.previous && shiftingToPrevious) {
            this.focusPrevious();
            event.preventDefault();
        }
        else if (this.next && shiftingToNext) {
            this.focusNext();
            event.preventDefault();
        }

    }

    FlowInput.prototype.inputListener = function(event) {
        var isValid = this.validate();
        var value = this.element.value;
        if (value.length >= this.config.limit && this.next && isValid) {
            this.focusNext();
        }
    }

    FlowInput.prototype.initialize = function() {
        this.element.addEventListener('keydown', this.keyDownListener.bind(this));
        this.element.addEventListener('input', this.inputListener.bind(this))
    }

    function NumberFlowInput(element, previous, next, config) {
        FlowInput.call(this, element, previous, next, config);
    }

    NumberFlowInput.prototype = Object.create(FlowInput.prototype);

    NumberFlowInput.prototype.validate = function() {
        var value = this.element.value;
        if (value.length) {
            value = parseInt(value);
            var outOfRange = false,
            min = this.config.min,
            max = this.config.max;
            if (min && value < parseInt(min)) {
                outOfRange = true;
            } else if (max && value > parseInt(max)) {
                outOfRange = true;
            }
            if(outOfRange) {
                this.element.setCustomValidity('Value must be between ' + min + ' and ' + max);
            } else {
                this.element.setCustomValidity('');
            }
        }
        return this.element.reportValidity();
    }

    NumberFlowInput.prototype.keyDownListener = function(event) {
        var isNumber = isNumberEvent(event),
            isNavigation = this.isNavigation(event);
        if (!isNumber && !isNavigation) {
            event.preventDefault();
        }
        FlowInput.prototype.keyDownListener.call(this, event);
    }

    NumberFlowInput.prototype.initialize = function() {
        FlowInput.prototype.initialize.call(this);
    }

    var durationInputElements = document.querySelectorAll('div.duration-input');
    for (var i = 0; i <durationInputElements.length; i++) {
        var durationElement = durationInputElements[i],
        inputElements = durationElement.querySelectorAll('input');
        var previousElement = null;
        for (var j = 0; j < inputElements.length; j++) {
            var inputElement = inputElements[j],
                nextElement = null,
                limit = inputElement.getAttribute('limit'),
                min = inputElement.getAttribute('min'),
                max = inputElement.getAttribute('max'),
                config = {'limit': limit, 'min': min, 'max': max};
            if (j < inputElements.length - 1) {
                nextElement = inputElements[j + 1];
            }
            var instance = new NumberFlowInput(inputElement, previousElement, nextElement, config);
            instance.initialize();
            previousElement = inputElement;
        }
    }
})();
