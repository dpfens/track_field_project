interface FLIPConfig {
    activeClass: string;
    inactiveClass: string | null;
    transitionClass: string;
}

class CSSTransitionFLIP {
    private element: HTMLElement;
    private activeClass: string | null;
    private inactiveClass: string | null;
    private transitionClass: string;

    constructor(element: HTMLElement, transitionClass: string, activeClass: string | null, inactiveClass: string | null) {
        element.style.willChange = 'transform';
        this.element = element;
        this.transitionClass = transitionClass;
        this.activeClass = activeClass;
        this.inactiveClass = inactiveClass;
    }

    calculateTransform(a: DOMRect, b: DOMRect): string {
        const scaleY = a.height / b.height;
        const scaleX = a.width / b.width;

        // dividing by 2 centers the transform since the origin
        // is centered not top left
        const translateX = a.left + a.width / 2 - (b.left + b.width / 2);
        const translateY = a.top + a.height / 2 - (b.top + b.height / 2);
        return [
            `translateX(${translateX}px)`,
            `translateY(${translateY}px)`,
            `scaleY(${scaleY})`,
            `scaleX(${scaleX})`
        ].join(" ");
}

    toggle(callback: any) {
        var element: HTMLElement = this.element,
            oldBoundingBox: DOMRect = element.getBoundingClientRect(),
            transitionClass: string = this.transitionClass,
            newBoundingBox: DOMRect,
            transformStatement;

        if (this.activeClass) {
            element.classList.toggle(this.activeClass);
        }
        if(this.inactiveClass) {
            element.classList.toggle(this.inactiveClass);
        }
        newBoundingBox = element.getBoundingClientRect();
        transformStatement = this.calculateTransform(oldBoundingBox, newBoundingBox);
        element.style.transform = transformStatement;
        element.getBoundingClientRect(); // force redraw
        element.classList.add(transitionClass);
        element.style.transform = "translateX(0) translateX(0)";
        var transitionClass: string = this.transitionClass;
        element.addEventListener("transitionend", function() {
            element.removeAttribute("style");
            element.classList.remove(transitionClass);
            if (callback) {
                callback(element);
            }
        }, { once: true });
    }
}
