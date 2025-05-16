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
var ebay_icon_1 = require("../ebay-icon");
var button_loading_1 = __importDefault(require("./button-loading"));
var button_expand_1 = __importDefault(require("./button-expand"));
var EbayButton = function (_a) {
    var _b = _a.priority, priority = _b === void 0 ? 'secondary' : _b, _c = _a.variant, variant = _c === void 0 ? 'standard' : _c, _d = _a.size, size = _d === void 0 ? 'regular' : _d, bodyState = _a.bodyState, split = _a.split, _e = _a.transparent, transparent = _e === void 0 ? false : _e, _f = _a.fluid, fluid = _f === void 0 ? false : _f, disabled = _a.disabled, partiallyDisabled = _a.partiallyDisabled, children = _a.children, _g = _a.onEscape, onEscape = _g === void 0 ? function () { } : _g, _h = _a.truncate, truncate = _h === void 0 ? false : _h, href = _a.href, extraClasses = _a.className, forwardedRef = _a.forwardedRef, borderless = _a.borderless, fixedHeight = _a.fixedHeight, rest = __rest(_a, ["priority", "variant", "size", "bodyState", "split", "transparent", "fluid", "disabled", "partiallyDisabled", "children", "onEscape", "truncate", "href", "className", "forwardedRef", "borderless", "fixedHeight"]);
    var classPrefix = href ? 'fake-btn' : 'btn';
    var priorityStyles = {
        primary: classPrefix + "--primary",
        secondary: classPrefix + "--secondary",
        tertiary: classPrefix + "--tertiary",
        none: ''
    };
    var sizeStyles = {
        large: classPrefix + "--large",
        regular: '',
        default: ''
    };
    var splitStyles = {
        start: classPrefix + "--split-start",
        end: classPrefix + "--split-end"
    };
    var isDestructive = variant === 'destructive';
    var isForm = variant === 'form';
    var isLoading = bodyState === 'loading';
    var isExpand = bodyState === 'expand';
    var isSlim = isForm && (isIconOnly(children) || (isExpand && !children));
    var className = classnames_1.default(classPrefix, extraClasses, priorityStyles[isForm || borderless ? 'none' : priority], sizeStyles[size], splitStyles[split], isDestructive && classPrefix + "--destructive", isForm && classPrefix + "--form", isSlim && classPrefix + "--slim", transparent && classPrefix + "--transparent", fluid && classPrefix + "--fluid", truncate && classPrefix + "--truncated", borderless && classPrefix + "--borderless", fixedHeight && (sizeStyles[size] ? sizeStyles[size] + "-" + fixedHeight : classPrefix + "--fixed-height"));
    var onKeyDown = function (e) {
        if (e.key === 'Escape' || e.key === 'Esc') {
            onEscape(e);
        }
    };
    var bodyContent = getBodyContent(children, { isLoading: isLoading, isExpand: isExpand });
    var ariaLive = isLoading ? "polite" : null;
    return href ? (react_1.default.createElement("a", __assign({ className: className, href: disabled ? undefined : href, ref: forwardedRef, onKeyDown: onKeyDown, "aria-live": ariaLive }, rest), bodyContent)) : (react_1.default.createElement("button", __assign({ disabled: disabled, "aria-disabled": partiallyDisabled, "aria-live": ariaLive, className: className, ref: forwardedRef, onKeyDown: onKeyDown }, rest), bodyContent));
};
function getBodyContent(children, _a) {
    var isLoading = _a.isLoading, isExpand = _a.isExpand;
    switch (true) {
        case isLoading:
            return react_1.default.createElement(button_loading_1.default, null);
        case isExpand:
            return react_1.default.createElement(button_expand_1.default, null, children);
        default:
            return children;
    }
}
function isIconOnly(children) {
    var childrenArray = react_1.Children.toArray(children);
    return childrenArray.length === 1 && childrenArray[0].type === ebay_icon_1.EbayIcon;
}
exports.default = component_utils_1.withForwardRef(EbayButton);
