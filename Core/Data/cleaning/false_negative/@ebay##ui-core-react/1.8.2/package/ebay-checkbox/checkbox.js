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
var ebay_icon_1 = require("../ebay-icon");
var ebay_field_1 = require("../ebay-field");
var component_utils_1 = require("../common/component-utils");
var isControlled = function (checked) { return typeof checked !== 'undefined'; };
var EbayCheckbox = function (_a) {
    var id = _a.id, _b = _a.size, size = _b === void 0 ? 'default' : _b, className = _a.className, style = _a.style, checked = _a.checked, _c = _a.defaultChecked, defaultChecked = _c === void 0 ? false : _c, _d = _a.onChange, onChange = _d === void 0 ? function () { } : _d, children = _a.children, inputRef = _a.inputRef, rest = __rest(_a, ["id", "size", "className", "style", "checked", "defaultChecked", "onChange", "children", "inputRef"]);
    var _e = react_1.useState(defaultChecked), isChecked = _e[0], setChecked = _e[1];
    var handleChange = function (e) {
        var input = e.target;
        onChange(e, input === null || input === void 0 ? void 0 : input.value, input === null || input === void 0 ? void 0 : input.checked);
        setChecked(input === null || input === void 0 ? void 0 : input.checked);
    };
    var containerClass = classnames_1.default('checkbox', className, { 'checkbox--large': size === 'large' });
    var iconChecked = size === 'large' ?
        react_1.default.createElement(ebay_icon_1.EbayIcon, { name: "checkboxCheckedLarge", className: "checkbox__checked" }) :
        react_1.default.createElement(ebay_icon_1.EbayIcon, { name: "checkboxChecked", className: "checkbox__checked" });
    var iconUnChecked = size === 'large' ?
        react_1.default.createElement(ebay_icon_1.EbayIcon, { name: "checkboxUncheckedLarge", className: "checkbox__unchecked" }) :
        react_1.default.createElement(ebay_icon_1.EbayIcon, { name: "checkboxUnchecked", className: "checkbox__unchecked" });
    var ebayLabel = component_utils_1.findComponent(children, ebay_field_1.EbayLabel);
    return (react_1.default.createElement(react_1.default.Fragment, null,
        react_1.default.createElement("span", { className: containerClass, style: __assign(__assign({}, style), { alignItems: 'center' }) },
            react_1.default.createElement("input", __assign({}, rest, { id: id, className: "checkbox__control", type: "checkbox", checked: isControlled(checked) ? checked : isChecked, onChange: handleChange, ref: inputRef })),
            react_1.default.createElement("span", { className: "checkbox__icon", hidden: true },
                iconChecked,
                iconUnChecked)),
        ebayLabel ?
            react_1.cloneElement(ebayLabel, __assign(__assign({}, ebayLabel.props), { position: 'end', htmlFor: id })) :
            children));
};
exports.default = EbayCheckbox;
