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
var ebay_dialog_base_1 = require("../../ebay-dialog-base");
var THRESHOLD_TOUCH = 30;
var classPrefix = 'drawer-dialog';
var EbayDrawerDialog = function (_a) {
    var _b;
    var _c = _a.expanded, controlledExpanded = _c === void 0 ? false : _c, noHandle = _a.noHandle, _d = _a.onClose, onClose = _d === void 0 ? function () { } : _d, _e = _a.onCollapsed, onCollapsed = _e === void 0 ? function () { } : _e, _f = _a.onExpanded, onExpanded = _f === void 0 ? function () { } : _f, _g = _a.a11yMaximizeText, a11yMaximizeText = _g === void 0 ? 'Maximize Drawer' : _g, _h = _a.a11yMinimizeText, a11yMinimizeText = _h === void 0 ? 'Minimize Drawer' : _h, children = _a.children, rest = __rest(_a, ["expanded", "noHandle", "onClose", "onCollapsed", "onExpanded", "a11yMaximizeText", "a11yMinimizeText", "children"]);
    var touches = [];
    var _j = react_1.useState(controlledExpanded), expanded = _j[0], setExpanded = _j[1];
    react_1.useEffect(function () {
        setExpanded(controlledExpanded);
    }, [controlledExpanded]);
    var setExpandedState = function (expand) {
        setExpanded(expand);
        if (expand) {
            onExpanded();
        }
        else {
            onCollapsed();
        }
    };
    var handleTouchStart = function (e) {
        touches = Array.from(e.changedTouches).map(function (_a) {
            var identifier = _a.identifier, pageY = _a.pageY;
            return ({ identifier: identifier, pageY: pageY });
        });
    };
    var handleTouchEnd = function (e) {
        Array.from(e.changedTouches).forEach(function (_a) {
            var identifier = _a.identifier;
            var idx = touches.findIndex(function (touch) { return touch.identifier === identifier; });
            if (idx > -1) {
                touches.splice(idx, 1);
            }
        });
    };
    var handleTouchMove = function (e) {
        if (touches.length) {
            Array.from(e.changedTouches).forEach(function (_a) {
                var identifier = _a.identifier, pageY = _a.pageY;
                var compare = touches.findIndex(function (touch) { return touch.identifier === identifier; });
                var diff = pageY - touches[compare].pageY;
                if (diff > THRESHOLD_TOUCH) {
                    // Drag down, collpase
                    if (expanded) {
                        setExpandedState(false);
                    }
                    else {
                        onClose();
                    }
                    handleTouchEnd(e);
                }
                else if (diff < -THRESHOLD_TOUCH) {
                    setExpandedState(true);
                    handleTouchEnd(e);
                }
            });
        }
    };
    var handle = noHandle ? null : (react_1.default.createElement("button", { "aria-label": expanded ? a11yMinimizeText : a11yMaximizeText, className: classPrefix + "__handle", onClick: function () { return setExpandedState(!expanded); }, onScroll: function () { return setExpandedState(true); }, onTouchStart: handleTouchStart, onTouchMove: handleTouchMove, onTouchEnd: handleTouchEnd, type: "button" }));
    var childrenArray = react_1.Children.toArray(children);
    var header = childrenArray.find(function (_a) {
        var type = _a.type;
        return type === ebay_dialog_base_1.EbayDialogHeader;
    });
    var withoutHeader = childrenArray.filter(function (_a) {
        var type = _a.type;
        return type !== ebay_dialog_base_1.EbayDialogHeader;
    });
    return (react_1.default.createElement(ebay_dialog_base_1.DialogBaseWithState, __assign({}, rest, { classPrefix: classPrefix, buttonPosition: "right", onCloseBtnClick: onClose, className: classnames_1.default(rest.className, classPrefix + "--mask-fade-slow"), windowClass: classnames_1.default(classPrefix + "__window", classPrefix + "__window--slide", (_b = {},
            _b[classPrefix + "__window--expanded"] = expanded,
            _b)), onBackgroundClick: onClose, top: handle }),
        header || react_1.default.createElement(ebay_dialog_base_1.EbayDialogHeader, null),
        withoutHeader));
};
exports.default = EbayDrawerDialog;
