import { ComponentProps, FC, KeyboardEvent } from 'react';
declare type EbayListboxButtonProps = ComponentProps<'input'> & {
    borderless?: boolean;
    fluid?: boolean;
    maxHeight?: string;
    prefixId?: string;
    floatingLabel?: string;
    onSelect?: (e: MouseEvent | KeyboardEvent, value: any, index: number) => void;
};
declare const ListboxButton: FC<EbayListboxButtonProps>;
export default ListboxButton;
//# sourceMappingURL=listbox-button.d.ts.map