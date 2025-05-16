import { KeyboardEventHandler, MouseEventHandler, ReactElement } from 'react';
import { DialogBaseProps } from '../../ebay-dialog-base';
export declare type EbaySnackbarDialogProps = Omit<DialogBaseProps<HTMLElement>, 'a11yCloseText'> & {
    layout?: 'row' | 'column';
    onOpen?: () => void;
    onClose?: () => void;
    onAction?: MouseEventHandler<HTMLButtonElement> & KeyboardEventHandler;
};
export declare const EbaySnackbarDialog: ({ className, onOpen, onClose, layout, open, children, onAction, ...rest }: EbaySnackbarDialogProps) => ReactElement;
//# sourceMappingURL=ebay-snackbar-dialog.d.ts.map