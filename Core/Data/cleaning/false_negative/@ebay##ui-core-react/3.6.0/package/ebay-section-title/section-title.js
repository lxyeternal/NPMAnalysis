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
var component_utils_1 = require("../common/component-utils");
var index_1 = require("./index");
var cta_1 = __importDefault(require("./cta"));
var EbaySectionTitle = function (_a) {
    var href = _a.href, ctaText = _a.ctaText, className = _a.className, children = _a.children, rest = __rest(_a, ["href", "ctaText", "className", "children"]);
    var sectionTitleClass = classnames_1.default(className, 'section-title');
    var title = component_utils_1.findComponent(children, index_1.EbaySectionTitleTitle);
    var subtitle = component_utils_1.findComponent(children, index_1.EbaySectionTitleSubtitle);
    var info = component_utils_1.findComponent(children, index_1.EbaySectionTitleInfo);
    var overflow = component_utils_1.findComponent(children, index_1.EbaySectionTitleOverflow);
    return (react_1.default.createElement("div", __assign({}, rest, { className: sectionTitleClass }),
        react_1.default.createElement("div", { className: "section-title__title-container" },
            title || react_1.default.createElement(index_1.EbaySectionTitleTitle, null, children),
            subtitle),
        href && react_1.default.createElement(cta_1.default, { href: href, ctaText: ctaText }) || info || overflow));
};
exports.default = EbaySectionTitle;
