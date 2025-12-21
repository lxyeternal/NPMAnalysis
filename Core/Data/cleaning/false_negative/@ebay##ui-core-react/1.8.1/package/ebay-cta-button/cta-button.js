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
var classnames_1 = __importDefault(require("classnames"));
var forwardRef_1 = require("../common/component-utils/forwardRef");
var ebay_icon_1 = require("../ebay-icon");
var ebay_button_1 = require("../ebay-button");
var EbayCtaButton = function (_a) {
    var size = _a.size, children = _a.children, fluid = _a.fluid, truncate = _a.truncate, forwardedRef = _a.forwardedRef, extraClasses = _a.className, rest = __rest(_a, ["size", "children", "fluid", "truncate", "forwardedRef", "className"]);
    var className = classnames_1.default(extraClasses, 'cta-btn', { 'cta-btn--large': size === 'large' }, { 'cta-btn--fluid': fluid }, { 'cta-btn--truncated': truncate });
    return (react_1.default.createElement("a", __assign({}, rest, { className: className, ref: forwardedRef }),
        react_1.default.createElement(ebay_button_1.EbayButtonCell, { type: "cta" },
            react_1.default.createElement("span", null, children),
            react_1.default.createElement(ebay_icon_1.EbayIcon, { name: "cta", width: 8, height: 8 }))));
};
exports.default = forwardRef_1.withForwardRef(EbayCtaButton);
