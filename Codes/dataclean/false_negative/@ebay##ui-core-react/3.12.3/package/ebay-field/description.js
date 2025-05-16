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
var Description = function (_a) {
    var _b;
    var type = _a.type, _c = _a.position, position = _c === void 0 ? 'below' : _c, className = _a.className, children = _a.children, rest = __rest(_a, ["type", "position", "className", "children"]);
    var wrapperClassName = classnames_1.default(className, 'field__description', (_b = {}, _b["field__description--" + type] = type, _b));
    var WrapperElement = position === 'below' ? "div" : "span";
    return (react_1.default.createElement(WrapperElement, __assign({}, rest, { className: wrapperClassName }),
        react_1.default.createElement("span", null, children)));
};
exports.default = Description;
