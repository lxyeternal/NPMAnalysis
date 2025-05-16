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
var tooltip_utils_1 = require("../common/tooltip-utils");
var ebay_drawer_dialog_1 = require("../ebay-drawer-dialog");
var ebay_dialog_base_1 = require("../ebay-dialog-base");
var ebay_infotip_host_1 = __importDefault(require("./ebay-infotip-host"));
var index_1 = require("./index");
var EbayInfotip = function (_a) {
    var _b = _a.variant, variant = _b === void 0 ? 'default' : _b, pointer = _a.pointer, overlayStyle = _a.overlayStyle, disabled = _a.disabled, onExpand = _a.onExpand, onCollapse = _a.onCollapse, children = _a.children, initialExpanded = _a.initialExpanded, _c = _a.icon, icon = _c === void 0 ? 'informationSmall' : _c, a11yCloseText = _a.a11yCloseText, ariaLabel = _a["aria-label"], className = _a.className;
    var buttonRef = react_1.useRef();
    var _d = tooltip_utils_1.useTooltip({ onCollapse: onCollapse, onExpand: onExpand, initialExpanded: initialExpanded, hostRef: buttonRef }), isExpanded = _d.isExpanded, expandTooltip = _d.expandTooltip, collapseTooltip = _d.collapseTooltip;
    var isModal = variant === 'modal';
    var containerRef = react_1.useRef();
    var heading = component_utils_1.findComponent(children, index_1.EbayInfotipHeading);
    var content = component_utils_1.findComponent(children, index_1.EbayInfotipContent);
    var button = component_utils_1.findComponent(children, ebay_infotip_host_1.default) || react_1.createElement(ebay_infotip_host_1.default);
    var toggleTooltip = function () {
        if (isExpanded) {
            collapseTooltip();
        }
        else {
            expandTooltip();
        }
    };
    if (!content) {
        throw new Error("EbayInfotip: Please use a EbayInfotipContent that defines the content of the infotip");
    }
    var _e = content.props, contentChildren = _e.children, contentProps = __rest(_e, ["children"]);
    return (react_1.default.createElement(tooltip_utils_1.Tooltip, { type: "infotip", isExpanded: isExpanded, className: classnames_1.default(className, { 'dialog--mini': isModal }), ref: containerRef },
        react_1.default.createElement(tooltip_utils_1.TooltipHost, null, react_1.cloneElement(button, __assign({ ref: buttonRef, onClick: toggleTooltip, disabled: disabled,
            variant: variant, 'aria-label': ariaLabel, 'aria-expanded': isExpanded, icon: icon }, button.props))),
        isModal ? (react_1.default.createElement(ebay_drawer_dialog_1.EbayDrawerDialog, __assign({}, contentProps, { open: isExpanded, onClose: collapseTooltip, mode: "mini", a11yCloseText: a11yCloseText, className: "dialog--mini__overlay" }),
            react_1.default.createElement(ebay_dialog_base_1.EbayDialogHeader, null, heading),
            contentChildren)) : (react_1.default.createElement(tooltip_utils_1.TooltipContent, __assign({}, contentProps, { type: "infotip", style: overlayStyle, pointer: pointer, showCloseButton: true, a11yCloseText: a11yCloseText, onClose: collapseTooltip }),
            heading,
            contentChildren))));
};
exports.default = EbayInfotip;
