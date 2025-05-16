"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = __importDefault(require("react"));
var EbayTourtipFooter = function (_a) {
    var index = _a.index, children = _a.children;
    return (react_1.default.createElement(react_1.default.Fragment, null,
        index !== undefined && (react_1.default.createElement("span", { className: "tourtip__index" }, index)),
        children));
};
exports.default = EbayTourtipFooter;
