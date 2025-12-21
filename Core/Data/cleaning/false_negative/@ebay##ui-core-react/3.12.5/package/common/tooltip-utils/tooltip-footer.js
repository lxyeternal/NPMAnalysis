"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = __importDefault(require("react"));
var classnames_1 = __importDefault(require("classnames"));
var TooltipFooter = function (_a) {
    var children = _a.children, className = _a.className, _b = _a.type, type = _b === void 0 ? 'tourtip' : _b;
    return (react_1.default.createElement("div", { className: classnames_1.default(type + "__footer", className) }, children));
};
exports.default = TooltipFooter;
