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
var EbayFakeMenu = function (_a) {
    var className = _a.className, _b = _a.itemMatchesUrl, itemMatchesUrl = _b === void 0 ? true : _b, _c = _a.onKeyDown, onKeyDown = _c === void 0 ? function () { } : _c, _d = _a.onSelect, onSelect = _d === void 0 ? function () { } : _d, children = _a.children, rest = __rest(_a, ["className", "itemMatchesUrl", "onKeyDown", "onSelect", "children"]);
    var childrenArray = react_1.Children.toArray(children);
    var defaultAriaCurrent = itemMatchesUrl === false ? 'true' : 'page';
    return (react_1.default.createElement("div", __assign({}, rest, { className: classnames_1.default(className, 'fake-menu') }),
        react_1.default.createElement("ul", { className: "fake-menu__items", tabIndex: -1 }, childrenArray.map(function (child, i) {
            var _a = child.props, current = _a.current, _b = _a.onClick, onClick = _b === void 0 ? function () { } : _b, itemRest = __rest(_a, ["current", "onClick"]);
            return (react_1.default.createElement("li", { key: i }, react_1.cloneElement(child, __assign(__assign({}, itemRest), { 'aria-current': current ? defaultAriaCurrent : undefined, onClick: function (e) {
                    onSelect(e, i);
                    onClick(e);
                }, onKeyDown: function (e) {
                    onKeyDown(e, i);
                } }))));
        }))));
};
exports.default = EbayFakeMenu;
