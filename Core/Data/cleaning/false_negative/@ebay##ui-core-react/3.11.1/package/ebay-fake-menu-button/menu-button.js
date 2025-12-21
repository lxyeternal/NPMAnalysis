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
var event_utils_1 = require("../common/event-utils");
var random_id_1 = require("../common/random-id");
var __1 = require("..");
var _1 = require(".");
var EbayMenuButton = function (_a) {
    var a11yText = _a.a11yText, noToggleIcon = _a.noToggleIcon, fixWidth = _a.fixWidth, reverse = _a.reverse, variant = _a.variant, _b = _a.expanded, defaultExpanded = _b === void 0 ? false : _b, className = _a.className, _c = _a.onCollapse, onCollapse = _c === void 0 ? function () { } : _c, _d = _a.onExpand, onExpand = _d === void 0 ? function () { } : _d, _e = _a.text, text = _e === void 0 ? '' : _e, children = _a.children, rest = __rest(_a, ["a11yText", "noToggleIcon", "fixWidth", "reverse", "variant", "expanded", "className", "onCollapse", "onExpand", "text", "children"]);
    var _f = react_1.useState(defaultExpanded), expanded = _f[0], setExpanded = _f[1];
    var _g = react_1.useState(), menuId = _g[0], setMenuId = _g[1];
    var ref = react_1.useRef();
    var icon = component_utils_1.findComponent(children, __1.EbayIcon);
    var label = component_utils_1.findComponent(children, _1.EbayFakeMenuButtonLabel) || (icon ? react_1.default.createElement("span", null, text) : text);
    var menuItems = component_utils_1.filterByType(children, [_1.EbayFakeMenuButtonItem, _1.EbayFakeMenuButtonSeparator]);
    react_1.useEffect(function () {
        var handleBackgroundClick = function (e) {
            if (ref.current && !ref.current.contains(e.currentTarget)) {
                setExpanded(false);
            }
        };
        if (expanded) {
            onExpand();
            // On React 18 useEffect hooks runs synchronous instead of asynchronous as React 17 or prior
            // causing the event listener to be attached to the document at the same time that the dialog
            // opens. Adding a timeout so the event is attached after the click event that opened the modal
            // is finished.
            setTimeout(function () {
                document.addEventListener('click', handleBackgroundClick, false);
            });
        }
        else if (expanded === false) {
            onCollapse();
        }
        return function () { return document.removeEventListener('click', handleBackgroundClick, false); };
    }, [expanded]);
    react_1.useEffect(function () {
        setMenuId(random_id_1.randomId());
    }, []);
    var handleMenuKeydown = function (e) {
        event_utils_1.handleEscapeKeydown(e, function () {
            var _a;
            setExpanded(false);
            (_a = ref.current) === null || _a === void 0 ? void 0 : _a.focus();
        });
    };
    var menuClasses = classnames_1.default('fake-menu-button__menu', {
        'menu-button__menu--fix-width': fixWidth,
        'menu-button__menu--reverse': reverse
    });
    var buttonProps = __assign({ ref: ref, className: 'fake-menu-button__button', 'aria-expanded': !!expanded, 'aria-haspopup': true, 'aria-label': a11yText, 'aria-controls': menuId, onClick: function () { return setExpanded(!expanded); } }, rest);
    return (react_1.default.createElement("span", { className: classnames_1.default('fake-menu-button', className) },
        variant === 'overflow' ?
            react_1.default.createElement(__1.EbayIconButton, __assign({ icon: "overflow" }, buttonProps)) :
            react_1.default.createElement(__1.EbayButton, __assign({ variant: variant === 'form' ? 'form' : undefined, bodyState: noToggleIcon ? undefined : 'expand' }, buttonProps),
                icon,
                label),
        expanded &&
            react_1.default.createElement(__1.EbayFakeMenu, { className: menuClasses, id: menuId, tabIndex: -1, onKeyDown: handleMenuKeydown }, menuItems.map(function (item, i) {
                return react_1.cloneElement(item, __assign(__assign({}, item.props), { className: classnames_1.default(item.props.className, 'fake-menu-button__item'), key: i, autoFocus: i === 0 }));
            }))));
};
exports.default = EbayMenuButton;
