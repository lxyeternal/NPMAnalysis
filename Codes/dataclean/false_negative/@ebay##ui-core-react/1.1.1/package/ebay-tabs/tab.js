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
var Tab = function (_a) {
    var children = _a.children, index = _a.index, selected = _a.selected, href = _a.href, className = _a.className, refCallback = _a.refCallback, _b = _a.onClick, onClick = _b === void 0 ? function () { } : _b, _c = _a.onKeyDown, onKeyDown = _c === void 0 ? function () { } : _c, rest = __rest(_a, ["children", "index", "selected", "href", "className", "refCallback", "onClick", "onKeyDown"]);
    return href ? (react_1.default.createElement("li", __assign({}, rest, { className: classnames_1.default(className, 'fake-tabs__item', { 'fake-tabs__item--current': selected }) }),
        react_1.default.createElement("a", { href: href, "aria-current": selected ? "page" : null }, children))) : (react_1.default.createElement("div", __assign({}, rest, { ref: refCallback, "aria-controls": "default-tabpanel-" + index, "aria-selected": selected, className: classnames_1.default(className, 'tabs__item'), id: "default-tab-" + index, role: "tab", tabIndex: selected ? 0 : -1, onClick: onClick, onKeyDown: onKeyDown }),
        react_1.default.createElement("span", null, children)));
};
exports.default = Tab;
