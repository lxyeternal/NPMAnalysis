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
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = __importStar(require("react"));
var component_utils_1 = require("../common/component-utils");
var helpers_1 = require("./helpers");
var EbayCarouselItem = function (_a) {
    var slideWidth = _a.slideWidth, offset = _a.offset, forwardedRef = _a.forwardedRef, children = _a.children, rest = __rest(_a, ["slideWidth", "offset", "forwardedRef", "children"]);
    var itemRef = react_1.useRef();
    var _b = react_1.useState(false), isVisible = _b[0], setIsVisible = _b[1];
    react_1.useImperativeHandle(forwardedRef, function () {
        if (!itemRef.current)
            return;
        var _a = helpers_1.getRelativeRects(itemRef.current), left = _a.left, right = _a.right;
        var fullyVisible = left === undefined ||
            (left - offset >= -0.01 && right - offset <= slideWidth + 0.01);
        setIsVisible(fullyVisible);
        return {
            left: left,
            right: right,
            fullyVisible: fullyVisible
        };
    }, [slideWidth, offset]);
    return (react_1.default.createElement("li", __assign({ ref: itemRef, "aria-hidden": !isVisible }, rest), children));
};
exports.default = component_utils_1.withForwardRef(EbayCarouselItem);
