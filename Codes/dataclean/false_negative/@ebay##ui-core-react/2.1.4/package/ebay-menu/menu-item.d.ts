import { ComponentProps, FC } from 'react';
export declare type MenuItemProps = Omit<ComponentProps<'div'>, 'onKeyDown'> & {
    focused?: boolean;
    tabIndex?: number;
    checked?: boolean;
    value?: string;
    disabled?: boolean;
    badgeNumber?: number;
};
declare const EbayMenuItem: FC<MenuItemProps>;
export default EbayMenuItem;
//# sourceMappingURL=menu-item.d.ts.map