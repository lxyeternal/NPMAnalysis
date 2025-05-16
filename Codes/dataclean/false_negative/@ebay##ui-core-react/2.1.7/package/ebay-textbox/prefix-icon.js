"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = __importDefault(require("react"));
var ebay_icon_1 = require("../ebay-icon");
var EbayTextboxPrefixIcon = function (_a) {
    var name = _a.name;
    return (react_1.default.createElement(ebay_icon_1.EbayIcon, { name: name }));
};
exports.default = EbayTextboxPrefixIcon;
