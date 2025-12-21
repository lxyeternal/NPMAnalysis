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
var EbayProgressStepper = function (_a) {
    var _b = _a.direction, direction = _b === void 0 ? 'row' : _b, _c = _a.defaultState, defaultState = _c === void 0 ? 'active' : _c, children = _a.children, className = _a.className, rest = __rest(_a, ["direction", "defaultState", "children", "className"]);
    var childrenArray = react_1.Children.toArray(children);
    var currentIndex = currentIndexByDefaultState(childrenArray, defaultState);
    return (react_1.default.createElement("div", __assign({}, rest, { className: classnames_1.default(className, 'progress-stepper', {
            'progress-stepper--vertical': direction === 'column'
        }) }),
        react_1.default.createElement("div", { role: "list", className: "progress-stepper__items" }, childrenArray.map(function (child, index) { return (react_1.default.createElement(react_1.Fragment, { key: index },
            index > 0 && react_1.default.createElement("hr", { className: "progress-stepper__separator", role: "presentation" }),
            react_1.cloneElement(child, __assign(__assign({ state: stepState(index, currentIndex) }, child.props), { current: currentIndex === index })))); }))));
};
function currentIndexByDefaultState(steps, defaultState) {
    var foundCurrentIndex = steps.findIndex(function (child) { return child.props.current; });
    if (foundCurrentIndex === -1) {
        // eslint-disable-next-line default-case
        switch (defaultState) {
            case 'complete': return steps.length - 1;
            case 'upcoming': return 0;
        }
    }
    return foundCurrentIndex;
}
function stepState(stepIndex, currentIndex) {
    if (stepIndex <= currentIndex)
        return 'complete';
    if (stepIndex > currentIndex)
        return 'upcoming';
}
exports.default = EbayProgressStepper;
