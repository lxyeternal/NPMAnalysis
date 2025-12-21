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
var forwardRef_1 = require("../common/component-utils/forwardRef");
var ebay_icon_1 = require("../ebay-icon");
var button_loading_1 = __importDefault(require("./button-loading"));
function isIconOnly(children) {
    var childrenArray = react_1.Children.toArray(children);
    return childrenArray.length === 1 && childrenArray[0].type === ebay_icon_1.EbayIcon;
}
var EbayButton = function (_a) {
    var _b, _c, _d, _e;
    var _f = _a.priority, priority = _f === void 0 ? 'secondary' : _f, _g = _a.size, size = _g === void 0 ? 'default' : _g, bodyState = _a.bodyState, _h = _a.transparent, transparent = _h === void 0 ? false : _h, _j = _a.fluid, fluid = _j === void 0 ? false : _j, disabled = _a.disabled, partiallyDisabled = _a.partiallyDisabled, children = _a.children, _k = _a.onEscape, onEscape = _k === void 0 ? function () { } : _k, _l = _a.truncate, truncate = _l === void 0 ? false : _l, href = _a.href, extraClasses = _a.className, forwardedRef = _a.forwardedRef, rest = __rest(_a, ["priority", "size", "bodyState", "transparent", "fluid", "disabled", "partiallyDisabled", "children", "onEscape", "truncate", "href", "className", "forwardedRef"]);
    var iconOnly = isIconOnly(children);
    var classPrefix = href ? 'fake-btn' : 'btn';
    var priorityStyles = {
        delete: classPrefix + "--delete",
        primary: classPrefix + "--primary",
        secondary: classPrefix + "--secondary",
        tertiary: classPrefix + "--tertiary",
        none: ''
    };
    var sizeStyles = {
        large: classPrefix + "--large",
        default: ''
    };
    var isLoading = bodyState === "loading";
    var className = classnames_1.default(classPrefix, extraClasses, priorityStyles[priority], sizeStyles[size], (_b = {}, _b[classPrefix + "--icon-only"] = iconOnly, _b), (_c = {}, _c[classPrefix + "--transparent"] = transparent, _c), (_d = {}, _d[classPrefix + "--fluid"] = fluid, _d), (_e = {}, _e[classPrefix + "--truncated"] = truncate, _e));
    var onKeyDown = function (e) {
        if (e.key === 'Escape' || e.key === 'Esc') {
            onEscape(e);
        }
    };
    var bodyContent = isLoading ? react_1.default.createElement(button_loading_1.default, null) : children;
    var ariaLive = isLoading ? "polite" : null;
    return href ? (react_1.default.createElement("a", __assign({ className: className, href: disabled ? undefined : href, ref: forwardedRef, onKeyDown: onKeyDown, "aria-live": ariaLive }, rest), bodyContent)) : (react_1.default.createElement("button", __assign({ disabled: disabled, "aria-disabled": partiallyDisabled, "aria-live": ariaLive, className: className, ref: forwardedRef, onKeyDown: onKeyDown }, rest), bodyContent));
};
exports.default = forwardRef_1.withForwardRef(EbayButton);
