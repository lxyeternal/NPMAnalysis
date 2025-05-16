import { ComponentProps, FC, MouseEvent, RefObject } from 'react';
declare type EbayListboxButtonOptionProps = ComponentProps<'input'> & {
    selected?: boolean;
    index?: number;
    onClick?: (event: MouseEvent<HTMLDivElement>, value: any, index: number) => void;
    innerRef?: RefObject<HTMLDivElement>;
};
declare const ListboxOption: FC<EbayListboxButtonOptionProps>;
export default ListboxOption;
//# sourceMappingURL=listbox-button-option.d.ts.map