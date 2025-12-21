import { ComponentProps, FC } from 'react';
import { PaginationVariant } from './types';
declare type PaginationCallback = (e?: Event, value?: string) => void;
declare type PaginationProps = Omit<ComponentProps<'nav'>, 'onSelect'> & {
    id?: string;
    a11yPreviousText?: string;
    a11yNextText?: string;
    a11yCurrentText?: string;
    onPrevious?: PaginationCallback;
    onNext?: PaginationCallback;
    onSelect?: (e?: Event, value?: string, index?: number) => void;
    variant?: PaginationVariant;
    fluid?: boolean;
};
declare const EbayPagination: FC<PaginationProps>;
export default EbayPagination;
//# sourceMappingURL=pagination.d.ts.map