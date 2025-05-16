import { FC } from 'react';
import { DialogBaseProps } from '../ebay-dialog-base';
export interface Props<T = any> extends DialogBaseProps<T> {
    open?: boolean;
    confirmText: string;
    rejectText: string;
    onOpen?: () => void;
    onReject?: () => void;
    onConfirm?: () => void;
}
declare const EbayConfirmDialog: FC<Props>;
export default EbayConfirmDialog;
//# sourceMappingURL=confirm-dialog.d.ts.map