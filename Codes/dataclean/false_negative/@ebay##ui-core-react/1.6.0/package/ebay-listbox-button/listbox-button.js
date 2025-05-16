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
var ebay_icon_1 = require("../ebay-icon");
var component_utils_1 = require("../common/component-utils");
var listbox_button_option_1 = __importDefault(require("./listbox-button-option"));
var ListboxButton = function (_a) {
    var children = _a.children, name = _a.name, _b = _a.onSelect, onSelect = _b === void 0 ? function () { } : _b, value = _a.value, borderless = _a.borderless, fluid = _a.fluid, className = _a.className, maxHeight = _a.maxHeight, prefixId = _a.prefixId, floatingLabel = _a.floatingLabel, rest = __rest(_a, ["children", "name", "onSelect", "value", "borderless", "fluid", "className", "maxHeight", "prefixId", "floatingLabel"]);
    var optionsContainerRef = react_1.useRef(null);
    var optionsParentContainerRef = react_1.useRef();
    var optionsByIndexRef = react_1.useRef(new Map());
    var buttonRef = react_1.useRef();
    var listBoxButtonOptions = component_utils_1.filterByType(children, listbox_button_option_1.default);
    if (!listBoxButtonOptions.length) {
        throw new Error("EbayListboxButton: Please use a\n        EbayListboxButtonOption that defines the options of the listbox");
    }
    var getInitialSelectedOption = function () {
        var selectedIndex = listBoxButtonOptions.findIndex(function (_a) {
            var props = _a.props;
            return props.value === value;
        });
        var index = selectedIndex > -1 ? selectedIndex : 0;
        return {
            option: listBoxButtonOptions[index],
            index: index
        };
    };
    // Get the default Selected value and set it in the state
    var _c = getInitialSelectedOption(), selectedOptionFromValue = _c.option, initialSelectedOptionIndex = _c.index;
    // Update the selected option to the state
    var _d = react_1.useState(selectedOptionFromValue), selectedOption = _d[0], setSelectedOption = _d[1];
    var _e = react_1.useState(initialSelectedOptionIndex), selectedIndex = _e[0], setSelectedIndex = _e[1];
    // Update the expanded status to the state
    var _f = react_1.useState(false), expanded = _f[0], setExpanded = _f[1];
    // Additional flag to avoid multiple re-render when users tries to open and close
    var _g = react_1.useState(false), optionsOpened = _g[0], setOptionsOpened = _g[1];
    react_1.useEffect(function () {
        setSelectedOption(selectedOptionFromValue);
    }, [value]);
    var childrenArray = react_1.Children.toArray(children);
    var getSelectedValueByIndex = function (index) { return childrenArray[index].props.value; };
    var getSelectedOption = function (currentIndex) { return optionsByIndexRef.current.get(currentIndex); };
    var setActiveDescendant = function (index) {
        var optionsContainerEle = optionsContainerRef.current;
        optionsContainerEle.setAttribute("aria-activedescendant", getSelectedOption(index).id);
    };
    var onOptionsSelect = function (e, optionValue, index) {
        // OnSelect set the selectedValue to the state and expanded to false to close the list box
        setSelectedOption(childrenArray[index]);
        setSelectedIndex(index);
        setExpanded(false);
        setActiveDescendant(index);
        buttonRef.current.focus();
        onSelect(e, optionValue, index);
    };
    var reset = function () {
        setExpanded(false);
        setSelectedOption(childrenArray[initialSelectedOptionIndex]);
    };
    var makeOptionActive = function (index) {
        var optionEle = optionsContainerRef.current.children[index];
        optionEle.setAttribute("aria-selected", 'true');
        optionEle.classList.add("listbox-button__option--active");
    };
    var makeOptionInActive = function (index) {
        var optionEle = optionsContainerRef.current.children[index];
        optionEle.setAttribute("aria-selected", 'false');
        optionEle.classList.remove("listbox-button__option--active");
    };
    // Followed the implementation from W3
    // https://www.w3.org/TR/wai-aria-practices/examples/listbox/listbox-collapsible.html
    var scrollOptions = function (index) {
        var listboxOptionsContainerNode = optionsParentContainerRef.current;
        var currentTarget = getSelectedOption(index);
        if (listboxOptionsContainerNode.scrollHeight > listboxOptionsContainerNode.clientHeight) {
            var scrollBottom = listboxOptionsContainerNode.clientHeight + listboxOptionsContainerNode.scrollTop;
            var elementBottom = currentTarget.offsetTop + currentTarget.offsetHeight;
            if (elementBottom > scrollBottom) {
                listboxOptionsContainerNode.scrollTop = elementBottom - listboxOptionsContainerNode.clientHeight;
            }
            else if (currentTarget.offsetTop < listboxOptionsContainerNode.scrollTop) {
                listboxOptionsContainerNode.scrollTop = currentTarget.offsetTop;
            }
        }
    };
    var makeSelections = function (updatedIndex) {
        makeOptionActive(updatedIndex);
        makeOptionInActive(selectedIndex);
        scrollOptions(updatedIndex);
        setActiveDescendant(updatedIndex);
        setSelectedIndex(updatedIndex);
        setSelectedOption(childrenArray[updatedIndex]);
    };
    var focusOptionsContainer = function (focusOptions) {
        return setTimeout(function () { var _a; return (_a = optionsContainerRef === null || optionsContainerRef === void 0 ? void 0 : optionsContainerRef.current) === null || _a === void 0 ? void 0 : _a.focus(focusOptions); }, 0);
    };
    var onButtonClick = function () {
        setExpanded(!expanded);
        setOptionsOpened(true);
        focusOptionsContainer({ preventScroll: true });
    };
    var onButtonKeyup = function (e) {
        switch (e.key) {
            case 'Escape':
                setExpanded(false);
                break;
            case 'Enter':
                focusOptionsContainer();
                break;
            default:
                break;
        }
    };
    var onOptionContainerKeydown = function (e) {
        switch (e.key) {
            case ' ':
            case 'PageUp':
            case 'PageDown':
            case 'Home':
            case 'End':
                e.preventDefault();
                break;
            case 'Down':
            case 'ArrowDown':
                e.preventDefault();
                if (selectedIndex !== listBoxButtonOptions.length - 1) {
                    makeSelections(selectedIndex < listBoxButtonOptions.length - 1 ? selectedIndex + 1 : 0);
                }
                break;
            case 'Up':
            case 'ArrowUp':
                e.preventDefault();
                if (selectedIndex !== 0) {
                    makeSelections(selectedIndex > 0 ? selectedIndex - 1 : listBoxButtonOptions.length - 1);
                }
                break;
            case 'Enter':
                setExpanded(false);
                setTimeout(function () { return setSelectedOption(childrenArray[selectedIndex]); });
                setTimeout(function () { return buttonRef.current.focus(); }, 0);
                onSelect(e, getSelectedValueByIndex(selectedIndex), selectedIndex);
                break;
            case 'Esc':
            case 'Escape':
                reset();
                break;
            default:
                break;
        }
    };
    // We want to minic the select box behavior so we take the onSelect that passed
    // at the parent level and use it for the OnClick on the list box since its a fake dropdown
    var updatelistBoxButtonOptions = listBoxButtonOptions
        .map(function (child, index) { return react_1.cloneElement(child, {
        index: index,
        key: index,
        selected: child.props.value === selectedOption.props.value,
        onClick: function (e, optionValue) { return onOptionsSelect(e, optionValue, index); },
        innerRef: function (optionNode) { return !optionNode
            ? optionsByIndexRef.current.delete(index)
            : optionsByIndexRef.current.set(index, optionNode); }
    }); });
    var wrapperClassName = classnames_1.default('listbox-button', className, { 'listbox-button--fluid': fluid });
    var buttonClassName = classnames_1.default('expand-btn', {
        'expand-btn--borderless': borderless,
        'expand-btn--floating-label': floatingLabel
    });
    var expandBtnTextId = prefixId && 'expand-btn-text';
    return (react_1.default.createElement("span", { className: wrapperClassName },
        react_1.default.createElement("button", __assign({}, rest, { type: "button", className: buttonClassName, "aria-expanded": expanded, "aria-haspopup": "listbox", "aria-labelledby": prefixId && prefixId + " " + expandBtnTextId, onClick: onButtonClick, 
            // https://stackoverflow.com/questions/17769005/onclick-and-onblur-ordering-issue
            onMouseDown: function (e) { return e.preventDefault(); }, onKeyUp: onButtonKeyup, ref: buttonRef }),
            react_1.default.createElement("span", { className: "expand-btn__cell" },
                floatingLabel ? (react_1.default.createElement("span", { className: "expand-btn__floating-label" }, floatingLabel)) : null,
                react_1.default.createElement("span", { className: "expand-btn__text", id: expandBtnTextId }, selectedOption.props.children),
                react_1.default.createElement(ebay_icon_1.EbayIcon, { name: "dropdown" }))),
        (expanded || optionsOpened) &&
            react_1.default.createElement("div", { className: "listbox-button__listbox", ref: optionsParentContainerRef, style: { maxHeight: maxHeight } },
                react_1.default.createElement("div", { className: "listbox-button__options", role: "listbox", tabIndex: 0, ref: optionsContainerRef, onKeyDown: function (e) { return onOptionContainerKeydown(e); }, 
                    // adding onMouseDown preventDefault b/c on IE the onClick event is not being fired on each
                    // option https://stackoverflow.com/questions/17769005/onclick-and-onblur-ordering-issue
                    onMouseDown: function (e) { return e.preventDefault(); }, onBlur: function () {
                        setExpanded(false);
                        setTimeout(function () { return buttonRef.current.focus(); }, 0);
                    } }, updatelistBoxButtonOptions)),
        react_1.default.createElement("select", { hidden: true, className: "listbox-button__native", name: name, value: selectedOption.props.value }, updatelistBoxButtonOptions.map(function (option, i) {
            return react_1.default.createElement("option", { value: option.props.value, key: i });
        }))));
};
exports.default = ListboxButton;
