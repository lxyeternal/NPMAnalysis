"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = __importDefault(require("react"));
var button_cell_1 = __importDefault(require("./button-cell"));
var button_text_1 = __importDefault(require("./button-text"));
var ebay_icon_1 = require("../ebay-icon");
var EbayButtonExpand = function (_a) {
    var children = _a.children;
    return (react_1.default.createElement(button_cell_1.default, null,
        react_1.default.createElement(button_text_1.default, null, children),
        react_1.default.createElement(ebay_icon_1.EbayIcon, { name: "dropdown" })));
};
exports.default = EbayButtonExpand;
