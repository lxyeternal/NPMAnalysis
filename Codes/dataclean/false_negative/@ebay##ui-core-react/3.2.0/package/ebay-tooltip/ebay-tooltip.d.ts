import { CSSProperties, FC } from 'react';
import { TooltipProps, PointerDirection } from '../common/tooltip-utils';
declare type Props = Omit<TooltipProps, 'ref'> & {
    noHover?: boolean;
    onExpand?: () => void;
    onCollapse?: () => void;
    pointer?: PointerDirection;
    overlayStyle?: CSSProperties;
};
declare const EbayTooltip: FC<Props>;
export default EbayTooltip;
//# sourceMappingURL=ebay-tooltip.d.ts.map