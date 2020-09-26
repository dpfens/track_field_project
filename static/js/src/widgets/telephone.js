(function() {
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

    function TelephoneFormatter(element) {
      this.element = element;
      this.value = element.value; // stores raw telephone number
    }

    TelephoneFormatter.prototype.isBackNavigation = function(event) {
      var code = event.key || event.keyCode;
        return code === 'Backspace' || code === 'ArrowLeft' || code === 'ArrowUp';
    }

    TelephoneFormatter.prototype.isForwardNavigation = function(event) {
      var code = event.key || event.keyCode;
      return code === 'Tab' || code === 'ArrowRight' || code === 'ArrowDown';
    }

    TelephoneFormatter.prototype.isNavigation = function(event) {
        return this.isBackNavigation(event) || this.isForwardNavigation(event);
    }

    TelephoneFormatter.prototype.validate = function() {
      return this.isNavigation(event) || isNumberEvent(event);
    }

    TelephoneFormatter.prototype.keyDownListener = function(event) {
      isValid = this.validate(event);
      if (!isValid){
        event.preventDefault();
      }
    }

    TelephoneFormatter.prototype.inputListener = function(event) {
      var value = this.element.value,
          valueLength,
          formattedValue;
      this.value = value.replace(/\D/g,'');
      formattedValue = this.value;
      valueLength = this.value.length;

      if (valueLength == 0) {
          formattedValue = formattedValue;
      } else if(valueLength < 4) {
          formattedValue = '('+formattedValue;
      } else if(valueLength < 7) {
          formattedValue = '('+formattedValue.substring(0,3)+') '+formattedValue.substring(3,6);
      } else if(valueLength === 7) {
          formattedValue = '('+formattedValue.substring(0,3)+') '+formattedValue.substring(3,7);
      } else if (valueLength < 11) {
          formattedValue = '('+formattedValue.substring(0,3)+') '+formattedValue.substring(3,6)+' - '+formattedValue.substring(6);
      } else {
        var countryCodeEnd = valueLength - 10;
          formattedValue = '+' + formattedValue.substring(0, countryCodeEnd) + '('+ formattedValue.substring(countryCodeEnd, countryCodeEnd+3)+') '+formattedValue.substring(countryCodeEnd+3,countryCodeEnd+6)+' - '+formattedValue.substring(countryCodeEnd+6);
      }
      this.element.value = formattedValue;
    }

    TelephoneFormatter.prototype.initialize = function() {
      this.element.addEventListener('keydown', this.keyDownListener.bind(this));
      this.element.addEventListener('input', this.inputListener.bind(this));
    }

    var InputElements = document.querySelectorAll('input.phone-input');
      for (var i = 0; i < InputElements.length; i++) {
          var element = InputElements[i],
              instance = new TelephoneFormatter(element);
          instance.initialize();
    }
})();
