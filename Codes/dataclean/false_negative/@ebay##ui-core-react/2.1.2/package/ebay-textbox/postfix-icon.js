"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = __importDefault(require("react"));
var ebay_icon_1 = require("../ebay-icon");
var ebay_icon_button_1 = require("../ebay-icon-button");
var EbayTextboxPostfixIcon = function (_a) {
    var name = _a.name, buttonAriaLabel = _a.buttonAriaLabel, _b = _a.onClick, onClick = _b === void 0 ? function () { } : _b;
    return buttonAriaLabel ?
        react_1.default.createElement(ebay_icon_button_1.EbayIconButton, { "aria-label": buttonAriaLabel, icon: name, transparent: true, onClick: onClick }) :
        react_1.default.createElement(ebay_icon_1.EbayIcon, { name: name });
};
exports.default = EbayTextboxPostfixIcon;
