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
exports.EbaySnackbarDialog = void 0;
var classnames_1 = __importDefault(require("classnames"));
var react_1 = __importStar(require("react"));
var ebay_dialog_base_1 = require("../../ebay-dialog-base");
var ebay_snackbar_dialog_action_1 = require("./ebay-snackbar-dialog-action");
var DEFAULT_TIMEOUT_LENGTH = 6000; // 6 seconds
exports.EbaySnackbarDialog = function (_a) {
    var className = _a.className, _b = _a.onOpen, onOpen = _b === void 0 ? function () { } : _b, _c = _a.onClose, onClose = _c === void 0 ? function () { } : _c, layout = _a.layout, open = _a.open, children = _a.children, onAction = _a.onAction, rest = __rest(_a, ["className", "onOpen", "onClose", "layout", "open", "children", "onAction"]);
    // We use this eventSet to track which event opened the snackbar and we make sure that
    // we don't close the snackbar in an undesired moment.
    // For example, the snackbar should stay open on focus even if the mouseLeave event happened.
    var eventSet = react_1.useRef(new Set());
    var timeoutRef = react_1.useRef();
    var _d = react_1.useState(open), isOpen = _d[0], setIsOpen = _d[1];
    var childrenArray = react_1.default.Children.toArray(children);
    var action = childrenArray.find(function (child) { return child.type === ebay_snackbar_dialog_action_1.EbaySnackbarDialogAction; });
    var content = childrenArray.filter(function (child) { return child.type !== ebay_snackbar_dialog_action_1.EbaySnackbarDialogAction; });
    var cancelCurrentCloseRequest = function () {
        clearTimeout(timeoutRef.current);
    };
    var closeDialog = function () {
        setIsOpen(false);
        onClose();
    };
    var requestToCloseDialog = function () {
        // We will make a request to close the snackbar only
        // when there is no pending opening event.
        if (eventSet.current.size === 0) {
            cancelCurrentCloseRequest();
            timeoutRef.current = setTimeout(function () {
                closeDialog();
            }, DEFAULT_TIMEOUT_LENGTH);
        }
    };
    var openDialog = function () {
        setIsOpen(true);
        onOpen();
        requestToCloseDialog();
    };
    var handleFocus = function () {
        cancelCurrentCloseRequest();
        eventSet.current.add('focus');
    };
    var handleBlur = function () {
        eventSet.current.delete('focus');
        requestToCloseDialog();
    };
    var handleMouseEnter = function () {
        cancelCurrentCloseRequest();
        eventSet.current.add('mouseEnter');
    };
    var handleMouseLeave = function () {
        eventSet.current.delete('mouseEnter');
        requestToCloseDialog();
    };
    var handleAction = function (event) {
        var _a, _b;
        cancelCurrentCloseRequest();
        onAction === null || onAction === void 0 ? void 0 : onAction(event);
        (_b = (_a = action === null || action === void 0 ? void 0 : action.props) === null || _a === void 0 ? void 0 : _a.onClick) === null || _b === void 0 ? void 0 : _b.call(_a, event);
        closeDialog();
    };
    react_1.useEffect(function () { return function () {
        // On unmount of the component we
        // cancel the close request
        cancelCurrentCloseRequest();
    }; }, []);
    // This useEffect is to make sure that the internal state is in sync with the "open" property.
    react_1.useEffect(function () {
        if (open) {
            openDialog();
        }
        else {
            closeDialog();
        }
    }, [open]);
    return (react_1.default.createElement(ebay_dialog_base_1.DialogBaseWithState, __assign({}, rest, { open: isOpen, isModal: false, baseEl: "aside", classPrefix: "snackbar-dialog", transitionElement: "root", a11yCloseText: "", buttonPosition: "hidden", className: classnames_1.default(className, 'snackbar-dialog--transition'), windowClass: layout === 'column' && 'snackbar-dialog__window--column', onFocus: handleFocus, onBlur: handleBlur, onMouseEnter: handleMouseEnter, onMouseLeave: handleMouseLeave }),
        content,
        action ? (react_1.default.createElement(ebay_dialog_base_1.EbayDialogActions, null, react_1.default.cloneElement(action, {
            onClick: handleAction
        }))) : null));
};
