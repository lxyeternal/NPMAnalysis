"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = __importDefault(require("react"));
var classnames_1 = __importDefault(require("classnames"));
var eek_util_1 = __importDefault(require("./eek-util"));
var ebay_icon_1 = require("../ebay-icon");
var EbayEek = function (_a) {
    var _b;
    var _c = _a.min, min = _c === void 0 ? '' : _c, _d = _a.max, max = _d === void 0 ? '' : _d, rating = _a.rating, a11yText = _a.a11yText, extraClasses = _a.className;
    var parsedRating = eek_util_1.default({ rating: rating, min: min, max: max });
    var className = classnames_1.default(extraClasses, 'eek', (_b = {}, _b["eek--rating-" + parsedRating] = !!parsedRating, _b));
    var backupA11yText = "Energy Rating: " + rating + ". Range: " + max + " - " + min + ".";
    return (react_1.default.createElement("div", { className: className, role: "figure", "aria-label": a11yText || backupA11yText },
        react_1.default.createElement("div", { className: "eek__container", "aria-hidden": true },
            react_1.default.createElement("span", { className: "eek__rating-range" },
                react_1.default.createElement("span", { "aria-hidden": "true" }, max),
                react_1.default.createElement(ebay_icon_1.EbayIcon, { name: "eekRangeArrow" }),
                react_1.default.createElement("span", { "aria-hidden": "true" }, min)),
            react_1.default.createElement("span", { className: "eek__rating", "aria-hidden": "true" }, rating)),
        react_1.default.createElement(ebay_icon_1.EbayIcon, { name: "eekArrow", height: "28px", width: "11px" })));
};
exports.default = EbayEek;
