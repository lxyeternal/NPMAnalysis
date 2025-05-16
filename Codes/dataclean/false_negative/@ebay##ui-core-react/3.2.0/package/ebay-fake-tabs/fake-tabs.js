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
var component_utils_1 = require("../common/component-utils");
var tab_1 = __importDefault(require("./tab"));
var EbayFakeTabs = function (_a) {
    var _b = _a.selectedIndex, selectedIndex = _b === void 0 ? 0 : _b, tabMatchesCurrentUrl = _a.tabMatchesCurrentUrl, className = _a.className, children = _a.children, rest = __rest(_a, ["selectedIndex", "tabMatchesCurrentUrl", "className", "children"]);
    var ariaCurrent = tabMatchesCurrentUrl === false ? 'true' : 'page';
    var tabHeadings = component_utils_1.filterByType(children, tab_1.default).map(function (item, i) {
        return react_1.cloneElement(item, __assign(__assign({}, item.props), { ariaCurrent: selectedIndex === i ? ariaCurrent : null }));
    });
    var tabContent = component_utils_1.excludeComponent(children, tab_1.default);
    return (react_1.default.createElement("div", __assign({}, rest, { className: classnames_1.default(className, 'fake-tabs') }),
        react_1.default.createElement("ul", { className: "fake-tabs__items" }, tabHeadings),
        react_1.default.createElement("div", { className: "fake-tabs__content" },
            react_1.default.createElement("div", { className: "fake-tabs__cell" }, tabContent))));
};
exports.default = EbayFakeTabs;
