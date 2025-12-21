/// <reference types="react" />
interface DialogAnimationHookProps {
    open?: boolean;
    transitionElement?: TransitionElement;
    classPrefix: string;
    dialogRef: React.RefObject<HTMLElement>;
    dialogWindowRef: React.RefObject<HTMLElement>;
    enabled?: boolean;
    onTransitionEnd: () => void;
}
export declare type TransitionElement = 'window' | 'root';
export declare function useDialogAnimation({ open, classPrefix, transitionElement, dialogRef, dialogWindowRef, enabled, onTransitionEnd }: DialogAnimationHookProps): void;
export {};
//# sourceMappingURL=animation.d.ts.map