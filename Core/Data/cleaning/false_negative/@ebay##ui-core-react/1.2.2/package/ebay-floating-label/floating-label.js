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
var react_1 = __importDefault(require("react"));
var ebay_textbox_1 = require("../ebay-textbox");
var component_utils_1 = require("../common/component-utils");
var ebay_select_1 = require("../ebay-select");
var EbayFloatingLabel = function (_a) {
    var label = _a.label, forwardedRef = _a.forwardedRef, _b = _a.elementType, elementType = _b === void 0 ? 'textbox' : _b, rest = __rest(_a, ["label", "forwardedRef", "elementType"]);
    var inputRef = function () { return forwardedRef; };
    if (elementType === 'select') {
        return (react_1.default.createElement(ebay_select_1.EbaySelect, __assign({}, rest, { floatingLabel: label })));
    }
    return (react_1.default.createElement(ebay_textbox_1.EbayTextbox, __assign({}, rest, { ref: inputRef(), floatingLabel: label })));
};
exports.default = component_utils_1.withForwardRef(EbayFloatingLabel);
