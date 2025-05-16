import { ComponentProps, FC, KeyboardEvent, MouseEvent } from 'react';
declare type SpanProps = Omit<ComponentProps<'div'>, 'onKeyDown'>;
declare type Callback = (event: KeyboardEvent | MouseEvent, i: number) => void;
declare type Props = SpanProps & {
    itemMatchesUrl?: boolean;
    onKeyDown?: Callback;
    onSelect?: Callback;
};
declare const EbayFakeMenu: FC<Props>;
export default EbayFakeMenu;
//# sourceMappingURL=menu.d.ts.map