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
var ebay_badge_1 = require("../ebay-badge");
var EbayIconButton = function (_a) {
    var _b;
    var href = _a.href, icon = _a.icon, badgeNumber = _a.badgeNumber, badgeAriaLabel = _a.badgeAriaLabel, transparent = _a.transparent, extraClasses = _a.className, rest = __rest(_a, ["href", "icon", "badgeNumber", "badgeAriaLabel", "transparent", "className"]);
    var classPrefix = href ? 'icon-link' : 'icon-btn';
    var className = classnames_1.default(extraClasses, classPrefix, (_b = {},
        _b[classPrefix + "--badged"] = badgeNumber,
        _b[classPrefix + "--transparent"] = transparent,
        _b));
    var children = (react_1.default.createElement(react_1.default.Fragment, null,
        react_1.default.createElement(ebay_icon_1.EbayIcon, { name: icon }),
        badgeNumber && react_1.default.createElement(ebay_badge_1.EbayBadge, { type: "icon", number: badgeNumber, "aria-label": badgeAriaLabel })));
    return href ? (react_1.default.createElement("a", __assign({ className: className, href: href }, rest), children)) : (react_1.default.createElement("button", __assign({ type: "button", className: className }, rest), children));
};
exports.default = EbayIconButton;
