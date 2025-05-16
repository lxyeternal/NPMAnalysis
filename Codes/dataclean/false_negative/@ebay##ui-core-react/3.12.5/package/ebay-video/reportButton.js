"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.ReportButton = void 0;
var ebay_icon_1 = require("../ebay-icon");
var react_1 = __importDefault(require("react"));
exports.ReportButton = function (_a) {
    var onReport = _a.onReport, children = _a.children;
    return (react_1.default.createElement("button", { className: "video-player__report-button", onClick: onReport },
        react_1.default.createElement(ebay_icon_1.EbayIcon, { name: "reportFlag" }),
        children));
};
