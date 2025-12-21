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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = __importDefault(require("react"));
var ebay_icon_1 = require("../../ebay-icon");
var component_utils_1 = require("../component-utils");
var constants_1 = require("./constants");
var tooltip_close_button_1 = __importDefault(require("./tooltip-close-button"));
var TooltipContent = function (_a) {
    var id = _a.id, style = _a.style, _b = _a.pointer, pointer = _b === void 0 ? constants_1.DEFAULT_POINTER_DIRECTION : _b, children = _a.children, _c = _a.type, type = _c === void 0 ? 'tooltip' : _c, showCloseButton = _a.showCloseButton, a11yCloseText = _a.a11yCloseText, onClose = _a.onClose;
    var closeButton = component_utils_1.findComponent(children, tooltip_close_button_1.default);
    return (react_1.default.createElement("span", { className: type + "__overlay", id: id, role: "tooltip", style: __assign(__assign({}, constants_1.POINTER_STYLES[pointer]), style) },
        react_1.default.createElement("span", { className: type + "__pointer " + type + "__pointer--" + pointer }),
        react_1.default.createElement("span", { className: type + "__mask" },
            react_1.default.createElement("span", { className: type + "__cell" },
                react_1.default.createElement("span", { className: type + "__content" }, children),
                showCloseButton ? (react_1.default.createElement("button", __assign({}, closeButton === null || closeButton === void 0 ? void 0 : closeButton.props, { className: "icon-btn icon-btn--transparent " + type + "__close", type: "button", "aria-label": a11yCloseText, onClick: onClose }),
                    react_1.default.createElement(ebay_icon_1.EbayIcon, { name: "close" }))) : null))));
};
exports.default = TooltipContent;
