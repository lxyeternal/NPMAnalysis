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
var react_1 = __importStar(require("react"));
var classnames_1 = __importDefault(require("classnames"));
var ebay_icon_1 = require("../ebay-icon");
var range_1 = require("../common/range");
var random_id_1 = require("../common/random-id");
var stars = range_1.range(1, 5);
var getValue = function (val) {
    var value = parseInt(val, 0) || 0;
    if (value > 5) {
        value = 0;
    }
    return value;
};
var EbayStarRatingSelect = function (_a) {
    var _b = _a.value, value = _b === void 0 ? 0 : _b, a11yText = _a.a11yText, className = _a.className, _c = _a.a11yStarText, a11yStarText = _c === void 0 ? [] : _c, disabled = _a.disabled, onChange = _a.onChange, onFocus = _a.onFocus, onKeyDown = _a.onKeyDown, _d = _a.name, name = _d === void 0 ? "star-rating-" + random_id_1.randomId() : _d, rest = __rest(_a, ["value", "a11yText", "className", "a11yStarText", "disabled", "onChange", "onFocus", "onKeyDown", "name"]);
    var _e = react_1.useState(getValue(value)), checkedValue = _e[0], setChecked = _e[1];
    react_1.useEffect(function () {
        setChecked(getValue(value));
    }, [value]);
    var handleKeyDown = function (i) { return function (e) {
        if (!disabled && onKeyDown) {
            setChecked(getValue(i));
            onKeyDown(e, i);
        }
    }; };
    var handleClick = function (i) { return function (e) {
        if (!disabled && onChange) {
            setChecked(getValue(i));
            onChange(e, i);
        }
    }; };
    var handleFocus = function (i) { return function (e) {
        if (!disabled && onFocus) {
            setChecked(getValue(i));
            onFocus(e, i);
        }
    }; };
    return (react_1.default.createElement("div", __assign({ role: a11yText && 'radiogroup', "aria-label": a11yText, className: classnames_1.default('star-rating-select', className) }, rest), stars.map(function (i) { return (react_1.default.createElement("span", { className: "star-rating-select__radio", key: i },
        react_1.default.createElement("input", { "aria-label": a11yStarText === null || a11yStarText === void 0 ? void 0 : a11yStarText[i - 1], className: classnames_1.default('star-rating-select__control', { 'star-rating-select__control--filled': i <= checkedValue }), type: "radio", name: name, value: i, disabled: disabled, defaultChecked: checkedValue === i, onClick: handleClick(i), onFocus: handleFocus(i), onKeyDown: handleKeyDown(i) }),
        react_1.default.createElement("span", { className: "star-rating-select__radio-icon" },
            react_1.default.createElement(ebay_icon_1.EbayIcon, { className: "star-rating__icon", name: "starDynamic" })))); })));
};
exports.default = EbayStarRatingSelect;
