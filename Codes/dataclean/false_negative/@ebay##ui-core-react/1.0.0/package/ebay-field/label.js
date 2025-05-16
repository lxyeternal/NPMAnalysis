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
var Label = function (_a) {
    var className = _a.className, children = _a.children, _b = _a.stacked, stacked = _b === void 0 ? false : _b, _c = _a.required, required = _c === void 0 ? false : _c, _d = _a.position, position = _d === void 0 ? 'start' : _d, rest = __rest(_a, ["className", "children", "stacked", "required", "position"]);
    var wrapperClassName = classnames_1.default("field__label", className, { 'field__label--stacked': stacked }, { 'field__label--end': position === 'end' });
    var requiredMark = required ? react_1.default.createElement(react_1.default.Fragment, null,
        " ",
        react_1.default.createElement("sup", null, "*")) : null;
    return react_1.default.createElement("label", __assign({ className: wrapperClassName }, rest),
        children,
        requiredMark);
};
exports.default = Label;
