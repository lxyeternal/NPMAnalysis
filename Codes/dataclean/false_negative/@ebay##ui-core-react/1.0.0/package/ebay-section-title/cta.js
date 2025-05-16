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
var ebay_icon_1 = require("../ebay-icon");
var Cta = function (_a) {
    var ctaText = _a.ctaText, href = _a.href, _b = _a.icon, icon = _b === void 0 ? 'arrowRightBold' : _b, rest = __rest(_a, ["ctaText", "href", "icon"]);
    var className = classnames_1.default('section-title__cta', {
        'section-title__cta--no-text': !ctaText
    });
    return (react_1.default.createElement("div", __assign({}, rest, { className: className }),
        react_1.default.createElement("a", { href: href, tabIndex: -1, "aria-hidden": "true" },
            ctaText && react_1.default.createElement("span", { className: "section-title__cta-text" }, ctaText),
            react_1.default.createElement(ebay_icon_1.EbayIcon, { name: icon, className: "section-title__cta-icon", noSkinClasses: true, height: "24", width: "24", "aria-hidden": "true" }))));
};
exports.default = Cta;
