import { ContextMenuService } from './services/context-menu.service';
import { ContextMenuComponent } from './components/context-menu/context-menu.component';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
export class ContextMenuModule {
}
ContextMenuModule.decorators = [
    { type: NgModule, args: [{
                declarations: [ContextMenuComponent],
                imports: [CommonModule],
                exports: [],
                providers: [ContextMenuService],
                entryComponents: [ContextMenuComponent]
            },] },
];
/**
 * @nocollapse
 */
ContextMenuModule.ctorParameters = () => [];
function ContextMenuModule_tsickle_Closure_declarations() {
    /** @type {?} */
    ContextMenuModule.decorators;
    /**
     * @nocollapse
     * @type {?}
     */
    ContextMenuModule.ctorParameters;
}
