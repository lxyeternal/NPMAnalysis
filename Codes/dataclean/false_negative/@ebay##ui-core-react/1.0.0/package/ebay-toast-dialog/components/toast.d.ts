import { MouseEventHandler, KeyboardEventHandler, FC } from 'react';
import { DialogBaseProps } from '../../ebay-dialog-base';
export declare type EbayToastProps = DialogBaseProps<HTMLElement> & {
    onClose?: MouseEventHandler<HTMLButtonElement> & KeyboardEventHandler;
};
export declare const EbayToast: FC<EbayToastProps>;
export default EbayToast;
//# sourceMappingURL=toast.d.ts.map