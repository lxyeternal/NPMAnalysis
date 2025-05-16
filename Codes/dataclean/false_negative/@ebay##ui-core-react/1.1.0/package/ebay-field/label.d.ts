import { ComponentProps, FC } from 'react';
import { LabelPosition } from './types';
export declare type Props = {
    className?: string;
    stacked?: boolean;
    required?: boolean;
    position?: LabelPosition;
} & ComponentProps<'label'>;
declare const Label: FC<Props>;
export default Label;
//# sourceMappingURL=label.d.ts.map