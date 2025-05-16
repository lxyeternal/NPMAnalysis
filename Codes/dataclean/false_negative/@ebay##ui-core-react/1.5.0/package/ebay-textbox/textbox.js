"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
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
var __rest = (this && this.__rest) || function (s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
            if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i]))
                t[p[i]] = s[p[i]];
        }
    return t;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = __importStar(require("react"));
var classnames_1 = __importDefault(require("classnames"));
var component_utils_1 = require("../common/component-utils");
var index_1 = require("./index");
var hooks_1 = require("../ebay-floating-label/hooks");
var isControlled = function (value) { return typeof value !== 'undefined'; };
var EbayTextbox = function (_a) {
    var _b = _a.type, type = _b === void 0 ? 'text' : _b, invalid = _a.invalid, fluid = _a.fluid, multiline = _a.multiline, underline = _a.underline /* DEPRECATED */, _c = _a.onChange, onChange = _c === void 0 ? function () { } : _c, _d = _a.onFocus, onFocus = _d === void 0 ? function () { } : _d, _e = _a.onBlur, onBlur = _e === void 0 ? function () { } : _e, _f = _a.onButtonClick, onButtonClick = _f === void 0 ? function () { } : _f, autoFocus = _a.autoFocus, _g = _a.defaultValue, defaultValue = _g === void 0 ? '' : _g, controlledValue = _a.value, forwardedRef = _a.forwardedRef, _h = _a.inputSize, inputSize = _h === void 0 ? 'default' : _h, floatingLabel = _a.floatingLabel, children = _a.children, placeholder = _a.placeholder, rest = __rest(_a, ["type", "invalid", "fluid", "multiline", "underline", "onChange", "onFocus", "onBlur", "onButtonClick", "autoFocus", "defaultValue", "value", "forwardedRef", "inputSize", "floatingLabel", "children", "placeholder"]);
    var _j = react_1.useState(defaultValue), value = _j[0], setValue = _j[1];
    var _k = hooks_1.useFloatingLabel({
        ref: forwardedRef,
        inputId: rest.id,
        className: rest.className,
        disabled: rest.disabled,
        label: floatingLabel,
        inputSize: inputSize,
        inputValue: controlledValue,
        placeholder: placeholder,
        invalid: invalid
    }), label = _k.label, Container = _k.Container, onFloatingLabelBlur = _k.onBlur, onFloatingLabelFocus = _k.onFocus, ref = _k.ref, floatingLabelPlaceholder = _k.placeholder;
    var handleFocus = function (event) {
        onFocus(event);
        onFloatingLabelFocus();
    };
    var handleBlur = function (event) {
        onBlur(event);
        onFloatingLabelBlur();
    };
    react_1.useEffect(function () {
        if (autoFocus) {
            handleFocus();
        }
    }, []);
    var onChangeHandler = function (e) {
        var newValue = e.target.value;
        if (!isControlled(controlledValue)) {
            setValue(newValue);
        }
        onChange(e, newValue);
    };
    var Input = multiline ? 'textarea' : 'input';
    var Wrapper = fluid ? 'div' : 'span';
    var prefixIcon = component_utils_1.findComponent(children, index_1.EbayTextboxPrefixIcon);
    var postfixIcon = component_utils_1.findComponent(children, index_1.EbayTextboxPostfixIcon);
    var inputClassName = classnames_1.default('textbox__control', {
        'textbox__control--fluid': fluid,
        'legacy-textbox-underline': underline,
        'textbox__control--large': inputSize === 'large'
    });
    var wrapperClassName = classnames_1.default('textbox', {
        'textbox--icon-end': postfixIcon
    });
    return (react_1.default.createElement(Container, null,
        label,
        react_1.default.createElement(Wrapper, { className: wrapperClassName },
            prefixIcon,
            react_1.default.createElement(Input, __assign({}, rest, { className: inputClassName, type: type, "aria-invalid": invalid, value: isControlled(controlledValue) ? controlledValue : value, onChange: onChangeHandler, onBlur: handleBlur, onFocus: handleFocus, autoFocus: autoFocus, ref: ref, placeholder: floatingLabelPlaceholder })),
            postfixIcon && react_1.cloneElement(postfixIcon, __assign({ onClick: onButtonClick }, postfixIcon.props)))));
};
exports.default = component_utils_1.withForwardRef(EbayTextbox);
