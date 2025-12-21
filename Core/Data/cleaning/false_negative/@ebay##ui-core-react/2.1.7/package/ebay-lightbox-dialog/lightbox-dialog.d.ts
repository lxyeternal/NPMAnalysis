import { FC } from 'react';
import { DialogBaseProps } from '../ebay-dialog-base';
declare type Mode = 'default' | 'mini';
export interface Props<T = any> extends DialogBaseProps<T> {
    open?: boolean;
    mode?: Mode;
    onOpen?: () => void;
    onClose?: () => void;
}
declare const EbayLightboxDialog: FC<Props>;
export default EbayLightboxDialog;
//# sourceMappingURL=lightbox-dialog.d.ts.map