"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.useTooltip = void 0;
var react_1 = require("react");
exports.useTooltip = function (_a) {
    var onExpand = _a.onExpand, onCollapse = _a.onCollapse, _b = _a.initialExpanded, initialExpanded = _b === void 0 ? false : _b;
    var _c = react_1.useState(initialExpanded), isExpanded = _c[0], setIsExpanded = _c[1];
    var expandTooltip = function () {
        setIsExpanded(true);
        if (onExpand) {
            onExpand();
        }
    };
    var collapseTooltip = function () {
        setIsExpanded(false);
        if (onCollapse) {
            onCollapse();
        }
    };
    return {
        isExpanded: isExpanded,
        expandTooltip: expandTooltip,
        collapseTooltip: collapseTooltip
    };
};
