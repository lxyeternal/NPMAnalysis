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
var EbayRadio = function (_a) {
    var _b = _a.size, size = _b === void 0 ? 'default' : _b, checked = _a.checked, defaultChecked = _a.defaultChecked, className = _a.className, style = _a.style, id = _a.id, _c = _a.onChange, onChange = _c === void 0 ? function () { } : _c, children = _a.children, rest = __rest(_a, ["size", "checked", "defaultChecked", "className", "style", "id", "onChange", "children"]);
    var handleChange = function (e) {
        var input = e.target;
        onChange(e, input === null || input === void 0 ? void 0 : input.value);
    };
    var containerClass = classnames_1.default('radio', className, { 'radio--large': size === 'large' });
    var iconChecked = size === 'large' ?
        react_1.default.createElement(ebay_icon_1.EbayIcon, { name: "radioCheckedLarge", className: "radio__checked" }) :
        react_1.default.createElement(ebay_icon_1.EbayIcon, { name: "radioChecked", className: "radio__checked" });
    var iconUnChecked = size === 'large' ?
        react_1.default.createElement(ebay_icon_1.EbayIcon, { name: "radioUncheckedLarge", className: "radio__unchecked" }) :
        react_1.default.createElement(ebay_icon_1.EbayIcon, { name: "radioUnchecked", className: "radio__unchecked" });
    var childrenArray = react_1.Children.toArray(children);
    var ebayLabel = childrenArray.find(function (child) { return child.type === ebay_field_1.EbayLabel; });
    return (react_1.default.createElement(react_1.default.Fragment, null,
        react_1.default.createElement("span", { className: containerClass, style: __assign(__assign({}, style), { alignItems: 'center' }) },
            react_1.default.createElement("input", __assign({}, rest, { id: id, className: "radio__control", type: "radio", defaultChecked: defaultChecked, checked: checked, onChange: handleChange })),
            react_1.default.createElement("span", { className: "radio__icon", hidden: true },
                iconChecked,
                iconUnChecked)),
        ebayLabel ?
            react_1.cloneElement(ebayLabel, __assign(__assign({}, ebayLabel.props), { position: 'end', htmlFor: id })) :
            children));
};
exports.default = EbayRadio;
