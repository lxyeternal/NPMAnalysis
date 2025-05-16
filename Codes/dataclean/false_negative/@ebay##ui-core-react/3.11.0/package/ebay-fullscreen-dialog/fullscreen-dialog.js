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
var ebay_dialog_base_1 = require("../ebay-dialog-base");
var classPrefix = 'fullscreen-dialog';
var EbayFullscreenDialog = function (_a) {
    var open = _a.open, _b = _a.onClose, onClose = _b === void 0 ? function () { } : _b, _c = _a.onOpen, onOpen = _c === void 0 ? function () { } : _c, className = _a.className, animated = _a.animated, rest = __rest(_a, ["open", "onClose", "onOpen", "className", "animated"]);
    return (react_1.default.createElement(ebay_dialog_base_1.DialogBaseWithState, __assign({}, rest, { classPrefix: classPrefix, buttonPosition: "left", onCloseBtnClick: onClose, transitionElement: "window", animated: animated, className: classnames_1.default(className, classPrefix + "--mask-fade-slow"), windowClass: classnames_1.default(classPrefix + "__window", classPrefix + "__window--slide"), open: open })));
};
exports.default = EbayFullscreenDialog;
