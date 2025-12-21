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
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = __importStar(require("react"));
var classnames_1 = __importDefault(require("classnames"));
var ebay_notice_content_1 = require("../ebay-notice-base/components/ebay-notice-content");
var notice_content_1 = __importDefault(require("../common/notice-utils/notice-content"));
var component_utils_1 = require("../common/component-utils");
var ebay_icon_1 = require("../ebay-icon");
var EbayInlineNotice = function (_a) {
    var className = _a.className, _b = _a.status, status = _b === void 0 ? 'general' : _b, children = _a.children, _c = _a.hidden, hidden = _c === void 0 ? false : _c, ariaLabel = _a["aria-label"], _d = _a.onNoticeShow, onNoticeShow = _d === void 0 ? function () { } : _d;
    react_1.useEffect(function () {
        if (!hidden) {
            onNoticeShow();
        }
    }, [hidden]);
    if (hidden) {
        return null;
    }
    var content = component_utils_1.findComponent(children, ebay_notice_content_1.EbayNoticeContent);
    if (!content) {
        throw new Error("EbayInlineNotice: Please use a EbayNoticeContent that defines the content of the notice");
    }
    var isGeneral = status === "general";
    return (react_1.default.createElement("div", { className: classnames_1.default(className, "inline-notice " + (!isGeneral ? "inline-notice--" + status : "")) },
        !isGeneral ? (react_1.default.createElement("span", { className: "inline-notice__header" },
            react_1.default.createElement(ebay_icon_1.EbayIcon, { name: status + "-filled", a11yText: ariaLabel, a11yVariant: "label" }))) : null,
        react_1.default.createElement(notice_content_1.default, __assign({}, content.props, { type: "inline" }))));
};
exports.default = EbayInlineNotice;
