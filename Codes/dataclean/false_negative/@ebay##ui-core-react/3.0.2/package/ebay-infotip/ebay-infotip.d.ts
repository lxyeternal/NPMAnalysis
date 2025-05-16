import { CSSProperties, FC, ReactNode } from 'react';
import { PointerDirection } from '../common/tooltip-utils';
import { Icon } from '../ebay-icon';
import { Variant } from './types';
declare type InfotipProps = {
    variant?: Variant;
    icon?: Icon;
    disabled?: boolean;
    initialExpanded?: boolean;
    pointer?: PointerDirection;
    overlayStyle?: CSSProperties;
    onExpand?: () => void;
    onCollapse?: () => void;
    a11yCloseText: string;
    'aria-label'?: string;
    className?: string;
    children?: ReactNode;
};
declare const EbayInfotip: FC<InfotipProps>;
export default EbayInfotip;
//# sourceMappingURL=ebay-infotip.d.ts.map