import { FC, ComponentProps } from 'react';
export declare type SignalStatus = 'neutral' | 'trustworthy' | 'time-sensitive' | 'recent';
declare type Props = ComponentProps<'span'> & {
    status?: SignalStatus;
};
declare const EbaySignal: FC<Props>;
export default EbaySignal;
//# sourceMappingURL=signal.d.ts.map