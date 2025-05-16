import { FC } from 'react';
import { DialogBaseProps } from '../ebay-dialog-base';
declare type Position = 'start' | 'end';
export interface Props<T = any> extends DialogBaseProps<T> {
    open?: boolean;
    animated?: boolean;
    position?: Position;
    onOpen?: () => void;
    onClose?: () => void;
}
declare const EbayPanelDialog: FC<Props>;
export default EbayPanelDialog;
//# sourceMappingURL=panel-dialog.d.ts.map