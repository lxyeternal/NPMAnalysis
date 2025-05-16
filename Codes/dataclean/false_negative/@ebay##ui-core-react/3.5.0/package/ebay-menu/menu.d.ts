import { ComponentProps, FC } from 'react';
import { EbayMenuType, EbayMenuPriority } from './index';
declare type SpanProps = Omit<ComponentProps<'span'>, 'onKeyDown' | 'onChange'>;
declare type Callback = (i: number, checked: boolean) => void;
declare type Props = SpanProps & {
    type?: EbayMenuType;
    priority?: EbayMenuPriority;
    checked?: number;
    onKeyDown?: Callback;
    onSelect?: Callback;
    onChange?: Callback;
};
declare const EbayMenu: FC<Props>;
export default EbayMenu;
//# sourceMappingURL=menu.d.ts.map