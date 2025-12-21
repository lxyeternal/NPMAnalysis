import { ChangeEvent, ComponentProps, FC } from 'react';
declare type Size = 'default' | 'large';
declare type EbayRadioProps = {
    size?: Size;
    onChange?: (event: ChangeEvent<HTMLInputElement>, value: string | number) => void;
};
declare type InputProps = Omit<ComponentProps<'input'>, 'size'>;
declare const EbayRadio: FC<InputProps & EbayRadioProps>;
export default EbayRadio;
//# sourceMappingURL=radio.d.ts.map