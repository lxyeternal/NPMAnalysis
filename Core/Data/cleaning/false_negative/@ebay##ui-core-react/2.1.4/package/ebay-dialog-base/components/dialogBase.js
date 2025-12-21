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
exports.DialogBase = void 0;
var react_1 = __importStar(require("react"));
var classnames_1 = __importDefault(require("classnames"));
var screenreaderTrap = __importStar(require("makeup-screenreader-trap"));
var keyboardTrap = __importStar(require("makeup-keyboard-trap"));
var ebay_icon_1 = require("../../ebay-icon");
var random_id_1 = require("../../common/random-id");
var animation_1 = require("./animation");
exports.DialogBase = function (_a) {
    var _b;
    var _c = _a.baseEl, Container = _c === void 0 ? 'div' : _c, _d = _a.classPrefix, classPrefix = _d === void 0 ? 'drawer-dialog' : _d, windowClass = _a.windowClass, windowType = _a.windowType, mainId = _a.mainId, top = _a.top, header = _a.header, _e = _a.buttonPosition, buttonPosition = _e === void 0 ? 'left' : _e, children = _a.children, ariaLabelledby = _a.ariaLabelledby, a11yCloseText = _a.a11yCloseText, _f = _a.onCloseBtnClick, onCloseBtnClick = _f === void 0 ? function () { } : _f, footer = _a.footer, onScroll = _a.onScroll, _g = _a.open, open = _g === void 0 ? false : _g, _h = _a.onBackgroundClick, onBackgroundClick = _h === void 0 ? function () { } : _h, ignoreEscape = _a.ignoreEscape, closeButton = _a.closeButton, isModal = _a.isModal, _j = _a.role, role = _j === void 0 ? 'dialog' : _j, focus = _a.focus, transitionElement = _a.transitionElement, animated = _a.animated, props = __rest(_a, ["baseEl", "classPrefix", "windowClass", "windowType", "mainId", "top", "header", "buttonPosition", "children", "ariaLabelledby", "a11yCloseText", "onCloseBtnClick", "footer", "onScroll", "open", "onBackgroundClick", "ignoreEscape", "closeButton", "isModal", "role", "focus", "transitionElement", "animated"]);
    var dialogRef = react_1.useRef(null);
    var drawerBaseEl = react_1.useRef(null);
    var closeButtonRef = react_1.useRef(null);
    var _k = react_1.useState(''), rId = _k[0], setRandomId = _k[1];
    react_1.useEffect(function () {
        setRandomId(random_id_1.randomId());
    }, []);
    react_1.useEffect(function () {
        var handleBackgroundClick = function (e) {
            if (drawerBaseEl.current && !drawerBaseEl.current.contains(e.target)) {
                onBackgroundClick(e);
            }
        };
        if (open && buttonPosition !== 'hidden') {
            // On React 18 useEffect hooks runs synchronous instead of asynchronous as React 17 or prior
            // causing the event listener to be attached to the document at the same time that the dialog
            // opens. Adding a timeout so the event is attached after the click event that opened the modal
            // is finished.
            setTimeout(function () {
                document.addEventListener('click', handleBackgroundClick, false);
            });
        }
        return function () { return document.removeEventListener('click', handleBackgroundClick, false); };
    }, [onBackgroundClick, open]);
    react_1.useEffect(function () {
        if (open && isModal) {
            screenreaderTrap.trap(drawerBaseEl.current);
            keyboardTrap.trap(drawerBaseEl.current);
        }
        else {
            screenreaderTrap.untrap();
            keyboardTrap.untrap();
        }
        return function () {
            screenreaderTrap.untrap();
            keyboardTrap.untrap();
        };
    }, [open, isModal]);
    animation_1.useDialogAnimation({
        open: open,
        classPrefix: classPrefix,
        transitionElement: transitionElement,
        dialogRef: dialogRef,
        dialogWindowRef: drawerBaseEl,
        enabled: animated,
        onTransitionEnd: function () { return handleFocus(open); }
    });
    var onKeyDown = function (event) {
        if (!ignoreEscape && event.key === 'Escape') {
            event.stopPropagation();
            onCloseBtnClick(undefined);
        }
    };
    react_1.useEffect(function () {
        // For animated dialogs we handle the focus on transitionEnd event
        if (!animated) {
            handleFocus(open);
        }
    }, [open]);
    function handleFocus(isOpen) {
        var _a, _b;
        if (isOpen) {
            if (focus) {
                (_a = focus.current) === null || _a === void 0 ? void 0 : _a.focus();
            }
            else if (isModal) {
                (_b = closeButtonRef.current) === null || _b === void 0 ? void 0 : _b.focus();
            }
            document.addEventListener('keydown', onKeyDown, false);
            return function () { return document.removeEventListener('keydown', onKeyDown, false); };
        }
    }
    var closeButtonContent = buttonPosition !== 'hidden' && (react_1.default.createElement("button", { ref: closeButtonRef, className: classnames_1.default("icon-btn", classPrefix + "__close", {
            'icon-btn--transparent': classPrefix === "toast-dialog"
        }), type: "button", "aria-label": a11yCloseText, onClick: onCloseBtnClick }, closeButton || react_1.default.createElement(ebay_icon_1.EbayIcon, { name: "close" })));
    var windowClassName = windowType ? classPrefix + "__" + windowType + "-window" : classPrefix + "__window";
    var dialogTitleId = ((_b = header === null || header === void 0 ? void 0 : header.props) === null || _b === void 0 ? void 0 : _b.id) || "dialog-title-" + rId;
    var dialogLabelledBy = ariaLabelledby || dialogTitleId;
    var dialogHeader = header ? react_1.cloneElement(header, __assign(__assign({}, header.props), { id: dialogTitleId })) : null;
    return (react_1.default.createElement(Container, __assign({}, props, { "aria-labelledby": dialogLabelledBy, "arial-modal": "true", role: role, hidden: !open, className: classnames_1.default(classPrefix, props.className), "aria-live": !isModal ? 'polite' : undefined, ref: dialogRef, onKeyDown: onKeyDown }),
        react_1.default.createElement("div", { className: classnames_1.default(windowClassName, windowClass), ref: drawerBaseEl },
            top,
            dialogHeader && (react_1.default.createElement("div", { className: classPrefix + "__header" },
                buttonPosition === 'right' && dialogHeader,
                buttonPosition !== 'bottom' && closeButtonContent,
                (buttonPosition === 'left' || buttonPosition === 'hidden') && dialogHeader)),
            react_1.default.createElement("div", { id: mainId, className: classPrefix + "__main", onScroll: onScroll }, children),
            footer || buttonPosition === 'bottom' ? (react_1.default.createElement("div", { className: classPrefix + "__footer" },
                footer,
                buttonPosition === 'bottom' && closeButtonContent)) : null)));
};
exports.default = exports.DialogBase;
