"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var useKeyPress = function () {
    var _a = react_1.useState(false), arrowUpPressed = _a[0], setArrowUpPressed = _a[1];
    var _b = react_1.useState(false), arrowDownPressed = _b[0], setArrowDownPressed = _b[1];
    var upHandler = function (_a) {
        var key = _a.key;
        var fn = {
            ArrowUp: setArrowUpPressed,
            ArrowDown: setArrowDownPressed
        }[key];
        if (fn)
            fn(false);
    };
    var downHandler = function (_a) {
        var key = _a.key;
        var fn = {
            ArrowUp: setArrowUpPressed,
            ArrowDown: setArrowDownPressed
        }[key];
        if (fn)
            fn(true);
    };
    react_1.useEffect(function () {
        window.addEventListener('keydown', downHandler);
        window.addEventListener('keyup', upHandler);
        return function () {
            window.removeEventListener('keydown', downHandler);
            window.removeEventListener('keyup', upHandler);
        };
    }, []);
    return [arrowUpPressed, arrowDownPressed];
};
exports.default = useKeyPress;
