import { ComponentProps, FC } from 'react';
export declare type SpinnerSize = 'small' | 'large';
declare type EbayProgressSpinnerProps = {
    size?: SpinnerSize;
    'aria-label'?: string;
};
declare type SpanProps = Omit<ComponentProps<'span'>, 'size'>;
declare const EbayProgressSpinner: FC<SpanProps & EbayProgressSpinnerProps>;
export default EbayProgressSpinner;
//# sourceMappingURL=progress-spinner.d.ts.map