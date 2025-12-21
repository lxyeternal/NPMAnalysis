import { CSSProperties, FC } from 'react';
import { TooltipProps, PointerDirection } from '../common/tooltip-utils';
declare type TourtipProps = Omit<TooltipProps, 'ref'> & {
    a11yCloseText: string;
    pointer?: PointerDirection;
    onExpand?: () => void;
    onCollapse?: () => void;
    overlayStyle?: CSSProperties;
    'aria-label'?: string;
    className?: string;
};
declare const EbayTourtip: FC<TourtipProps>;
export default EbayTourtip;
//# sourceMappingURL=ebay-tourtip.d.ts.map