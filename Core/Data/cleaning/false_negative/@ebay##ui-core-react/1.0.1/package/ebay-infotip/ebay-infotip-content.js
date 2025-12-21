"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
/**
 * This Component is used only for finding it as a child of EbayInfotip
 * and pass the properties to TooltipContent
*/
var react_1 = __importDefault(require("react"));
var EbayInfotipContent = function (_a) {
    var children = _a.children;
    return react_1.default.createElement(react_1.default.Fragment, null, children);
};
exports.default = EbayInfotipContent;
