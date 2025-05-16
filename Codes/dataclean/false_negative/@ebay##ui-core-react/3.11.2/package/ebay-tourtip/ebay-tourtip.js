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
var ebay_tourtip_content_1 = __importDefault(require("./ebay-tourtip-content"));
var ebay_tourtip_host_1 = __importDefault(require("./ebay-tourtip-host"));
var ebay_tourtip_footer_1 = __importDefault(require("./ebay-tourtip-footer"));
var ebay_tourtip_heading_1 = __importDefault(require("./ebay-tourtip-heading"));
var EbayTourtip = function (_a) {
    var a11yCloseText = _a.a11yCloseText, ariaLabel = _a["aria-label"], className = _a.className, children = _a.children, onCollapse = _a.onCollapse, onExpand = _a.onExpand, overlayStyle = _a.overlayStyle, pointer = _a.pointer, rest = __rest(_a, ["a11yCloseText", 'aria-label', "className", "children", "onCollapse", "onExpand", "overlayStyle", "pointer"]);
    var hostRef = react_1.useRef();
    var _b = tooltip_utils_1.useTooltip({ onExpand: onExpand, onCollapse: onCollapse, initialExpanded: true, hostRef: hostRef }), isExpanded = _b.isExpanded, collapseTooltip = _b.collapseTooltip;
    var containerRef = react_1.useRef();
    var content = component_utils_1.findComponent(children, ebay_tourtip_content_1.default);
    if (!content) {
        throw new Error("EbayTourtip: Please use a EbayTourtipContent that defines the content of the tourtip");
    }
    var _c = content.props, contentChildren = _c.children, contentProps = _c.contentProps;
    var host = component_utils_1.findComponent(children, ebay_tourtip_host_1.default);
    if (!host) {
        throw new Error("EbayTourtip: Please use a EbayTourtipHost that defines the host of the tourtip");
    }
    var heading = component_utils_1.findComponent(children, ebay_tourtip_heading_1.default);
    var footer = component_utils_1.findComponent(children, ebay_tourtip_footer_1.default);
    return (react_1.default.createElement(tooltip_utils_1.Tooltip, __assign({}, rest, { className: className, type: "tourtip", isExpanded: isExpanded, ref: containerRef }),
        react_1.default.createElement(tooltip_utils_1.TooltipHost, __assign({}, host.props, { forwardedRef: hostRef, ariaLabel: ariaLabel, ariaExpanded: isExpanded })),
        react_1.default.createElement(tooltip_utils_1.TooltipContent, __assign({}, contentProps, { a11yCloseText: a11yCloseText, onClose: collapseTooltip, pointer: pointer, showCloseButton: true, style: overlayStyle, type: "tourtip" }),
            heading,
            contentChildren,
            footer && (react_1.default.createElement(tooltip_utils_1.TooltipFooter, { type: "tourtip" }, footer)))));
};
exports.default = EbayTourtip;
