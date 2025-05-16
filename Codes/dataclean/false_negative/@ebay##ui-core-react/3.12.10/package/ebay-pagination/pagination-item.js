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
var ebay_icon_1 = require("../ebay-icon");
var component_utils_1 = require("../common/component-utils");
var classnames_1 = __importDefault(require("classnames"));
var EbayPaginationItem = function (_a) {
    var _b = _a.pageIndex, pageIndex = _b === void 0 ? 0 : _b, key = _a.key, current = _a.current, disabled = _a.disabled, _c = _a.type, type = _c === void 0 ? 'page' : _c, href = _a.href, hide = _a.hide, children = _a.children, _d = _a.a11yPreviousText, a11yPreviousText = _d === void 0 ? 'Previous page' : _d, _e = _a.a11yNextText, a11yNextText = _e === void 0 ? 'Next page' : _e, onSelect = _a.onSelect, onNext = _a.onNext, onPrevious = _a.onPrevious, className = _a.className, style = _a.style, forwardedRef = _a.forwardedRef, rest = __rest(_a, ["pageIndex", "key", "current", "disabled", "type", "href", "hide", "children", "a11yPreviousText", "a11yNextText", "onSelect", "onNext", "onPrevious", "className", "style", "forwardedRef"]);
    var handlePageNumber = function (e) {
        onSelect(e, e.currentTarget.innerText, pageIndex);
    };
    var handleNextPage = function (e) {
        if (!e.currentTarget.getAttribute('aria-disabled')) {
            onNext(e);
        }
    };
    var handlePreviousPage = function (e) {
        if (!e.currentTarget.getAttribute('aria-disabled')) {
            onPrevious(e);
        }
    };
    var isAnchor = !!href;
    var ButtonOrAnchor = isAnchor ? 'a' : 'button';
    var iconClassName = isAnchor ? 'icon-link' : 'icon-btn';
    switch (type) {
        case 'previous':
            return (react_1.default.createElement(ButtonOrAnchor, __assign({}, rest, { ref: forwardedRef, "aria-disabled": disabled ? 'true' : undefined, "aria-label": a11yPreviousText, href: disabled ? undefined : href, className: classnames_1.default(iconClassName, 'pagination__previous'), style: style, onClick: handlePreviousPage }),
                react_1.default.createElement(ebay_icon_1.EbayIcon, { name: "paginationPrev" })));
        case 'next':
            return (react_1.default.createElement(ButtonOrAnchor, __assign({}, rest, { ref: forwardedRef, "aria-disabled": disabled ? 'true' : undefined, "aria-label": a11yNextText, href: disabled ? undefined : href, className: classnames_1.default(iconClassName, 'pagination__next'), style: style, onClick: handleNextPage }),
                react_1.default.createElement(ebay_icon_1.EbayIcon, { name: "paginationNext" })));
        case 'separator':
            return (react_1.default.createElement("span", { key: key, style: style, className: "pagination__item", ref: forwardedRef, role: "separator" }, children));
        default:
            return (react_1.default.createElement("li", __assign({}, rest, { hidden: hide }),
                react_1.default.createElement(ButtonOrAnchor, { ref: forwardedRef, "aria-current": current ? 'page' : undefined, href: href, className: "pagination__item", style: style, key: key, onClick: handlePageNumber }, children)));
    }
};
exports.default = component_utils_1.withForwardRef(EbayPaginationItem);
