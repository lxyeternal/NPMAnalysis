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
var ebay_textbox_1 = require("../ebay-textbox");
var forwardRef_1 = require("../common/component-utils/forwardRef");
var textboxElementBackgroundRGB = 'rgb(255, 255, 255)';
var hasValue = function (input) { var _a; return ((_a = input === null || input === void 0 ? void 0 : input.value) === null || _a === void 0 ? void 0 : _a.length) > 0; };
// check for computed background color because of Chrome autofill bug
// https://stackoverflow.com/questions/35049555/chrome-autofill-autocomplete-no-value-for-password/35783761#35783761
var isAutofilled = function (input) { return getComputedStyle(input).backgroundColor !== textboxElementBackgroundRGB; };
var EbayLegacyFloatingLabel = function (_a) {
    var defaultValue = _a.defaultValue, id = _a.id, disabled = _a.disabled, label = _a.label, onBlur = _a.onBlur, onFocus = _a.onFocus, forwardedRef = _a.forwardedRef, rest = __rest(_a, ["defaultValue", "id", "disabled", "label", "onBlur", "onFocus", "forwardedRef"]);
    var _internalInputRef = react_1.useRef(null);
    var inputRef = function () { return forwardedRef || _internalInputRef; };
    var _b = react_1.useState(true), isFloating = _b[0], setFloating = _b[1];
    var _c = react_1.useState(false), shouldAnimate = _c[0], setAnimate = _c[1];
    var _d = react_1.useState(false), isFocused = _d[0], setFocused = _d[1];
    var onBlurHandler = function (e, value) {
        if (!hasValue(e.target)) {
            setAnimate(true);
            setFloating(false);
        }
        if (onBlur) {
            onBlur(e, value);
        }
        setFocused(false);
    };
    var onFocusHandler = function (e, value) {
        setAnimate(true);
        setFloating(true);
        if (onFocus) {
            onFocus(e, value);
        }
        setFocused(true);
    };
    react_1.useEffect(function () {
        setFloating(isFocused || hasValue(inputRef().current) || isAutofilled(inputRef().current));
    }, [isFocused, rest.value]);
    var labelClassName = classnames_1.default('legacy-floating-label__label', disabled && 'legacy-floating-label__label--disabled', shouldAnimate && 'legacy-floating-label__label--animate', !isFloating && 'legacy-floating-label__label--inline');
    var inputAttributes = __assign(__assign({}, rest), { defaultValue: defaultValue ? String(defaultValue) : undefined, id: id,
        disabled: disabled, ref: inputRef(), onFocus: onFocusHandler, onBlur: onBlurHandler });
    return (react_1.default.createElement("span", { className: "legacy-floating-label" },
        react_1.default.createElement("label", { htmlFor: id, className: labelClassName }, label),
        react_1.default.createElement(ebay_textbox_1.EbayTextbox, __assign({}, inputAttributes, { underline: true }))));
};
exports.default = forwardRef_1.withForwardRef(EbayLegacyFloatingLabel);
