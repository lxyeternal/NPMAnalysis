import { ComponentProps, FC, MouseEvent } from 'react';
import { Icon } from '../ebay-icon';
declare type HTMLButtonProps = ComponentProps<'button'>;
export declare type ExpandButtonProps = HTMLButtonProps & {
    borderless?: boolean;
    icon?: Icon;
    onExpand?: () => void;
    onCollapse?: () => void;
    onClick?: (e: MouseEvent) => void;
};
declare const EbayExpandButton: FC<ExpandButtonProps>;
export default EbayExpandButton;
//# sourceMappingURL=expand-button.d.ts.map