import { Component, EventEmitter, Output } from '@angular/core';
import { ContextMenuConfig } from './context-menu-config';
var ContextMenuComponent = /** @class */ (function () {
    /**
     * @param {?} config
     */
    function ContextMenuComponent(config) {
        this.config = config;
        this.menuActionClick = new EventEmitter();
    }
    /**
     * @return {?}
     */
    ContextMenuComponent.prototype.ngOnInit = function () {
    };
    /**
     * @param {?} item
     * @return {?}
     */
    ContextMenuComponent.prototype.onContextMenuAction = function (item) {
        if (!item || !item.click)
            return;
        item.click(this.config.context);
        this.menuActionClick.emit();
    };
    ContextMenuComponent.decorators = [
        { type: Component, args: [{
                    selector: 'app-context-menu',
                    template: "<ul class=\"dropdown-menu\">\n    <ng-container *ngFor=\"let item of config.items\">\n        <li *ngIf=\"!item.divider\" [ngClass]=\"{disabled: item.disabled}\">\n            <a (click)=\"onContextMenuAction(item)\">{{item.text}}</a>\n        </li>\n        <li *ngIf=\"item.divider\" role=\"separator\" class=\"divider\"></li>\n    </ng-container>\n</ul>\n",
                    styles: [".dropdown-menu {\n        position: unset !important;\n        display: unset !important;\n      }\n      \n      a {\n        cursor: pointer;\n      }\n      "]
                },] },
    ];
    /**
     * @nocollapse
     */
    ContextMenuComponent.ctorParameters = function () { return [
        { type: ContextMenuConfig, },
    ]; };
    ContextMenuComponent.propDecorators = {
        'menuActionClick': [{ type: Output },],
    };
    return ContextMenuComponent;
}());
export { ContextMenuComponent };
function ContextMenuComponent_tsickle_Closure_declarations() {
    /** @type {?} */
    ContextMenuComponent.decorators;
    /**
     * @nocollapse
     * @type {?}
     */
    ContextMenuComponent.ctorParameters;
    /** @type {?} */
    ContextMenuComponent.propDecorators;
    /** @type {?} */
    ContextMenuComponent.prototype.menuActionClick;
    /** @type {?} */
    ContextMenuComponent.prototype.config;
}
