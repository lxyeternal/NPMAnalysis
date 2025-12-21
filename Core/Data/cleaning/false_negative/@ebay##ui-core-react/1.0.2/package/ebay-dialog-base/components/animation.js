"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.useDialogAnimation = void 0;
var react_1 = require("react");
function useDialogAnimation(_a) {
    var open = _a.open, classPrefix = _a.classPrefix, transitionElement = _a.transitionElement, dialogRef = _a.dialogRef, dialogWindowRef = _a.dialogWindowRef, enabled = _a.enabled, onTransitionEnd = _a.onTransitionEnd;
    var firstRender = react_1.useRef(true);
    react_1.useLayoutEffect(function () {
        if (!enabled) {
            return;
        }
        var transitionElements = [dialogWindowRef, dialogRef];
        if (transitionElement === 'window') {
            transitionElements = [dialogWindowRef];
        }
        else if (transitionElement === 'root') {
            transitionElements = [dialogRef];
        }
        var cancelCurrentAnimation;
        if (open) {
            cancelCurrentAnimation = showAnimation({
                dialog: dialogRef,
                waitFor: transitionElements,
                classPrefix: classPrefix,
                onTransitionEnd: onTransitionEnd
            });
        }
        else if (!firstRender.current) {
            cancelCurrentAnimation = hideAnimation({
                dialog: dialogRef,
                waitFor: transitionElements,
                classPrefix: classPrefix,
                onTransitionEnd: onTransitionEnd
            });
        }
        firstRender.current = false;
        return function () {
            if (cancelCurrentAnimation) {
                cancelCurrentAnimation();
            }
        };
    }, [open, enabled]);
}
exports.useDialogAnimation = useDialogAnimation;
function showAnimation(_a) {
    var dialog = _a.dialog, waitFor = _a.waitFor, classPrefix = _a.classPrefix, onTransitionEnd = _a.onTransitionEnd;
    return transition(dialog, waitFor, classPrefix + "--show", onTransitionEnd);
}
function hideAnimation(_a) {
    var dialog = _a.dialog, waitFor = _a.waitFor, classPrefix = _a.classPrefix, onTransitionEnd = _a.onTransitionEnd;
    return transition(dialog, waitFor, classPrefix + "--hide", onTransitionEnd);
}
function transition(element, waitFor, className, onTransitionEnd) {
    if (!element.current || !className) {
        return;
    }
    var ran = 0;
    var pending = waitFor ? waitFor.length : 0;
    var initClass = className + "-init";
    element.current.classList.add(initClass);
    return nextFrame(function () {
        if (!element.current) {
            return;
        }
        element.current.classList.add(className);
        element.current.classList.remove(initClass);
        waitFor.forEach(function (ref) {
            var listener = function () {
                var _a, _b;
                if (++ran === pending) {
                    (_a = element.current) === null || _a === void 0 ? void 0 : _a.classList.remove(className);
                    onTransitionEnd();
                    (_b = ref.current) === null || _b === void 0 ? void 0 : _b.removeEventListener('transitionend', listener);
                }
            };
            ref.current.addEventListener('transitionend', listener, { once: true });
        });
    });
}
function nextFrame(callback) {
    var frame;
    var cancelFrame;
    if (window.requestAnimationFrame) {
        frame = window.requestAnimationFrame(function () {
            frame = window.requestAnimationFrame(callback);
        });
        cancelFrame = window.cancelAnimationFrame;
    }
    else {
        frame = window.setTimeout(callback, 26); // 16ms to simulate RAF, 10ms to ensure called after the frame.
        cancelFrame = window.clearTimeout;
    }
    return function () {
        if (frame) {
            cancelFrame(frame);
            frame = undefined;
        }
    };
}
