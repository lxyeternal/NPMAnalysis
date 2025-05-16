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
var Breadcrumbs = function (_a) {
    var _b = _a.a11yHeadingText, a11yHeadingText = _b === void 0 ? 'Page navigation' : _b, _c = _a.a11yHeadingTag, a11yHeadingTag = _c === void 0 ? 'h2' : _c, _d = _a.id, id = _d === void 0 ? 'ebay-breadcrumb' : _d, _e = _a.children, breadcrumbItems = _e === void 0 ? [] : _e, className = _a.className, _f = _a.onSelect, onSelect = _f === void 0 ? function () { } : _f, rest = __rest(_a, ["a11yHeadingText", "a11yHeadingTag", "id", "children", "className", "onSelect"]);
    var headingId = id + "-breadcrumbs-heading";
    var lastItemIndex = react_1.Children.count(breadcrumbItems) - 1;
    var A11yHeadingTag = a11yHeadingTag;
    var anyLink = react_1.Children.toArray(breadcrumbItems).some(function (item) { return item.props.href; });
    var tag = anyLink ? 'a' : 'button';
    return (react_1.default.createElement("nav", __assign({}, rest, { "aria-labelledby": headingId, className: classnames_1.default('breadcrumbs', className), role: "navigation" }),
        react_1.default.createElement(A11yHeadingTag, { id: headingId, className: "clipped" }, a11yHeadingText),
        react_1.default.createElement("ul", null, react_1.Children.map(breadcrumbItems, function (item, index) {
            var isLastItem = index === lastItemIndex;
            var _a = item.props, href = _a.href, children = _a.children;
            var itemProps = {
                tag: tag,
                isLastItem: isLastItem,
                href: href,
                children: children,
                onClick: function (event) { return onSelect(event, event.target); }
            };
            return react_1.cloneElement(item, itemProps);
        }))));
};
exports.default = Breadcrumbs;
