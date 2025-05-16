import { FC } from 'react';
import { DialogBaseProps } from '../ebay-dialog-base';
export interface Props<T = any> extends DialogBaseProps<T> {
    open?: boolean;
    confirmText: string;
    onOpen?: () => void;
    onConfirm?: () => void;
}
declare const EbayAlertDialog: FC<Props>;
export default EbayAlertDialog;
//# sourceMappingURL=alert-dialog.d.ts.map