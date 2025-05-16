import { FC, RefObject, ReactNode, ComponentProps } from 'react';
declare type InputRef = RefObject<HTMLSelectElement | HTMLTextAreaElement | HTMLInputElement> | any;
declare type FloatingLabelHookProps = {
    inputId?: string;
    ref?: InputRef;
    disabled?: boolean;
    label?: string;
    inputSize?: 'default' | 'large';
    inputValue?: ComponentProps<'input'>['value'];
    className?: string;
    placeholder?: string;
    invalid?: boolean;
};
declare type FloatingLabelHookReturn = {
    label: ReactNode;
    onBlur: () => void;
    onFocus: () => void;
    Container: FC<{
        children?: ReactNode;
    }>;
    ref: InputRef;
    placeholder: string;
};
export declare function useFloatingLabel({ ref, inputId, className, disabled, label, inputSize, inputValue, placeholder, invalid }: FloatingLabelHookProps): FloatingLabelHookReturn;
export {};
//# sourceMappingURL=hooks.d.ts.map