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
Object.defineProperty(exports, "__esModule", { value: true });
exports.getClosestIndex = exports.getNextIndex = exports.getSlide = exports.alterChildren = exports.getOffset = exports.getMaxOffset = exports.isNativeScrolling = exports.getRelativeRects = void 0;
var react_1 = require("react");
function getRelativeRects(el) {
    var parent = el.parentElement;
    var currentLeft = parent
        ? parent.firstElementChild.getBoundingClientRect().left
        : 0;
    var _a = el.getBoundingClientRect(), left = _a.left, right = _a.right;
    return {
        left: left - currentLeft,
        right: right - currentLeft
    };
}
exports.getRelativeRects = getRelativeRects;
exports.isNativeScrolling = function (el) { return getComputedStyle(el).overflowX !== 'visible'; };
exports.getMaxOffset = function (items, slideWidth) {
    if (!items.length) {
        return 0;
    }
    var lastEl = items[items.length - 1];
    return Math.max(lastEl.right - slideWidth, 0) || 0;
};
exports.getOffset = function (items, index, slideWidth) {
    if (!items.length) {
        return 0;
    }
    return Math.min(items[index].left, exports.getMaxOffset(items, slideWidth)) || 0;
};
exports.alterChildren = function (children, itemsRef, itemsPerSlide, slideWidth, offset, gap) { return react_1.Children.map(children, function (item, index) {
    var _a = item.props.style, style = _a === void 0 ? {} : _a;
    var itemWidth;
    if (itemsPerSlide) {
        var itemsInSlide = itemsPerSlide + (itemsPerSlide % 1);
        itemWidth = "calc(" + 100 / itemsInSlide + "% - " + ((itemsInSlide - 1) * gap) / itemsInSlide + "px)";
    }
    var isStartOfSlide = itemsPerSlide ? index % itemsPerSlide === 0 : true;
    return react_1.cloneElement(item, __assign(__assign({}, item.props), { slideWidth: slideWidth,
        offset: offset, ref: function (el) {
            itemsRef.current[index] = el;
        }, className: isStartOfSlide ? 'carousel__snap-point' : item.props.className, style: __assign(__assign({}, style), { width: itemWidth || style.width, marginRight: gap && index !== react_1.Children.count(children) - 1 ? gap + "px" : style.marginRight }) }));
}); };
/**
 * Ensures that an index is valid.
 */
var normalizeIndex = function (index, items, itemsPerSlide) {
    if (index > 0) {
        var result = index;
        result %= items.length || 1; // Ensure index is within bounds.
        result -= result % (itemsPerSlide || 1); // Round index to the nearest valid slide index.
        result = Math.abs(result); // Ensure positive value.
        return result;
    }
    return 0;
};
/**
 * Gets the slide for a given index.
 * Defaults to the current index if none provided.
 */
exports.getSlide = function (activeIndex, itemsPerSlide, nextIndex) {
    if (nextIndex === void 0) { nextIndex = activeIndex; }
    if (!itemsPerSlide) {
        return;
    }
    return Math.ceil(nextIndex / itemsPerSlide);
};
var getDelta = function (direction) { return direction === 'LEFT' ? -1 : 1; };
exports.getNextIndex = function (direction, activeIndex, items, slideWidth, itemsPerSlide) {
    var i = activeIndex;
    var item;
    // If going backward from 0, we go to the end.
    if (direction === 'LEFT' && i === 0) {
        i = items.length - 1;
    }
    else {
        // Find the index of the next item that is not fully in view.
        do {
            var delta = getDelta(direction);
            item = items[i += delta];
        } while (item && item.fullyVisible);
        if (direction === 'LEFT' && !itemsPerSlide) {
            // If going left without items per slide, go as far left as possible while keeping this item fully in view.
            var targetOffset = item.right - slideWidth;
            do {
                item = items[--i];
            } while (item && item.left >= targetOffset);
            i += 1;
        }
    }
    return normalizeIndex(i, items, itemsPerSlide);
};
exports.getClosestIndex = function (scrollLeft, items, slideWidth, itemsPerSlide, gap) {
    if (itemsPerSlide === void 0) { itemsPerSlide = 1; }
    var closest;
    if (scrollLeft >= exports.getMaxOffset(items, slideWidth) - gap) {
        closest = items.length - 1;
    }
    else {
        // Find the closest item using a binary search on each carousel slide.
        var totalItems = items.length;
        var low = 0;
        var high = Math.ceil(totalItems / itemsPerSlide) - 1;
        while (high - low > 1) {
            var mid = Math.floor((low + high) / 2);
            if (scrollLeft > items[mid * itemsPerSlide].left) {
                low = mid;
            }
            else {
                high = mid;
            }
        }
        var deltaLow = Math.abs(scrollLeft - items[low * itemsPerSlide].left);
        var deltaHigh = Math.abs(scrollLeft - items[high * itemsPerSlide].left);
        closest = normalizeIndex((deltaLow > deltaHigh ? high : low) * itemsPerSlide, items, itemsPerSlide);
    }
    return closest;
};
