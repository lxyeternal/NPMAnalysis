import { Component, EventEmitter, Output } from '@angular/core';
import { ContextMenuConfig } from './context-menu-config';
export class ContextMenuComponent {
    /**
     * @param {?} config
     */
    constructor(config) {
        this.config = config;
        this.menuActionClick = new EventEmitter();
    }
    /**
     * @return {?}
     */
    ngOnInit() {
    }
    /**
     * @param {?} item
     * @return {?}
     */
    onContextMenuAction(item) {
        if (!item || !item.click)
            return;
        item.click(this.config.context);
        this.menuActionClick.emit();
    }
}
ContextMenuComponent.decorators = [
    { type: Component, args: [{
                selector: 'app-context-menu',
                template: `<ul class="dropdown-menu">
    <ng-container *ngFor="let item of config.items">
        <li *ngIf="!item.divider" [ngClass]="{disabled: item.disabled}">
            <a (click)="onContextMenuAction(item)">{{item.text}}</a>
        </li>
        <li *ngIf="item.divider" role="separator" class="divider"></li>
    </ng-container>
</ul>
`,
                styles: [`.dropdown-menu {
        position: unset !important;
        display: unset !important;
      }
      
      a {
        cursor: pointer;
      }
      `]
            },] },
];
/**
 * @nocollapse
 */
ContextMenuComponent.ctorParameters = () => [
    { type: ContextMenuConfig, },
];
ContextMenuComponent.propDecorators = {
    'menuActionClick': [{ type: Output },],
};
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
