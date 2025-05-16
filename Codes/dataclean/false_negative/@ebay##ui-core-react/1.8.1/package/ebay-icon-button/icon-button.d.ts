import { ComponentProps, FC } from 'react';
import { Icon } from '../ebay-icon';
export declare type EbayIconButtonProps = {
    href?: string;
    icon: Icon;
    badgeNumber?: number;
    badgeAriaLabel?: string;
    transparent?: boolean;
};
declare type HTMLButtonProps = ComponentProps<'button'>;
declare type HTMLAnchorProps = ComponentProps<'a'>;
declare type Props = EbayIconButtonProps & HTMLButtonProps & HTMLAnchorProps;
declare const EbayIconButton: FC<Props>;
export default EbayIconButton;
//# sourceMappingURL=icon-button.d.ts.map