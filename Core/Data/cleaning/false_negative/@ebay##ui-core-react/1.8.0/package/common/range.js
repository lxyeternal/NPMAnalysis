"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.range = void 0;
exports.range = function (start, stop, step) {
    if (step === void 0) { step = 1; }
    return Array(Math.ceil(((stop + 1) - start) / step)).fill(start).map(function (x, y) { return x + y * step; });
};
