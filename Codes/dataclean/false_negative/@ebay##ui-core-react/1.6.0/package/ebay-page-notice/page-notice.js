"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var __rest = (this && this.__rest) || function (s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
            if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i]))
                t[p[i]] = s[p[i]];
        }
    return t;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = __importDefault(require("react"));
var notice_content_1 = __importDefault(require("../common/notice-utils/notice-content"));
var ebay_notice_content_1 = require("../ebay-notice-base/components/ebay-notice-content");
var ebay_icon_1 = require("../ebay-icon");
var EbayPageNotice = function (_a) {
    var _b = _a.status, status = _b === void 0 ? 'general' : _b, children = _a.children, ariaLabel = _a["aria-label"], rest = __rest(_a, ["status", "children", 'aria-label']);
    var childrenArray = react_1.default.Children.toArray(children);
    var content = childrenArray.find(function (child) { return child.type === ebay_notice_content_1.EbayNoticeContent; });
    if (!content) {
        throw new Error("EbayPageNotice: Please use a EbayNoticeContent that defines the content of the notice");
    }
    return (react_1.default.createElement("section", __assign({}, rest, { "aria-labelledby": status + "-status", className: "page-notice " + (status !== "general" ? "page-notice--" + status : ""), role: "region" }),
        status !== "general" ? (react_1.default.createElement("div", { className: "page-notice__header", id: status + "-status" },
            react_1.default.createElement(ebay_icon_1.EbayIcon, { name: status + "FilledSmall", a11yText: ariaLabel, a11yVariant: "label" }))) : null,
        react_1.default.createElement(notice_content_1.default, __assign({}, content.props, { type: "page" })),
        children));
};
exports.default = EbayPageNotice;
