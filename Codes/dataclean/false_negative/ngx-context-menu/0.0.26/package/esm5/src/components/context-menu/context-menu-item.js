/**
 *
 */
var ContextMenuAction = /** @class */ (function () {
    /**
     * @param {?} text
     * @param {?} click
     * @param {?=} disabled
     * @param {?=} icon
     */
    function ContextMenuAction(text, click, disabled, icon) {
        this.text = text;
        this.click = click;
        this.disabled = disabled;
        this.icon = icon;
        this.divider = false;
    }
    return ContextMenuAction;
}());
export { ContextMenuAction };
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
var ContextMenuDivider = /** @class */ (function () {
    function ContextMenuDivider() {
        this.divider = true;
    }
    return ContextMenuDivider;
}());
export { ContextMenuDivider };
function ContextMenuDivider_tsickle_Closure_declarations() {
    /** @type {?} */
    ContextMenuDivider.prototype.divider;
}
export var /** @type {?} */ CONTEXT_MENU_DIVIDER = new ContextMenuDivider();
