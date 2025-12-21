import { ComponentProps, FC } from 'react';
export declare type EbayFakeMenuItemProps = Omit<ComponentProps<'a'>, 'onKeyDown'> & {
    current?: boolean;
    disabled?: boolean;
    autoFocus?: boolean;
};
declare const EbayMenuItem: FC<EbayFakeMenuItemProps>;
export default EbayMenuItem;
//# sourceMappingURL=menu-item.d.ts.map