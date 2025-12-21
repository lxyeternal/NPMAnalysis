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
var component_utils_1 = require("../common/component-utils");
var tooltip_utils_1 = require("../common/tooltip-utils");
var ebay_tooltip_content_1 = __importDefault(require("./ebay-tooltip-content"));
var ebay_tooltip_host_1 = __importDefault(require("./ebay-tooltip-host"));
var EbayTooltip = function (_a) {
    var className = _a.className, pointer = _a.pointer, overlayStyle = _a.overlayStyle, noHover = _a.noHover, _b = _a.onFocus, onFocus = _b === void 0 ? function () { } : _b, _c = _a.onBlur, onBlur = _c === void 0 ? function () { } : _c, _d = _a.onMouseEnter, onMouseEnter = _d === void 0 ? function () { } : _d, _e = _a.onMouseLeave, onMouseLeave = _e === void 0 ? function () { } : _e, onExpand = _a.onExpand, onCollapse = _a.onCollapse, children = _a.children, rest = __rest(_a, ["className", "pointer", "overlayStyle", "noHover", "onFocus", "onBlur", "onMouseEnter", "onMouseLeave", "onExpand", "onCollapse", "children"]);
    var _f = tooltip_utils_1.useTooltip({ onCollapse: onCollapse, onExpand: onExpand }), isExpanded = _f.isExpanded, expandTooltip = _f.expandTooltip, collapseTooltip = _f.collapseTooltip;
    var timeoutRef = react_1.useRef();
    var handleOnMouseEnter = function (event) {
        onMouseEnter(event);
        if (!noHover) {
            clearTimeout(timeoutRef.current);
            expandTooltip();
        }
    };
    var handleOnMouseLeave = function (event) {
        onMouseLeave(event);
        if (!noHover) {
            clearTimeout(timeoutRef.current);
            timeoutRef.current = setTimeout(function () {
                collapseTooltip();
            }, 300);
        }
    };
    var handleOnFocus = function (event) {
        onFocus(event);
        expandTooltip();
    };
    var handleOnBlur = function (event) {
        onBlur(event);
        collapseTooltip();
    };
    var content = component_utils_1.findComponent(children, ebay_tooltip_content_1.default);
    var host = component_utils_1.findComponent(children, ebay_tooltip_host_1.default);
    if (!host) {
        throw new Error("EbayTooltip: Please use a EbayTooltipHost that defines the host of the tooltip");
    }
    if (!content) {
        throw new Error("EbayTooltip: Please use a EbayTooltipContent that defines the content of the tooltip");
    }
    return (react_1.default.createElement(tooltip_utils_1.Tooltip, __assign({}, rest, { className: className, type: "tooltip", isExpanded: isExpanded, onFocus: handleOnFocus, onBlur: handleOnBlur, onMouseEnter: handleOnMouseEnter, onMouseLeave: handleOnMouseLeave }),
        react_1.default.createElement(tooltip_utils_1.TooltipHost, __assign({}, host.props)),
        react_1.default.createElement(tooltip_utils_1.TooltipContent, __assign({}, content.props, { type: "tooltip", style: overlayStyle, pointer: pointer }))));
};
exports.default = EbayTooltip;
