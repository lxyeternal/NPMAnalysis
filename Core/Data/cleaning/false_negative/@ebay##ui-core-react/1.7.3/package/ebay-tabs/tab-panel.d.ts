import { ComponentProps, FC } from 'react';
declare type TabPanelProps = ComponentProps<'div'> & {
    index?: number;
    parentId?: string;
    selected?: boolean;
    fake?: boolean;
};
declare const TabPanel: FC<TabPanelProps>;
export default TabPanel;
//# sourceMappingURL=tab-panel.d.ts.map