"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = __importDefault(require("react"));
var notice_cta_1 = __importDefault(require("../common/notice-utils/notice-cta"));
var EbayPageNoticeCTA = function (_a) {
    var className = _a.className, children = _a.children;
    return (react_1.default.createElement(notice_cta_1.default, { className: className, type: "page" }, children));
};
exports.default = EbayPageNoticeCTA;
