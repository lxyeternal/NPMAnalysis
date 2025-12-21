"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
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
// todo: convert to hooks
var Tabs = /** @class */ (function (_super) {
    __extends(Tabs, _super);
    function Tabs(props) {
        var _this = _super.call(this, props) || this;
        var _a = props.index, index = _a === void 0 ? 0 : _a;
        _this.onTabSelect = _this.onTabSelect.bind(_this);
        _this.headings = [];
        _this.state = {
            selectedIndex: index,
            focusedIndex: index
        };
        return _this;
    }
    Tabs.prototype.componentDidUpdate = function (prevProps) {
        var _a;
        if (this.props.index !== prevProps.index) {
            this.onTabSelect(this.props.index);
        }
        (_a = this.headings[this.state.focusedIndex]) === null || _a === void 0 ? void 0 : _a.focus();
    };
    Tabs.prototype.onTabSelect = function (i) {
        if (this.props.onTabSelect) {
            this.props.onTabSelect(i);
        }
        this.setState({
            selectedIndex: i,
            focusedIndex: i
        });
    };
    /**
     * Handle a11y for heading
     * https://ebay.gitbooks.io/mindpatterns/content/disclosure/tabs.html
     */
    Tabs.prototype.onTabKeyDown = function (ev, index) {
        var _this = this;
        var _a = this.props, _b = _a.activation, activation = _b === void 0 ? 'auto' : _b, children = _a.children;
        event_utils_1.handleActionKeydown(ev, function () {
            ev.preventDefault();
            if (activation === 'manual') {
                _this.onTabSelect(index);
            }
        });
        event_utils_1.handleLeftRightArrowsKeydown(ev, function () {
            ev.preventDefault();
            var len = component_utils_1.filterByType(children, tab_1.default).length;
            var direction = ['Left', 'ArrowLeft'].includes(ev.key) ? -1 : 1;
            var nextIndex = (_this.state.focusedIndex + len + direction) % len;
            _this.setState({ focusedIndex: nextIndex });
            if (activation !== 'manual') {
                _this.onTabSelect(nextIndex);
            }
        });
    };
    Tabs.prototype.render = function () {
        var _this = this;
        var _a = this.props, className = _a.className, _b = _a.size, size = _b === void 0 ? 'medium' : _b, children = _a.children;
        var fake = component_utils_1.filterBy(children, function (_a) {
            var type = _a.type, props = _a.props;
            return type === tab_1.default && props.href;
        }).length > 0;
        var large = size === 'large';
        var tabHeadings = component_utils_1.filterByType(children, tab_1.default).map(function (item, i) {
            var _a = item.props, href = _a.href, content = _a.children;
            var itemProps = {
                refCallback: function (ref) { _this.headings[i] = ref; },
                index: i,
                selected: _this.state.selectedIndex === i,
                href: href,
                children: content,
                onClick: function () { _this.onTabSelect(i); },
                onKeyDown: function (e) { _this.onTabKeyDown(e, i); }
            };
            return react_1.default.cloneElement(item, itemProps);
        });
        var tabPanels = component_utils_1.filterByType(children, tab_panel_1.default).map(function (item, i) {
            var content = item.props.children;
            var itemProps = {
                index: i,
                selected: _this.state.selectedIndex === i,
                fake: fake,
                children: content
            };
            return react_1.default.cloneElement(item, itemProps);
        });
        return fake ? (react_1.default.createElement("div", { className: classnames_1.default(className, 'fake-tabs') },
            react_1.default.createElement("ul", { className: classnames_1.default('fake-tabs__items', { 'fake-tabs__items--large': large }) }, tabHeadings),
            react_1.default.createElement("div", { className: "fake-tabs__content" }, tabPanels))) : (react_1.default.createElement("div", { className: classnames_1.default(className, 'tabs') },
            react_1.default.createElement("div", { className: classnames_1.default('tabs__items', { 'tabs__items--large': large }), role: "tablist" }, tabHeadings),
            react_1.default.createElement("div", { className: "tabs__content" }, tabPanels)));
    };
    return Tabs;
}(react_1.Component));
exports.default = Tabs;
