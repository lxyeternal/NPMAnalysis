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
var carousel_control_button_1 = __importDefault(require("./carousel-control-button"));
var carousel_list_1 = __importDefault(require("./carousel-list"));
var helpers_1 = require("./helpers");
var debounce_1 = require("../common/debounce");
// TO-DO:
// Image slides
// Auto play
var EbayCarousel = function (_a) {
    var _b = _a.gap, gap = _b === void 0 ? 16 : _b, _c = _a.index, index = _c === void 0 ? 0 : _c, _itemsPerSlide = _a.itemsPerSlide, a11yPreviousText = _a.a11yPreviousText, a11yNextText = _a.a11yNextText, _d = _a.onScroll, onScroll = _d === void 0 ? function () { } : _d, _e = _a.onNext, onNext = _e === void 0 ? function () { } : _e, _f = _a.onPrevious, onPrevious = _f === void 0 ? function () { } : _f, _g = _a.onSlide, onSlide = _g === void 0 ? function () { } : _g, className = _a.className, children = _a.children, rest = __rest(_a, ["gap", "index", "itemsPerSlide", "a11yPreviousText", "a11yNextText", "onScroll", "onNext", "onPrevious", "onSlide", "className", "children"]);
    var _h = react_1.useState(index), activeIndex = _h[0], setActiveIndex = _h[1];
    var _j = react_1.useState(0), slideWidth = _j[0], setSlideWidth = _j[1];
    var _k = react_1.useState(0), offset = _k[0], setOffset = _k[1];
    var containerRef = react_1.useRef(null);
    var itemsRef = react_1.useRef([]);
    var itemCount = react_1.Children.count(children);
    var itemsPerSlide = Math.floor(_itemsPerSlide) || undefined;
    var isSingleSlide = itemCount <= itemsPerSlide;
    var prevControlDisabled = isSingleSlide || offset === 0;
    var nextControlDisabled = isSingleSlide || (offset === helpers_1.getMaxOffset(itemsRef.current, slideWidth));
    var handleResize = function () {
        if (!containerRef.current)
            return;
        var containerWidth = containerRef.current.getBoundingClientRect().width;
        setSlideWidth(containerWidth);
    };
    react_1.useEffect(function () {
        window.addEventListener('resize', debounce_1.debounce(handleResize, 16));
        return function () {
            window.removeEventListener('resize', debounce_1.debounce(handleResize, 16));
        };
    }, []);
    react_1.useEffect(function () {
        setOffset(helpers_1.getOffset(itemsRef.current, activeIndex, slideWidth));
    }, [activeIndex, slideWidth]);
    react_1.useEffect(function () {
        if (index >= 0 && index <= itemCount - 1) {
            setActiveIndex(index);
        }
    }, [index]);
    react_1.useEffect(function () {
        itemsRef.current = itemsRef.current.splice(0, itemCount);
    }, [children]);
    react_1.useEffect(function () {
        var containerWidth = containerRef.current.getBoundingClientRect().width;
        setSlideWidth(containerWidth);
    }, [containerRef.current]);
    var handleControlClick = function (event, _a) {
        var direction = _a.direction;
        var nextIndex = helpers_1.getNextIndex(direction, activeIndex, itemsRef.current, slideWidth, itemsPerSlide);
        var slide = helpers_1.getSlide(activeIndex, itemsPerSlide, nextIndex);
        setActiveIndex(nextIndex);
        if (direction === 'LEFT') {
            onPrevious(event);
        }
        else {
            onNext(event);
        }
        onSlide({ slide: slide });
    };
    return (react_1.default.createElement("div", __assign({ className: classnames_1.default('carousel', className, {
            'carousel--slides': itemsPerSlide,
            'carousel--peek': itemsPerSlide % 1 === 0
        }) }, rest),
        react_1.default.createElement("div", { ref: containerRef, className: "carousel__container" },
            react_1.default.createElement(carousel_control_button_1.default, { label: a11yPreviousText, type: "prev", disabled: prevControlDisabled, onClick: handleControlClick }),
            react_1.default.createElement(carousel_list_1.default, { itemsRef: itemsRef, offset: offset, gap: gap, itemsPerSlide: itemsPerSlide, nextControlDisabled: nextControlDisabled, activeIndex: activeIndex, onScroll: onScroll, onSetActiveIndex: setActiveIndex, slideWidth: slideWidth }, children),
            react_1.default.createElement(carousel_control_button_1.default, { type: "next", label: a11yNextText, disabled: nextControlDisabled, onClick: handleControlClick }))));
};
exports.default = EbayCarousel;
