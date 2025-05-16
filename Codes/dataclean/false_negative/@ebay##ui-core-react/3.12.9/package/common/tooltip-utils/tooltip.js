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
var forwardRef_1 = require("../component-utils/forwardRef");
var component_utils_1 = require("../component-utils");
var tooltip_host_1 = __importDefault(require("./tooltip-host"));
var Tooltip = function (_a) {
    var _b;
    var className = _a.className, type = _a.type, isExpanded = _a.isExpanded, children = _a.children, forwardedRef = _a.forwardedRef, rest = __rest(_a, ["className", "type", "isExpanded", "children", "forwardedRef"]);
    var originalHostComponent = component_utils_1.findComponent(children, tooltip_host_1.default);
    var content = component_utils_1.excludeComponent(children, tooltip_host_1.default)[0];
    if (!originalHostComponent) {
        throw new Error("Tooltip: Please use a TooltipHost that defines the host of the tooltip");
    }
    if (!content) {
        throw new Error("Tooltip: Please use a component that defines the content of the tooltip");
    }
    var host = react_1.cloneElement(originalHostComponent, __assign({ className: type + "__host", 'aria-expanded': isExpanded, 'aria-describedby': content.props.id }, originalHostComponent.props));
    return (react_1.default.createElement("span", __assign({}, rest, { ref: forwardedRef, className: classnames_1.default(className, type, (_b = {},
            _b[type + "--expanded"] = isExpanded,
            _b)) }),
        host,
        content));
};
exports.default = forwardRef_1.withForwardRef(Tooltip);
