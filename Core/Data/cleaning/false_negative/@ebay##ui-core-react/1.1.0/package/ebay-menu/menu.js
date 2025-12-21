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
var use_roving_index_1 = __importDefault(require("../common/event-utils/use-roving-index"));
var usePrevious_1 = require("../common/component-utils/usePrevious");
var event_utils_1 = require("../common/event-utils");
var index_1 = require("./index");
var changedIndex = function (arr1, arr2) { return arr1.findIndex(function (x, i) { return arr2[i] !== x; }); };
var EbayMenu = function (_a) {
    var type = _a.type, _b = _a.priority, priority = _b === void 0 ? 'secondary' : _b, checked = _a.checked, className = _a.className, _c = _a.onKeyDown, onKeyDown = _c === void 0 ? function () { } : _c, _d = _a.onChange, onChange = _d === void 0 ? function () { } : _d, _e = _a.onSelect, onSelect = _e === void 0 ? function () { } : _e, children = _a.children, rest = __rest(_a, ["type", "priority", "checked", "className", "onKeyDown", "onChange", "onSelect", "children"]);
    var childrenArray = react_1.Children.toArray(children);
    var _f = use_roving_index_1.default(children, index_1.EbayMenuItem), focusedIndex = _f[0], setFocusedIndex = _f[1];
    var _g = react_1.useState(childrenArray.map(function () { return false; })), checkedIndexes = _g[0], setCheckedIndexes = _g[1];
    var updateIndex = function (index, value, resetOthers) {
        if (resetOthers === void 0) { resetOthers = false; }
        setCheckedIndexes(function (prevCheckedIndexes) {
            return prevCheckedIndexes.map(function (indexChecked, i) {
                var defaultValue = resetOthers ? false : indexChecked;
                return index === i ? value : defaultValue;
            });
        });
    };
    var selectIndex = function (index) {
        switch (type) {
            case 'radio':
                return updateIndex(index, true, true);
            case 'checkbox':
                return updateIndex(index, !checkedIndexes[index]);
            default:
                return;
        }
    };
    react_1.useEffect(function () {
        if (type === 'radio') {
            if (checked !== undefined) {
                selectIndex(checked);
            }
            var checkedIndex = childrenArray.findIndex(function (child) { return child.props.checked; });
            if (checkedIndex > -1) {
                selectIndex(checkedIndex);
            }
        }
        else if (type === 'checkbox') {
            setCheckedIndexes(childrenArray.map(function (child) { return child.props.checked; }));
        }
    }, []);
    var prevCheckedIndexes = usePrevious_1.usePrevious(checkedIndexes);
    react_1.useEffect(function () {
        if (type === 'radio') {
            var checkedIndex = checkedIndexes.findIndex(Boolean);
            if (checkedIndex > -1) {
                onChange(checkedIndex, true);
                onSelect(checkedIndex, true);
            }
        }
        else if (type === 'checkbox') {
            if (prevCheckedIndexes) {
                var index = changedIndex(prevCheckedIndexes, checkedIndexes);
                onChange(index, checkedIndexes[index]);
                onSelect(index, checkedIndexes[index]);
            }
        }
    }, [checkedIndexes]);
    return (react_1.default.createElement("span", __assign({}, rest, { className: classnames_1.default(className, 'menu') }),
        react_1.default.createElement("div", { className: "menu__items", role: "menu" }, childrenArray.map(function (child, i) {
            var _a = child.props, _b = _a.onClick, onClick = _b === void 0 ? function () { } : _b, _c = _a.onFocus, onFocus = _c === void 0 ? function () { } : _c, itemRest = __rest(_a, ["onClick", "onFocus"]);
            return react_1.cloneElement(child, __assign(__assign({}, itemRest), { focused: i === focusedIndex, tabIndex: focusedIndex === undefined ? 0 : -1, checked: checkedIndexes[i], onFocus: function (e) {
                    setFocusedIndex(i);
                    onFocus(e);
                }, onClick: function (e) {
                    setFocusedIndex(i);
                    selectIndex(i);
                    onClick(e);
                }, onKeyDown: function (e) {
                    event_utils_1.handleActionKeydown(e, function () {
                        selectIndex(i);
                    });
                    onKeyDown(i, checkedIndexes[i]);
                } }));
        }))));
};
exports.default = EbayMenu;
