import { FC, ChangeEvent, ComponentProps } from 'react';
declare type Props = ComponentProps<'input'> & {
    onChange?: (e: ChangeEvent<HTMLInputElement>, value: string | number, checked: boolean) => void;
};
declare const EbaySwitch: FC<Props>;
export default EbaySwitch;
//# sourceMappingURL=ebay-switch.d.ts.map