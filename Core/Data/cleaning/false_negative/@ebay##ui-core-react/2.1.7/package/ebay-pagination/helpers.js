"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getMaxWidth = exports.calcPageState = exports.pageNumbersAround = void 0;
var const_1 = require("./const");
function pageNumbersAround(totalPages, selectedPage, maxVisiblePages, withDots) {
    if (maxVisiblePages === void 0) { maxVisiblePages = totalPages; }
    if (withDots === void 0) { withDots = false; }
    var visibleItems = Math.min(maxVisiblePages, totalPages);
    var startIndexWithoutDots = Math.max(0, selectedPage - Math.ceil((visibleItems - 1) / 2));
    var startIndexWithDots = visibleItems < 4 ? selectedPage :
        Math.max(0, selectedPage - Math.floor((visibleItems - 1) / 2));
    var endIndex = (withDots ? startIndexWithDots : startIndexWithoutDots) + visibleItems;
    var closeToEnd = endIndex >= totalPages;
    var visibleRangeWithDots = function (start, end) {
        var items = visibleRange(totalPages, start, end);
        if (visibleItems > 2) {
            items[end - 2] = 'dots';
            items[end - 1] = 'hidden';
            items[totalPages - 1] = 'visible';
        }
        else if (visibleItems > 1) {
            items[end - 1] = 'dots';
        }
        return items;
    };
    if (closeToEnd) {
        return visibleRange(totalPages, totalPages - visibleItems);
    }
    return withDots ?
        visibleRangeWithDots(startIndexWithDots, endIndex) :
        visibleRange(totalPages, startIndexWithoutDots, endIndex);
}
exports.pageNumbersAround = pageNumbersAround;
function calcPageState(selectedPage, visiblePages, totalPages, variant) {
    if (variant === void 0) { variant = 'show-range'; }
    if (selectedPage === -1) {
        return [];
    }
    var adjustedNumPages = clamp(Math.min(totalPages, visiblePages), const_1.MIN_PAGES, const_1.MAX_PAGES);
    return pageNumbersAround(totalPages, selectedPage - 1, adjustedNumPages, variant === 'show-last');
}
exports.calcPageState = calcPageState;
function clamp(n, min, max) {
    // eslint-disable-next-line no-nested-ternary
    return n <= min ? min : n >= max ? max : n;
}
function visibleRange(totalItems, start, end) {
    return Array(totalItems)
        .fill('hidden')
        .fill('visible', start, end);
}
/**
 * Calculates the maximum width for an element within its container.
 *
 * Based on eBayUI Core Marko implementation.
 * See https://github.com/eBay/ebayui-core/blob/v8.6.0/src/components/ebay-pagination/component.js#L119-L132
 */
function getMaxWidth(el) {
    if (!el) {
        return 0;
    }
    el.style.width = '100vw';
    var result = el.offsetWidth;
    el.style.width = null;
    return result;
}
exports.getMaxWidth = getMaxWidth;
