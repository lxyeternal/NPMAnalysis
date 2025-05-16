import { ComponentProps, FC } from 'react';
export declare type EbayBadgeType = 'menu' | 'icon' | 'img';
declare type Props = ComponentProps<'span'> & {
    type?: EbayBadgeType;
    number: number;
};
declare const EbayBadge: FC<Props>;
export default EbayBadge;
//# sourceMappingURL=badge.d.ts.map