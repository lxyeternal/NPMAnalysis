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
var ebay_select_option_1 = __importDefault(require("./ebay-select-option"));
var ebay_icon_1 = require("../ebay-icon");
var component_utils_1 = require("../common/component-utils");
var hooks_1 = require("../ebay-floating-label/hooks");
var isControlled = function (value) { return typeof value !== 'undefined'; };
var EbaySelect = function (_a) {
    var controlledValue = _a.value, defaultValue = _a.defaultValue, className = _a.className, borderless = _a.borderless, name = _a.name, disabled = _a.disabled, _b = _a.onChange, onChange = _b === void 0 ? function () { } : _b, _c = _a.onBlur, onBlur = _c === void 0 ? function () { } : _c, _d = _a.onFocus, onFocus = _d === void 0 ? function () { } : _d, floatingLabel = _a.floatingLabel, children = _a.children, inputSize = _a.inputSize, invalid = _a.invalid, rest = __rest(_a, ["value", "defaultValue", "className", "borderless", "name", "disabled", "onChange", "onBlur", "onFocus", "floatingLabel", "children", "inputSize", "invalid"]);
    var isFieldInvalid = invalid || rest['aria-invalid'] === 'true';
    var _e = react_1.useState(defaultValue), value = _e[0], setValue = _e[1];
    var selectRef = react_1.useRef(null);
    var _f = hooks_1.useFloatingLabel({
        ref: selectRef,
        inputId: rest.id,
        className: className,
        disabled: disabled,
        label: floatingLabel,
        inputValue: controlledValue,
        inputSize: inputSize,
        invalid: isFieldInvalid
    }), label = _f.label, Container = _f.Container, onFloatingLabelBlur = _f.onBlur, onFloatingLabelFocus = _f.onFocus, ref = _f.ref;
    var handleSelectChange = function (e) {
        var _a = e.target, newValue = _a.value, selectedIndex = _a.selectedIndex;
        if (!isControlled(controlledValue)) {
            setValue(newValue);
        }
        onChange(e, selectedIndex, newValue);
    };
    var handleBlur = function (event) {
        onBlur(event);
        onFloatingLabelBlur();
    };
    var handleFocus = function (event) {
        onFocus(event);
        onFloatingLabelFocus();
    };
    var selectClassName = classnames_1.default('select', className, {
        'select--borderless': borderless,
        'select--large': inputSize === "large"
    });
    return (react_1.default.createElement(Container, null,
        label,
        react_1.default.createElement("span", { className: selectClassName },
            react_1.default.createElement("select", __assign({}, rest, { name: name, value: isControlled(controlledValue) ? controlledValue : value, disabled: disabled, onChange: handleSelectChange, onBlur: handleBlur, onFocus: handleFocus, ref: ref }), options(children)),
            react_1.default.createElement(ebay_icon_1.EbayIcon, { name: "dropdown", height: "8", width: "8" }))));
};
exports.default = EbaySelect;
function optionGroups(data) {
    var optGroups = {};
    data.forEach(function (opt) {
        var option = opt.props;
        if (option.optgroup) {
            if (!Object.prototype.hasOwnProperty.call(optGroups, option.optgroup)) {
                optGroups[option.optgroup] = [];
            }
            optGroups[option.optgroup].push(option);
        }
    });
    return optGroups;
}
function options(children) {
    var renderedGroups = [];
    var allOptions = [];
    var optGroups = {};
    var withinGroup = false;
    var childrenOpts = component_utils_1.filterByType(children, ebay_select_option_1.default).map(function (c) { return react_1.cloneElement(c, {}); });
    if (childrenOpts) {
        optGroups = optionGroups(childrenOpts);
        var currentGroupName_1;
        childrenOpts.forEach(function (option, idx) {
            var _a = option.props, value = _a.value, optionClassName = _a.optionClassName, optionChildren = _a.children, optgroup = _a.optgroup;
            withinGroup = optgroup && renderedGroups.indexOf(optgroup) === -1;
            if (withinGroup) { // This will always be true when the very first group is encountered.
                currentGroupName_1 = optgroup;
                var currentGroupOptions = optGroups[currentGroupName_1];
                var opts = currentGroupOptions.map(function (groupOption) { return (react_1.default.createElement(ebay_select_option_1.default, { key: "opt-" + groupOption.value, value: groupOption.value, className: groupOption.optionClassName }, groupOption.children)); });
                allOptions.push(react_1.default.createElement("optgroup", { key: idx, label: optgroup }, opts));
                renderedGroups.push(optgroup);
            }
            else if (!optgroup) {
                /**
                 * The check below is necessary because we could still be in a group which has already
                 * been added to the renderedGroups array. In that case it will be skipped.
                 */
                allOptions.push(react_1.default.createElement(ebay_select_option_1.default, { key: idx, value: value, className: optionClassName }, optionChildren));
            }
        });
        return allOptions;
    }
}
