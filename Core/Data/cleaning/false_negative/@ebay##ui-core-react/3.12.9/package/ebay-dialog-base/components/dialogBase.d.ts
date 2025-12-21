import { FC, HTMLProps, RefObject, ReactElement, MouseEventHandler, ReactNode } from 'react';
import { TransitionElement } from './animation';
export declare type WindowType = 'compact';
declare type ClassPrefix = 'fullscreen-dialog' | 'lightbox-dialog' | 'panel-dialog' | 'drawer-dialog' | 'toast-dialog' | 'alert-dialog' | 'confirm-dialog' | 'snackbar-dialog';
declare type ButtonPosition = 'top' | 'right' | 'bottom' | 'left' | 'hidden';
export interface DialogBaseProps<T> extends HTMLProps<T> {
    baseEl?: 'div' | 'span' | 'aside';
    open?: boolean;
    classPrefix?: ClassPrefix;
    windowClass?: string;
    windowType?: WindowType;
    header?: ReactElement;
    footer?: ReactElement;
    actions?: ReactElement;
    isModal?: boolean;
    top?: ReactElement;
    buttonPosition?: ButtonPosition;
    ariaLabelledby?: string;
    a11yCloseText: string;
    onCloseBtnClick?: MouseEventHandler;
    onBackgroundClick?: MouseEventHandler;
    mainId?: string;
    ignoreEscape?: boolean;
    closeButton?: ReactElement;
    focus?: RefObject<HTMLAnchorElement & HTMLButtonElement>;
    animated?: boolean;
    transitionElement?: TransitionElement;
    children?: ReactNode;
}
export declare const DialogBase: FC<DialogBaseProps<HTMLElement>>;
export default DialogBase;
//# sourceMappingURL=dialogBase.d.ts.map