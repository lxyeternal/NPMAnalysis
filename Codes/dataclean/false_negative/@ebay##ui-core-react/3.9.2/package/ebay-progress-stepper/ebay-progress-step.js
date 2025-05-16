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
var index_1 = require("./index");
var typeIcons = {
    complete: 'stepperConfirmation',
    attention: 'stepperAttention',
    upcoming: 'stepperUpcoming',
    active: 'stepperConfirmation'
};
var EbayProgressStep = function (_a) {
    var current = _a.current, _b = _a.state, state = _b === void 0 ? 'complete' : _b, children = _a.children, className = _a.className, rest = __rest(_a, ["current", "state", "children", "className"]);
    var childrenArray = react_1.Children.toArray(children);
    var title = childrenArray.find(function (child) { return child.type === index_1.EbayProgressTitle; });
    var text = childrenArray.filter(function (child) { return child.type !== index_1.EbayProgressTitle; });
    var stepClassNames = classnames_1.default(className, 'progress-stepper__item', { 'progress-stepper__item--attention': state === 'attention' });
    var icon = typeIcons[state];
    var ariaLabel = current ? 'current' : state;
    return (react_1.default.createElement("div", __assign({}, rest, { className: stepClassNames, role: "listitem", "aria-current": current ? 'step' : undefined }),
        react_1.default.createElement("div", { className: "progress-stepper__icon" }, icon && react_1.default.createElement(ebay_icon_1.EbayIcon, { name: icon, height: "24", width: "24", "aria-label": ariaLabel })),
        react_1.default.createElement("div", { className: "progress-stepper__text" },
            title,
            text)));
};
exports.default = EbayProgressStep;
