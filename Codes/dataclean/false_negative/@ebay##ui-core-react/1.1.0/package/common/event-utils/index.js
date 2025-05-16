"use strict";
/*
* Based on https://github.com/eBay/ebayui-core/edit/master/src/common/event-utils/index.js
*/
Object.defineProperty(exports, "__esModule", { value: true });
exports.wrapEvent = exports.handleResize = exports.removeEventListener = exports.addEventListener = exports.preventDefaultIfHijax = exports.handleTextInput = exports.handleLeftRightArrowsKeydown = exports.handleUpDownArrowsKeydown = exports.handleEscapeKeydown = exports.handleActionKeydown = exports.handleEnterKeydown = void 0;
/**
 * Generic keydown handler used by more specific cases
 * @param {Array} keyList: List of acceptable keys
 * @param {KeyboardEvent} e
 * @param {Function} callback
 */
function handleKeydown(keyList, e, callback) {
    if (callback === void 0) { callback = function () { }; }
    if (keyList.includes(e.key)) {
        callback();
    }
}
// inverse of found keys
function handleNotKeydown(keyList, e, callback) {
    if (callback === void 0) { callback = function () { }; }
    if (!keyList.includes(e.key)) {
        callback();
    }
}
function handleEnterKeydown(e, callback) {
    handleKeydown(['Enter'], e, callback);
}
exports.handleEnterKeydown = handleEnterKeydown;
function handleActionKeydown(e, callback) {
    handleKeydown([' ', 'Enter'], e, callback);
}
exports.handleActionKeydown = handleActionKeydown;
function handleEscapeKeydown(e, callback) {
    handleKeydown(['Esc', 'Escape'], e, callback);
}
exports.handleEscapeKeydown = handleEscapeKeydown;
function handleUpDownArrowsKeydown(e, callback) {
    handleKeydown(['Up', 'ArrowUp', 'Down', 'ArrowDown'], e, callback);
}
exports.handleUpDownArrowsKeydown = handleUpDownArrowsKeydown;
function handleLeftRightArrowsKeydown(e, callback) {
    handleKeydown(['Left', 'ArrowLeft', 'Right', 'ArrowRight'], e, callback);
}
exports.handleLeftRightArrowsKeydown = handleLeftRightArrowsKeydown;
// only fire for character input, not modifier/meta keys (enter, escape, backspace, tab, etc.)
function handleTextInput(e, callback) {
    var keyList = [
        // Edge
        'Esc',
        'Left',
        'Up',
        'Right',
        'Down',
        // Browsers
        'Tab',
        'Enter',
        'Shift',
        'Control',
        'Alt',
        'CapsLock',
        'Escape',
        'ArrowLeft',
        'ArrowUp',
        'ArrowRight',
        'ArrowDown',
        'Meta'
    ];
    handleNotKeydown(keyList, e, callback);
}
exports.handleTextInput = handleTextInput;
function preventDefaultIfHijax(e, hijax) {
    if (hijax) {
        e.preventDefault();
    }
}
exports.preventDefaultIfHijax = preventDefaultIfHijax;
var handlers = [];
function addEventListener(_, handler) {
    if (handlers.length === 0) {
        window.addEventListener('resize', handleResize);
    }
    handlers.push(handler);
}
exports.addEventListener = addEventListener;
function removeEventListener(_, handler) {
    if (handlers.length === 1) {
        window.removeEventListener('resize', handleResize);
    }
    handlers.splice(handlers.indexOf(handler), 1);
}
exports.removeEventListener = removeEventListener;
function handleResize(e) {
    window.removeEventListener('resize', handleResize);
    var callback = function () {
        if (handlers.length) {
            handlers.forEach(function (handler) { return handler(e); });
            window.addEventListener('resize', handleResize);
        }
    };
    if (window.requestAnimationFrame) {
        window.requestAnimationFrame(callback);
    }
    else {
        window.setTimeout(callback, 16);
    }
}
exports.handleResize = handleResize;
function wrapEvent(parentEventHandler, localEventHandler) {
    if (parentEventHandler === void 0) { parentEventHandler = function () { }; }
    return function (e) {
        parentEventHandler(e);
        if (!e.defaultPrevented) {
            return localEventHandler(e);
        }
    };
}
exports.wrapEvent = wrapEvent;
