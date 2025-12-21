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
var ebay_badge_1 = require("../ebay-badge");
var ebay_icon_1 = require("../ebay-icon");
var EbayMenuItem = function (_a) {
    var className = _a.className, checked = _a.checked, _b = _a.focused, focused = _b === void 0 ? false : _b, tabIndex = _a.tabIndex, disabled = _a.disabled, badgeNumber = _a.badgeNumber, children = _a.children, rest = __rest(_a, ["className", "checked", "focused", "tabIndex", "disabled", "badgeNumber", "children"]);
    var ref = react_1.useRef(null);
    react_1.useEffect(function () {
        if (ref.current && focused) {
            ref.current.focus();
        }
    }, [ref, focused]);
    return (react_1.default.createElement("div", __assign({}, rest, { ref: ref, className: classnames_1.default(className, 'menu__item'), role: "menuitem", "aria-checked": checked, "aria-disabled": disabled, "aria-hidden": badgeNumber !== undefined, tabIndex: focused ? 0 : tabIndex }),
        react_1.default.createElement("span", null,
            children,
            badgeNumber !== undefined && react_1.default.createElement(ebay_badge_1.EbayBadge, { type: "menu", number: badgeNumber })),
        react_1.default.createElement(ebay_icon_1.EbayIcon, { name: "tickSmall" })));
};
exports.default = EbayMenuItem;
