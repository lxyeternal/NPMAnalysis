import { ComponentProps, FC } from 'react';
import { EbayButtonProps } from '..';
export declare type EbayFakeMenuButtonVariant = 'overflow' | 'form' | 'button';
export declare type EbayFakeMenuButtonProps = {
    a11yText?: string;
    noToggleIcon?: boolean;
    expanded?: boolean;
    fixWidth?: boolean;
    reverse?: boolean;
    variant?: EbayFakeMenuButtonVariant;
    className?: string;
    onCollapse?: () => void;
    onExpand?: () => void;
    text?: string;
    type?: 'radio' | 'checkbox';
};
declare type ButtonProps = Omit<EbayButtonProps, 'variant'> & Omit<ComponentProps<'button'>, 'type'> & ComponentProps<'a'>;
declare type Props = ButtonProps & EbayFakeMenuButtonProps;
declare const EbayMenuButton: FC<Props>;
export default EbayMenuButton;
//# sourceMappingURL=menu-button.d.ts.map