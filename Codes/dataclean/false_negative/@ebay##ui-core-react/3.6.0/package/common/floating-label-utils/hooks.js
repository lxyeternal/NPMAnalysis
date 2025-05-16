"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.useFloatingLabel = void 0;
var react_1 = __importStar(require("react"));
var classnames_1 = __importDefault(require("classnames"));
var classPrefix = 'floating-label__label';
// input background in Skin 12, used for autofill detection
var textboxElementBackgroundRGB = [
    'rgb(245, 245, 245)',
    'rgb(247, 247, 247)' // From skin version 12.6.0
];
// check for computed background color because of Chrome autofill bug
// https://stackoverflow.com/questions/35049555/chrome-autofill-autocomplete-no-value-for-password/35783761#35783761
var isAutofilled = function (input) {
    return input && !textboxElementBackgroundRGB.includes(getComputedStyle(input).backgroundColor);
};
var hasValue = function (input) { var _a; return ((_a = input === null || input === void 0 ? void 0 : input.value) === null || _a === void 0 ? void 0 : _a.length) > 0; };
var isSelect = function (element) { return (element === null || element === void 0 ? void 0 : element.tagName) === "SELECT"; };
var setPlaceholder = function (element, value) {
    // For select elements we need to temporary remove the text of the first option
    // when the element is not focused, so only the label is shown. We still need to
    // maintain the width of the input so we manually change the "min-width"
    // Inspired by the marko implementation: https://github.com/makeup/makeup-js/blob/master/packages/makeup-floating-label/src/index.js
    if (isSelect(element) && !hasValue(element.querySelector("option"))) {
        element.style['min-width'] = '';
        var beforeWidth = element.offsetWidth;
        element.querySelector("option").text = value;
        if (!value && beforeWidth > element.offsetWidth) {
            element.style['min-width'] = beforeWidth + "px";
        }
    }
};
var getPlaceholder = function (element) {
    if (isSelect(element)) {
        return element.querySelector("option").text;
    }
    return element === null || element === void 0 ? void 0 : element.placeholder;
};
function useFloatingLabel(_a) {
    var _b;
    var ref = _a.ref, inputId = _a.inputId, className = _a.className, disabled = _a.disabled, label = _a.label, inputSize = _a.inputSize, inputValue = _a.inputValue, placeholder = _a.placeholder, invalid = _a.invalid;
    var _internalInputRef = react_1.useRef(null);
    var inputRef = function () { return ref || _internalInputRef; };
    var _c = react_1.useState(Boolean(inputValue)), isFloating = _c[0], setFloating = _c[1];
    var _d = react_1.useState(false), shouldAnimate = _d[0], setAnimate = _d[1];
    var _e = react_1.useState(false), isFocused = _e[0], setFocused = _e[1];
    var selectFirstOptionText = react_1.useRef("");
    var onBlur = function () {
        setAnimate(true);
        setFloating(false);
        setFocused(false);
        setPlaceholder(inputRef().current, "");
    };
    var onFocus = function () {
        var _a;
        setAnimate(true);
        setFloating(true);
        setFocused(true);
        setPlaceholder((_a = inputRef()) === null || _a === void 0 ? void 0 : _a.current, selectFirstOptionText.current);
    };
    react_1.useEffect(function () {
        var _a, _b;
        if (!label) {
            return;
        }
        selectFirstOptionText.current = getPlaceholder((_a = inputRef()) === null || _a === void 0 ? void 0 : _a.current);
        setPlaceholder((_b = inputRef()) === null || _b === void 0 ? void 0 : _b.current, "");
    }, []);
    react_1.useEffect(function () {
        var _a, _b;
        if (!label) {
            return;
        }
        setFloating(isFocused || hasValue((_a = inputRef()) === null || _a === void 0 ? void 0 : _a.current) || isAutofilled((_b = inputRef()) === null || _b === void 0 ? void 0 : _b.current));
    }, [isFocused, inputValue]);
    var labelClassName = classnames_1.default(className, classPrefix, (_b = {},
        _b[classPrefix + "--disabled"] = disabled,
        _b[classPrefix + "--animate"] = shouldAnimate,
        _b[classPrefix + "--inline"] = !isFloating,
        _b[classPrefix + "--invalid"] = invalid,
        _b));
    var floatingLabelClassName = classnames_1.default("floating-label", {
        'floating-label--large': inputSize === "large"
    });
    var FragmentContainer = react_1.useCallback(function (_a) {
        var children = _a.children;
        return react_1.default.createElement(react_1.default.Fragment, null, children);
    }, []);
    var FloatingLabelContainer = react_1.useCallback(function (_a) {
        var children = _a.children;
        return react_1.default.createElement("span", { className: floatingLabelClassName }, children);
    }, [floatingLabelClassName]);
    if (!label) {
        return {
            label: null,
            Container: FragmentContainer,
            onBlur: function () { },
            onFocus: function () { },
            ref: inputRef(),
            placeholder: placeholder
        };
    }
    var labelElement = react_1.default.createElement("label", { htmlFor: inputId, className: labelClassName }, label);
    return {
        label: labelElement,
        Container: FloatingLabelContainer,
        onBlur: onBlur,
        onFocus: onFocus,
        ref: inputRef(),
        placeholder: !isFloating ? null : placeholder
    };
}
exports.useFloatingLabel = useFloatingLabel;
