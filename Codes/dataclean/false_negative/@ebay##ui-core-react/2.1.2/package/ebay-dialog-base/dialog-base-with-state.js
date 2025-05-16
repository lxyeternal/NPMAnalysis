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
Object.defineProperty(exports, "__esModule", { value: true });
exports.DialogBaseWithState = void 0;
var react_1 = __importStar(require("react"));
var react_remove_scroll_1 = require("react-remove-scroll");
var dialogBase_1 = require("./components/dialogBase");
var index_1 = require("./index");
exports.DialogBaseWithState = function (_a) {
    var isModal = _a.isModal, open = _a.open, children = _a.children, _b = _a.animated, animated = _b === void 0 ? true : _b, rest = __rest(_a, ["isModal", "open", "children", "animated"]);
    var shouldRenderModal = isModal !== false;
    var childrenArray = react_1.Children.toArray(children);
    var header = childrenArray.find(function (child) { return child.type === index_1.EbayDialogHeader; });
    var footer = childrenArray.find(function (child) { return child.type === index_1.EbayDialogFooter; });
    var closeButton = childrenArray.find(function (child) { return child.type === index_1.EbayDialogCloseButton; });
    var content = childrenArray.filter(function (child) {
        return ![index_1.EbayDialogHeader, index_1.EbayDialogFooter, index_1.EbayDialogCloseButton].some(function (c) { return c === child.type; });
    });
    var dialogBase = (react_1.default.createElement(dialogBase_1.DialogBase, __assign({}, rest, { open: open, isModal: shouldRenderModal, header: header, footer: footer, closeButton: closeButton, animated: animated }), content));
    var renderOverLay = function () { return shouldRenderModal ? (react_1.default.createElement(react_remove_scroll_1.RemoveScroll, { enabled: open }, dialogBase)) : dialogBase; };
    return animated || open ? renderOverLay() : null;
};
exports.default = exports.DialogBaseWithState;
