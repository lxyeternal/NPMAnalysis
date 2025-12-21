/**
 *
 */
export interface ContextMenuItem {
    divider: boolean;
}
/**
 *
 */
export declare class ContextMenuAction implements ContextMenuItem {
    text: string;
    click: (context?: any) => any;
    disabled: boolean;
    icon: any;
    readonly divider: boolean;
    constructor(text: string, click: (context?: any) => any, disabled?: boolean, icon?: any);
}
/**
 *
 */
export declare class ContextMenuDivider implements ContextMenuItem {
    readonly divider: boolean;
}
export declare const CONTEXT_MENU_DIVIDER: ContextMenuDivider;
