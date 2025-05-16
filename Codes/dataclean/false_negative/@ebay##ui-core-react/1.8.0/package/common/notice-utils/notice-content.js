"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = __importDefault(require("react"));
var classnames_1 = __importDefault(require("classnames"));
var NoticeContent = function (_a) {
    var className = _a.className, type = _a.type, children = _a.children;
    var ContentTag = type === 'inline' ? 'span' : 'div';
    return (react_1.default.createElement(ContentTag, { className: classnames_1.default(className, type + "-notice__main") }, children));
};
exports.default = NoticeContent;
