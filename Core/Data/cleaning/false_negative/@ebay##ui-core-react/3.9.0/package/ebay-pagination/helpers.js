"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getMaxWidth = exports.calcPageState = exports.pageNumbersAround = void 0;
var const_1 = require("./const");
function pageNumbersAround(totalPages, selectedPage, maxVisiblePages, variant) {
    if (maxVisiblePages === void 0) { maxVisiblePages = totalPages; }
    if (variant === void 0) { variant = null; }
    var withDots = variant === 'show-last' || (variant === 'overflow' && totalPages > const_1.MAX_PAGES);
    var hasLeadingDots = variant === 'overflow' && totalPages > const_1.MAX_PAGES;
    var visibleItems = Math.min(maxVisiblePages, totalPages);
    var startIndexWithoutDots = Math.max(0, selectedPage - Math.ceil((visibleItems - 1) / 2));
    var startIndexWithDots = visibleItems < const_1.MIN_VISIBLE_ITEMS ? selectedPage :
        Math.max(0, selectedPage - Math.floor((visibleItems - 1) / 2));
    var endIndex = (withDots ? startIndexWithDots : startIndexWithoutDots) + visibleItems;
    var closeToEnd = endIndex >= totalPages;
    var closeToFront = selectedPage <= const_1.MIN_VISIBLE_ITEMS;
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
    // middle show item[1] (...) and item[item.length - 1] (...)
    var visibleRangeWithOverflowDots = function (start, end) {
        // Following Dot
        if (closeToFront) {
            return visibleRangeWithDots(0, end);
            // Leading Dot
        }
        else if (closeToEnd) {
            var items_1 = visibleRange(totalPages, totalPages - const_1.TRAILING_SPACE_WITH_DOT, totalPages);
            items_1[0] = 'visible';
            items_1[1] = 'dots';
            return items_1;
        }
        // Middle case with Leading & Following Dots
        var items = visibleRange(totalPages, selectedPage - const_1.LEADING_SPACE_WITH_DOT, selectedPage + const_1.LEADING_SPACE_WITH_DOT + 1);
        items[0] = 'visible';
        items[1] = closeToFront ? 'visible' : 'dots';
        items[totalPages - 2] = 'dots';
        items[totalPages - 1] = 'visible';
        return items;
    };
    if (closeToEnd && totalPages <= const_1.MAX_PAGES) {
        return visibleRange(totalPages, totalPages - visibleItems);
    }
    if (withDots) {
        return hasLeadingDots ?
            visibleRangeWithOverflowDots(startIndexWithDots, endIndex) :
            visibleRangeWithDots(startIndexWithDots, endIndex);
    }
    return visibleRange(totalPages, startIndexWithoutDots, endIndex);
}
exports.pageNumbersAround = pageNumbersAround;
function calcPageState(selectedPage, visiblePages, totalPages, variant) {
    if (variant === void 0) { variant = 'show-range'; }
    if (selectedPage === -1) {
        return [];
    }
    var adjustedNumPages = variant === 'overflow' ? const_1.MAX_PAGES :
        clamp(Math.min(totalPages, visiblePages), const_1.MIN_PAGES, const_1.MAX_PAGES);
    return pageNumbersAround(totalPages, selectedPage - 1, adjustedNumPages, variant);
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
