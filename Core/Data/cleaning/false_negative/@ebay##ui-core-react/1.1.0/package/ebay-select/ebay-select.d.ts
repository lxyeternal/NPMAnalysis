import { ChangeEvent, ComponentProps, FC } from 'react';
declare type SelectValue = string | ReadonlyArray<string> | number;
export declare type EbaySelectProps = ComponentProps<'select'> & {
    borderless?: boolean;
    defaultValue?: SelectValue;
    onChange?: (e: ChangeEvent<HTMLSelectElement>, selectedIndex: number, newValue: SelectValue) => void;
    floatingLabel?: string;
    inputSize?: 'default' | 'large';
    invalid?: boolean;
};
declare const EbaySelect: FC<EbaySelectProps>;
export default EbaySelect;
//# sourceMappingURL=ebay-select.d.ts.map