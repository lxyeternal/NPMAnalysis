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
var classPrefix = 'panel-dialog';
var EbayPanelDialog = function (_a) {
    var _b, _c;
    var open = _a.open, animated = _a.animated, _d = _a.position, position = _d === void 0 ? 'start' : _d, _e = _a.onClose, onClose = _e === void 0 ? function () { } : _e, _f = _a.onOpen, onOpen = _f === void 0 ? function () { } : _f, className = _a.className, rest = __rest(_a, ["open", "animated", "position", "onClose", "onOpen", "className"]);
    return (react_1.default.createElement(ebay_dialog_base_1.DialogBaseWithState, __assign({}, rest, { "aria-label": "Infotip", classPrefix: classPrefix, buttonPosition: "right", onCloseBtnClick: onClose, onBackgroundClick: onClose, animated: animated, className: classnames_1.default(className, (_b = {}, _b[classPrefix + "--mask-fade-slow"] = animated, _b)), windowClass: classnames_1.default(classPrefix + "__window--slide", (_c = {},
            _c[classPrefix + "__window--end"] = position === 'end',
            _c)), open: open })));
};
exports.default = EbayPanelDialog;
