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
var classnames_1 = __importDefault(require("classnames"));
var ebay_notice_content_1 = require("../ebay-notice-base/components/ebay-notice-content");
var notice_content_1 = __importDefault(require("../common/notice-utils/notice-content"));
var icon_1 = __importDefault(require("../ebay-icon/icon"));
var EbaySectionNotice = function (_a) {
    var _b = _a.status, status = _b === void 0 ? 'general' : _b, children = _a.children, className = _a.className, ariaLabel = _a["aria-label"], _c = _a["aria-roledescription"], ariaRoleDescription = _c === void 0 ? 'Notice' : _c, rest = __rest(_a, ["status", "children", "className", 'aria-label', 'aria-roledescription']);
    var childrenArray = react_1.default.Children.toArray(children);
    var content = childrenArray.find(function (_a) {
        var type = _a.type;
        return type === ebay_notice_content_1.EbayNoticeContent;
    });
    var hasStatus = status !== 'general' && status !== 'none';
    if (!content) {
        throw new Error("EbaySectionNotice: Please use a EbayNoticeContent that defines the content of the notice");
    }
    return (react_1.default.createElement("section", __assign({}, rest, { className: classnames_1.default(className, "section-notice", hasStatus && "section-notice--" + status), role: "region", "aria-label": !hasStatus ? ariaLabel : null, "aria-labelledby": hasStatus ? "section-notice-" + status : null, "aria-roledescription": ariaRoleDescription }),
        hasStatus && (react_1.default.createElement("div", { className: "section-notice__header", id: "section-notice-" + status },
            react_1.default.createElement(icon_1.default, { name: status + "-filled", a11yText: ariaLabel, a11yVariant: "label" }))),
        react_1.default.createElement(notice_content_1.default, __assign({}, content.props, { type: "section" })),
        children));
};
exports.default = EbaySectionNotice;
