"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = __importDefault(require("react"));
var button_cell_1 = __importDefault(require("./button-cell"));
var ebay_progress_spinner_1 = require("../ebay-progress-spinner");
var EbayButtonLoading = function () { return (react_1.default.createElement(button_cell_1.default, null,
    react_1.default.createElement(ebay_progress_spinner_1.EbayProgressSpinner, null))); };
exports.default = EbayButtonLoading;
