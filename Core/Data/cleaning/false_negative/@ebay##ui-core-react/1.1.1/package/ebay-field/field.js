"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = __importDefault(require("react"));
var classnames_1 = __importDefault(require("classnames"));
var Field = function (_a) {
    var className = _a.className, _b = _a.layout, layout = _b === void 0 ? 'inline' : _b, children = _a.children;
    var WrapperElement = layout === 'block' ? 'div' : 'span';
    return (react_1.default.createElement(WrapperElement, { className: classnames_1.default('field', className) }, children));
};
exports.default = Field;
