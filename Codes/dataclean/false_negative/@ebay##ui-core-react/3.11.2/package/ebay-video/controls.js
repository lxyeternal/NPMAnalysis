"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.customControls = void 0;
var react_1 = __importDefault(require("react"));
var react_dom_1 = __importDefault(require("react-dom"));
var shaka_player_ui_1 = require("shaka-player/dist/shaka-player.ui");
var reportButton_1 = require("./reportButton");
function customControls(onReport) {
    if (onReport === void 0) { onReport = function () { }; }
    // Have to contain in order to not execute until shaka is downloaded
    var Report = /** @class */ (function (_super) {
        __extends(class_1, _super);
        function class_1(parent, controls, text) {
            var _this = _super.call(this, parent, controls) || this;
            appendChild(_this.parent, react_1.default.createElement(reportButton_1.ReportButton, { onReport: onReport }, text));
            return _this;
        }
        return class_1;
    }(shaka_player_ui_1.ui.Element));
    Report.Factory = /** @class */ (function () {
        function class_2(reportText) {
            this.reportText = reportText;
        }
        class_2.prototype.create = function (rootElement, controls) {
            return new Report(rootElement, controls, this.reportText);
        };
        return class_2;
    }());
    var TextSelection = shaka_player_ui_1.ui.TextSelection;
    TextSelection.Factory = /** @class */ (function () {
        function Factory() {
        }
        /** @override */
        // eslint-disable-next-line class-methods-use-this
        Factory.prototype.create = function (rootElement, controls) {
            return new shaka_player_ui_1.ui.TextSelection(rootElement, controls);
        };
        return Factory;
    }());
    return { Report: Report, TextSelection: TextSelection };
}
exports.customControls = customControls;
function appendChild(container, reactElement) {
    var tempEl = document.createElement('div');
    react_dom_1.default.render(reactElement, tempEl);
    container.appendChild(tempEl.firstChild);
}
