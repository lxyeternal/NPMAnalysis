"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.useTooltip = void 0;
var react_1 = require("react");
exports.useTooltip = function (_a) {
    var onExpand = _a.onExpand, onCollapse = _a.onCollapse, _b = _a.initialExpanded, initialExpanded = _b === void 0 ? false : _b, hostRef = _a.hostRef;
    var _c = react_1.useState(initialExpanded), isExpanded = _c[0], setIsExpanded = _c[1];
    var expandTooltip = function () {
        setIsExpanded(true);
        if (onExpand) {
            onExpand();
        }
    };
    var collapseTooltip = function () {
        var _a;
        setIsExpanded(false);
        if (onCollapse) {
            onCollapse();
        }
        (_a = hostRef === null || hostRef === void 0 ? void 0 : hostRef.current) === null || _a === void 0 ? void 0 : _a.focus();
    };
    return {
        isExpanded: isExpanded,
        expandTooltip: expandTooltip,
        collapseTooltip: collapseTooltip
    };
};
