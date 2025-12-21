"use strict";
var __spreadArrays = (this && this.__spreadArrays) || function () {
    for (var s = 0, i = 0, il = arguments.length; i < il; i++) s += arguments[i].length;
    for (var r = Array(s), k = 0, i = 0; i < il; i++)
        for (var a = arguments[i], j = 0, jl = a.length; j < jl; j++, k++)
            r[k] = a[j];
    return r;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var use_key_press_1 = __importDefault(require("./use-key-press"));
var useRovingIndex = function (children, FocusableType, defaultValue) {
    var _a = react_1.useState(defaultValue), rovingIndex = _a[0], setRovingIndex = _a[1];
    var _b = use_key_press_1.default(), arrowUpPressed = _b[0], arrowDownPressed = _b[1];
    var rovingIndexArray = react_1.Children
        .toArray(children)
        .reduce(function (focusables, child, i) {
        return child.type === FocusableType ? __spreadArrays(focusables, [i]) : focusables;
    }, []);
    var currentIndex = rovingIndexArray.indexOf(rovingIndex);
    var previousOrCurrent = function () {
        if (currentIndex === -1)
            return rovingIndex;
        var previousRovingIndex = rovingIndexArray[currentIndex - 1];
        return previousRovingIndex === undefined ? rovingIndex : previousRovingIndex;
    };
    var nextOrCurrent = function () {
        if (currentIndex === -1)
            return rovingIndex;
        var nextRovingIndex = rovingIndexArray[currentIndex + 1];
        return nextRovingIndex === undefined ? rovingIndex : nextRovingIndex;
    };
    react_1.useEffect(function () {
        if (arrowUpPressed)
            setRovingIndex(previousOrCurrent());
        if (arrowDownPressed)
            setRovingIndex(nextOrCurrent());
    }, [arrowUpPressed, arrowDownPressed]);
    return [rovingIndex, setRovingIndex];
};
exports.default = useRovingIndex;
