declare type UseTooltipArgs = {
    onExpand: () => void;
    onCollapse: () => void;
    initialExpanded?: boolean;
};
declare type UseTooltip = {
    isExpanded: boolean;
    expandTooltip: () => void;
    collapseTooltip: () => void;
};
export declare const useTooltip: ({ onExpand, onCollapse, initialExpanded }: UseTooltipArgs) => UseTooltip;
export {};
//# sourceMappingURL=use-tooltip.d.ts.map