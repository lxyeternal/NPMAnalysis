import { ChangeEvent, ComponentProps, FC, MouseEvent } from 'react';
declare type Props = ComponentProps<'div'> & {
    a11yText?: string;
    value?: string;
    a11yStarText?: string[];
    disabled?: boolean;
    name?: string;
    onKeyDown?: (e: MouseEvent, value: number) => void;
    onChange?: (event: ChangeEvent<HTMLInputElement>, value: string | number) => void;
    onFocus?: (event: ChangeEvent<HTMLInputElement>, value: string | number) => void;
};
declare const EbayStarRatingSelect: FC<Props>;
export default EbayStarRatingSelect;
//# sourceMappingURL=star-rating-select.d.ts.map