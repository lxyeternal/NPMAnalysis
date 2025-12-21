"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = __importDefault(require("react"));
var classnames_1 = __importDefault(require("classnames"));
var ebay_icon_1 = require("../ebay-icon");
var icon = {
    prev: 'carouselPrev',
    next: 'carouselNext'
};
var typeToDirection = {
    prev: 'LEFT',
    next: 'RIGHT'
};
var CarouselControlButton = function (_a) {
    var type = _a.type, label = _a.label, hidden = _a.hidden, disabled = _a.disabled, onClick = _a.onClick;
    var handleOnClick = function (event) {
        onClick(event, { direction: typeToDirection[type] });
    };
    return (react_1.default.createElement("button", { className: classnames_1.default('carousel__control', "carousel__control--" + type), "aria-label": label, "aria-disabled": disabled, disabled: disabled, onClick: handleOnClick },
        react_1.default.createElement(ebay_icon_1.EbayIcon, { className: classnames_1.default('icon', "icon--carousel-" + type), focusable: false, name: icon[type], "aria-hidden": hidden })));
};
exports.default = CarouselControlButton;
