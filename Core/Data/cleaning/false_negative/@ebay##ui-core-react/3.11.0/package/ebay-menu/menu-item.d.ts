import { ComponentProps, FC } from 'react';
import { EbayMenuType } from './types';
export declare type MenuItemProps = Omit<ComponentProps<'div'>, 'onKeyDown'> & {
    type?: EbayMenuType;
    focused?: boolean;
    tabIndex?: number;
    checked?: boolean;
    value?: string;
    disabled?: boolean;
    badgeNumber?: number;
    badgeAriaLabel?: string;
};
declare const EbayMenuItem: FC<MenuItemProps>;
export default EbayMenuItem;
//# sourceMappingURL=menu-item.d.ts.map