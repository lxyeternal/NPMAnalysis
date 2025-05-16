"use strict";
// copy-pasted from @ebay/ebayui-core/dist/components/ebay-carousel/utils/scroll-transition
// todo: replace with ebayui-core-react/ebay-carousel when it's ready
Object.defineProperty(exports, "__esModule", { value: true });
exports.scrollTransition = void 0;
var onScrollEnd = function (el, fn) {
    var timeout;
    var frame;
    var lastPos;
    (function checkMoved() {
        var scrollLeft = el.scrollLeft;
        if (lastPos !== scrollLeft) {
            lastPos = scrollLeft;
            timeout = setTimeout(function () {
                frame = requestAnimationFrame(checkMoved);
            }, 90);
            return;
        }
        fn(lastPos);
    }());
    return function () {
        clearTimeout(timeout);
        cancelAnimationFrame(frame);
    };
};
var supportsScrollBehavior = typeof window !== 'undefined' && 'scrollBehavior' in document.body.style;
/**
 * Utility to animate scroll position of an element using an `ease-out` curve over 250ms.
 * Cancels the animation if the user touches back down.
 *
 * @param {HTMLElement} el The element to scroll.
 * @param {number} to The offset to animate to.
 * @param {function} fn A function that will be called after the transition completes.
 * @return {function} A function that cancels the transition.
 */
function scrollTransition(el, to, fn) {
    if (supportsScrollBehavior) {
        el.scrollTo({ left: to });
        return onScrollEnd(el, fn);
    }
    var lastPosition;
    var cancelInterruptTransition;
    var frame = requestAnimationFrame(function (startTime) {
        var scrollLeft = el.scrollLeft;
        var distance = to - scrollLeft;
        var duration = 450;
        (function animate(curTime) {
            var delta = curTime - startTime;
            if (delta > duration) {
                el.scrollLeft = to;
                cancel();
                return fn();
            }
            el.scrollLeft = easeInOut(delta / duration) * distance + scrollLeft;
            frame = requestAnimationFrame(animate);
        }(startTime));
    });
    // The animation can be interrupted by new touch events.
    el.addEventListener('touchstart', handleTouchStart);
    return cancel;
    function cancel() {
        cancelAnimationFrame(frame);
        if (lastPosition === undefined) {
            cancelTouchStart();
        }
        else {
            if (cancelInterruptTransition)
                cancelInterruptTransition();
            cancelTouchEnd();
        }
    }
    function handleTouchStart() {
        cancel();
        lastPosition = el.scrollLeft;
        // If we were interrupted by a touch start we wait for a touch end to see if we moved.
        el.addEventListener('touchend', handleTouchEnd);
    }
    function handleTouchEnd() {
        cancelTouchEnd();
        // If we haven't moved because of the interrupt we continue to transition.
        if (lastPosition === el.scrollLeft) {
            cancelInterruptTransition = scrollTransition(el, to, fn);
        }
    }
    function cancelTouchStart() {
        el.removeEventListener('touchstart', handleTouchStart);
    }
    function cancelTouchEnd() {
        el.removeEventListener('touchend', handleTouchEnd);
    }
}
exports.scrollTransition = scrollTransition;
/**
 * Ease out timing function.
 * Based on https://gist.github.com/gre/1650294.
 *
 * @param {number} val - A number between 0 and 1.
 * @return {number}
 */
function easeInOut(val) {
    return val < 0.5 ? 2 * val * val : -1 + (4 - 2 * val) * val;
}
