import { FC, ReactNode } from 'react';
import { StepState, StepType } from './types';
export declare type EbayProgressStepProps = {
    type?: StepType;
    state?: StepState;
    current?: boolean;
    number?: number;
    className?: string;
    children?: ReactNode;
};
declare const EbayProgressStep: FC<EbayProgressStepProps>;
export default EbayProgressStep;
//# sourceMappingURL=ebay-progress-step.d.ts.map