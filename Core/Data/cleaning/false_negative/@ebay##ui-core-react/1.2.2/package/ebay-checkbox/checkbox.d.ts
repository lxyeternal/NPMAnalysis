import { FC, ChangeEvent, ComponentProps } from 'react';
declare type Size = 'default' | 'large';
declare type InputProps = Omit<ComponentProps<'input'>, 'size'>;
declare type EbayCheckboxProps = {
    size?: Size;
    onChange?: (e: ChangeEvent<HTMLInputElement>, value: string | number, checked: boolean) => void;
};
declare const EbayCheckbox: FC<InputProps & EbayCheckboxProps>;
export default EbayCheckbox;
//# sourceMappingURL=checkbox.d.ts.map