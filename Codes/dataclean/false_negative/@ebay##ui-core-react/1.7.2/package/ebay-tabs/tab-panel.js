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
var TabPanel = function (_a) {
    var children = _a.children, index = _a.index, parentId = _a.parentId, selected = _a.selected, fake = _a.fake, className = _a.className, rest = __rest(_a, ["children", "index", "parentId", "selected", "fake", "className"]);
    return fake ? (react_1.default.createElement("div", __assign({}, rest, { className: classnames_1.default(className, 'fake-tabs__cell') }), children)) : (react_1.default.createElement("div", __assign({}, rest, { "aria-labelledby": "default-tab-" + index, className: classnames_1.default(className, 'tabs__panel'), id: (parentId || 'default') + "-tabpanel-" + index, role: "tabpanel", hidden: !selected }),
        react_1.default.createElement("div", { className: "tabs__cell" }, children)));
};
exports.default = TabPanel;
