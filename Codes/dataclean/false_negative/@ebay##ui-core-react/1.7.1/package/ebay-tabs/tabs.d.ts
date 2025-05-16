import { ComponentProps, FC } from 'react';
import { Activation, Size } from './types';
declare type TabsProps = ComponentProps<'div'> & {
    index?: number;
    /** @deprecated Kept for backward-compatibility with eBayUI */
    fake?: boolean;
    size?: Size;
    activation?: Activation;
    onTabSelect?: (index: number) => void;
};
declare const Tabs: FC<TabsProps>;
export default Tabs;
//# sourceMappingURL=tabs.d.ts.map