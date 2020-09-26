(function() {

    function LengthSlider(element) {
        this.element = element;
        this.value = element.value; // stores raw Lengthe number
    }

    LengthSlider.prototype.inputListener = function(event) {
        var value = this.element.value;
        this.element.value = formattedValue;
    }

    LengthSlider.prototype.initialize = function() {
        this.element.addEventListener('input', this.inputListener.bind(this));
    }

    var InputElements = document.querySelectorAll('input.length-input');
    for (var i = 0; i < InputElements.length; i++) {
        var element = InputElements[i],
            instance = new LengthSlider(element);
        instance.initialize();
    }
})();
