import { FC, RefObject } from 'react';
import { DialogBaseProps } from '../../ebay-dialog-base';
export interface EbayDrawerProps<T> extends DialogBaseProps<T> {
    expanded?: boolean;
    open?: boolean;
    noHandle?: boolean;
    focus?: RefObject<HTMLAnchorElement & HTMLButtonElement>;
    a11yMinimizeText: string;
    a11yMaximizeText: string;
    onShow?: () => void;
    onClose?: () => void;
    onExpanded?: () => void;
    onCollapsed?: () => void;
}
declare const EbayDrawerDialog: FC<EbayDrawerProps<any>>;
export default EbayDrawerDialog;
//# sourceMappingURL=drawer.d.ts.map