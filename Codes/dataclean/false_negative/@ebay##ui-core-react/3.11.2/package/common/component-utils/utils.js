"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.filterBy = exports.filterByType = exports.excludeComponent = exports.findComponent = void 0;
var react_1 = require("react");
require("./array.polyfill.flat"); // for Mobile Safari 11
function findComponent(nodes, componentType) {
    if (nodes === void 0) { nodes = []; }
    var elements = react_1.Children.toArray(nodes);
    return elements.find(function (_a) {
        var type = _a.type;
        return type === componentType;
    }) || null;
}
exports.findComponent = findComponent;
function excludeComponent(nodes, componentType) {
    if (nodes === void 0) { nodes = []; }
    var elements = react_1.Children.toArray(nodes);
    return elements.filter(function (_a) {
        var type = _a.type;
        return type !== componentType;
    });
}
exports.excludeComponent = excludeComponent;
function filterByType(nodes, componentType) {
    if (nodes === void 0) { nodes = []; }
    var elements = react_1.Children.toArray(nodes);
    var types = [componentType].flat();
    return elements.filter(function (_a) {
        var type = _a.type;
        return types.includes(type);
    });
}
exports.filterByType = filterByType;
function filterBy(nodes, predicate) {
    if (nodes === void 0) { nodes = []; }
    var elements = react_1.Children.toArray(nodes);
    return elements.filter(predicate);
}
exports.filterBy = filterBy;
