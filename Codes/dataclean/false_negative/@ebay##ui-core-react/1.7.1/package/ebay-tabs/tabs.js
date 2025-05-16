"use strict";
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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = __importStar(require("react"));
var event_utils_1 = require("../common/event-utils");
var tab_1 = __importDefault(require("./tab"));
var tab_panel_1 = __importDefault(require("./tab-panel"));
var component_utils_1 = require("../common/component-utils");
var classnames_1 = __importDefault(require("classnames"));
var Tabs = function (_a) {
    var id = _a.id, className = _a.className, _b = _a.index, index = _b === void 0 ? 0 : _b, _c = _a.size, size = _c === void 0 ? 'medium' : _c, _d = _a.activation, activation = _d === void 0 ? 'auto' : _d, _e = _a.onTabSelect, onTabSelect = _e === void 0 ? function () { } : _e, children = _a.children;
    var headings = [];
    var _f = react_1.useState(index), selectedIndex = _f[0], setSelectedIndex = _f[1];
    var _g = react_1.useState(index), focusedIndex = _g[0], setFocusedIndex = _g[1];
    var onSelect = function (i) {
        onTabSelect(i);
        setSelectedIndex(i);
        setFocusedIndex(i);
    };
    /**
     * Handle a11y for heading
     * https://ebay.gitbooks.io/mindpatterns/content/disclosure/tabs.html
     */
    var onKeyDown = function (ev, i) {
        event_utils_1.handleActionKeydown(ev, function () {
            ev.preventDefault();
            if (activation === 'manual') {
                onSelect(i);
            }
        });
        event_utils_1.handleLeftRightArrowsKeydown(ev, function () {
            ev.preventDefault();
            var len = component_utils_1.filterByType(children, tab_1.default).length;
            var direction = ['Left', 'ArrowLeft'].includes(ev.key) ? -1 : 1;
            var nextIndex = (focusedIndex + len + direction) % len;
            setFocusedIndex(nextIndex);
            if (activation !== 'manual') {
                onSelect(nextIndex);
            }
        });
    };
    react_1.useEffect(function () {
        onSelect(index);
    }, [index]);
    react_1.useEffect(function () {
        var _a;
        (_a = headings[focusedIndex]) === null || _a === void 0 ? void 0 : _a.focus();
    }, [focusedIndex]);
    var isFake = component_utils_1.filterBy(children, function (_a) {
        var type = _a.type, props = _a.props;
        return type === tab_1.default && props.href;
    }).length > 0;
    var isLarge = size === 'large';
    var tabHeadings = component_utils_1.filterByType(children, tab_1.default).map(function (item, i) {
        var _a = item.props, href = _a.href, content = _a.children;
        var itemProps = {
            refCallback: function (ref) { headings[i] = ref; },
            index: i,
            parentId: id,
            selected: selectedIndex === i,
            href: href,
            children: content,
            onClick: function () { onSelect(i); },
            onKeyDown: function (e) { onKeyDown(e, i); }
        };
        return react_1.cloneElement(item, itemProps);
    });
    var tabPanels = component_utils_1.filterByType(children, tab_panel_1.default).map(function (item, i) {
        var content = item.props.children;
        var itemProps = {
            index: i,
            parentId: id,
            selected: selectedIndex === i,
            fake: isFake,
            children: content
        };
        return react_1.cloneElement(item, itemProps);
    });
    return isFake ? (react_1.default.createElement("div", { id: id, className: classnames_1.default(className, 'fake-tabs') },
        react_1.default.createElement("ul", { className: classnames_1.default('fake-tabs__items', { 'fake-tabs__items--large': isLarge }) }, tabHeadings),
        react_1.default.createElement("div", { className: "fake-tabs__content" }, tabPanels))) : (react_1.default.createElement("div", { id: id, className: classnames_1.default(className, 'tabs') },
        react_1.default.createElement("div", { className: classnames_1.default('tabs__items', { 'tabs__items--large': isLarge }), role: "tablist" }, tabHeadings),
        react_1.default.createElement("div", { className: "tabs__content" }, tabPanels)));
};
exports.default = Tabs;
