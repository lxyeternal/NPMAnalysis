import { FC, CSSProperties, ReactNode } from 'react';
import { PointerDirection, TooltipType } from './types';
declare type TooltipContentProps = {
    id?: string;
    type?: TooltipType;
    style?: CSSProperties;
    pointer?: PointerDirection;
    showCloseButton?: boolean;
    a11yCloseText?: string;
    onClose?: () => void;
    children?: ReactNode;
};
declare const TooltipContent: FC<TooltipContentProps>;
export default TooltipContent;
//# sourceMappingURL=tooltip-content.d.ts.map