/**
 *
 */
export class ContextMenuAction {
    /**
     * @param {?} text
     * @param {?} click
     * @param {?=} disabled
     * @param {?=} icon
     */
    constructor(text, click, disabled, icon) {
        this.text = text;
        this.click = click;
        this.disabled = disabled;
        this.icon = icon;
        this.divider = false;
    }
}
function ContextMenuAction_tsickle_Closure_declarations() {
    /** @type {?} */
    ContextMenuAction.prototype.divider;
    /** @type {?} */
    ContextMenuAction.prototype.text;
    /** @type {?} */
    ContextMenuAction.prototype.click;
    /** @type {?} */
    ContextMenuAction.prototype.disabled;
    /** @type {?} */
    ContextMenuAction.prototype.icon;
}
/**
 *
 */
export class ContextMenuDivider {
    constructor() {
        this.divider = true;
    }
}
function ContextMenuDivider_tsickle_Closure_declarations() {
    /** @type {?} */
    ContextMenuDivider.prototype.divider;
}
export const /** @type {?} */ CONTEXT_MENU_DIVIDER = new ContextMenuDivider();
