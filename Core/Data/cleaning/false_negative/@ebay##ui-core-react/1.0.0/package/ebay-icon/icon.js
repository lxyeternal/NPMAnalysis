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
var component_utils_1 = require("../common/component-utils");
var random_id_1 = require("../common/random-id");
var SMALL_ICON_SIZE = 16;
var LARGE_ICON_SIZE = 64;
var DEFAULT_ICON_SIZE = 24;
var EbayIcon = function (_a) {
    var _b;
    var name = _a.name, extraClass = _a.className, _c = _a.noSkinClasses, noSkinClasses = _c === void 0 ? false : _c, a11yText = _a.a11yText, a11yVariant = _a.a11yVariant, forwardedRef = _a.forwardedRef, rest = __rest(_a, ["name", "className", "noSkinClasses", "a11yText", "a11yVariant", "forwardedRef"]);
    var _d = react_1.useState(''), rId = _d[0], setRandomId = _d[1];
    react_1.useEffect(function () {
        setRandomId(random_id_1.randomId());
    }, []);
    var noTitle = a11yVariant === 'label';
    var a11yTextId = a11yText && "icon-title-" + rId;
    var a11yProps = a11yText ? {
        'aria-labelledby': noTitle ? undefined : a11yTextId,
        'aria-label': noTitle ? a11yText : undefined,
        role: 'img'
    } : {
        'aria-hidden': true
    };
    var iconSize = getIconSize(name) + "px";
    var kebabName = kebabCased(name);
    var className = classnames_1.default(extraClass, { 'icon': !noSkinClasses }, (_b = {}, _b["icon--" + kebabName] = !noSkinClasses, _b));
    return (react_1.default.createElement("svg", __assign({ height: iconSize, width: iconSize }, rest, { className: className, xmlns: "http://www.w3.org/2000/svg", focusable: false, ref: forwardedRef }, a11yProps),
        a11yText && !noTitle && react_1.default.createElement("title", { id: a11yTextId }, a11yText),
        react_1.default.createElement("use", { xlinkHref: "#icon-" + kebabName })));
};
function getIconSize(iconName) {
    var sizeCandidate = iconName.split('-').slice(-1)[0];
    return {
        small: SMALL_ICON_SIZE,
        large: LARGE_ICON_SIZE
    }[sizeCandidate] || DEFAULT_ICON_SIZE;
}
function kebabCased(str) {
    return str.replace(/([A-Z])/g, function (s, c) { return "-" + c.toLowerCase(); });
}
exports.default = component_utils_1.withForwardRef(EbayIcon);
