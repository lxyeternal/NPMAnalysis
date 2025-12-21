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
var ebay_icon_1 = require("../ebay-icon");
var BreadcrumbItem = function (_a) {
    var _b = _a.tag, Item = _b === void 0 ? 'button' : _b, _c = _a.isLastItem, isLastItem = _c === void 0 ? false : _c, href = _a.href, children = _a.children, onClick = _a.onClick, rest = __rest(_a, ["tag", "isLastItem", "href", "children", "onClick"]);
    var isLink = Item === 'a';
    var itemAttr = __assign(__assign(__assign({}, rest), isLastItem ? { 'aria-current': 'location' } : {}), { href: isLink ? href : undefined, onClick: isLink ? undefined : onClick });
    return (react_1.default.createElement("li", null,
        react_1.default.createElement(Item, __assign({}, itemAttr), children),
        !isLastItem && react_1.default.createElement(ebay_icon_1.EbayIcon, { name: "breadcrumb", height: "8", width: "8" })));
};
exports.default = BreadcrumbItem;
