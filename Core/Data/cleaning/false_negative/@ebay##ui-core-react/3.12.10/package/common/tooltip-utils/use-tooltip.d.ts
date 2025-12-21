import { RefObject } from 'react';
declare type UseTooltipArgs = {
    onExpand: () => void;
    onCollapse: () => void;
    initialExpanded?: boolean;
    hostRef?: RefObject<HTMLElement>;
};
declare type UseTooltip = {
    isExpanded: boolean;
    expandTooltip: () => void;
    collapseTooltip: () => void;
};
export declare const useTooltip: ({ onExpand, onCollapse, initialExpanded, hostRef }: UseTooltipArgs) => UseTooltip;
export {};
//# sourceMappingURL=use-tooltip.d.ts.map