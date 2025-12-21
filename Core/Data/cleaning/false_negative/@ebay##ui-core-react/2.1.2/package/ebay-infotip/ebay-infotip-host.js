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
var dedupe_1 = __importDefault(require("classnames/dedupe"));
var ebay_icon_1 = require("../ebay-icon");
var forwardRef_1 = require("../common/component-utils/forwardRef");
var EbayInfotipHost = function (_a) {
    var icon = _a.icon, className = _a.className, children = _a.children, forwardedRef = _a.forwardedRef, variant = _a.variant, rest = __rest(_a, ["icon", "className", "children", "forwardedRef", "variant"]);
    var classPrefix = variant === 'modal' ? 'dialog--mini' : 'infotip';
    var buttonIcon = react_1.default.createElement(ebay_icon_1.EbayIcon, { name: icon });
    var buttonContent = typeof children === 'function' ? children({ icon: buttonIcon }) : children;
    return (react_1.default.createElement("button", __assign({}, rest, { className: dedupe_1.default('icon-btn icon-btn--transparent', className, classPrefix + "__host"), type: "button", ref: forwardedRef }), buttonContent || buttonIcon));
};
exports.default = forwardRef_1.withForwardRef(EbayInfotipHost);
