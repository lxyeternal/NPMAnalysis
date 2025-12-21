import { ComponentProps, FC } from 'react';
declare type TabProps = ComponentProps<'li'> & ComponentProps<'div'> & {
    index?: number;
    parentId?: string;
    selected?: boolean;
    href?: string;
    onClick?: () => void;
    onKeyDown?: () => void;
    refCallback?: () => void;
};
declare const Tab: FC<TabProps>;
export default Tab;
//# sourceMappingURL=tab.d.ts.map