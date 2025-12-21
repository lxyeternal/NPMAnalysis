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
var classPrefix = 'lightbox-dialog';
var EbayLightboxDialog = function (_a) {
    var _b;
    var open = _a.open, mode = _a.mode, _c = _a.onClose, onClose = _c === void 0 ? function () { } : _c, _d = _a.onOpen, onOpen = _d === void 0 ? function () { } : _d, rest = __rest(_a, ["open", "mode", "onClose", "onOpen"]);
    return (react_1.default.createElement(ebay_dialog_base_1.DialogBaseWithState, __assign({ buttonPosition: "right" }, rest, { classPrefix: classPrefix, onCloseBtnClick: onClose, onBackgroundClick: onClose, className: classnames_1.default(rest.className, classPrefix + "--mask-fade"), windowClass: classnames_1.default('lightbox-dialog__window--fade', (_b = {},
            _b[classPrefix + "__window--mini"] = mode === 'mini',
            _b)), open: open })));
};
exports.default = EbayLightboxDialog;
