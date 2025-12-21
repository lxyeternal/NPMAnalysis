import { Component, ComponentProps, ReactElement } from 'react';
import { Activation, Size } from './types';
declare type TabsProps = ComponentProps<'div'> & {
    index?: number;
    /** @deprecated Kept for backward-compatibility with eBayUI */
    fake?: boolean;
    size?: Size;
    activation?: Activation;
    onTabSelect?: (index: number) => void;
};
declare type State = {
    selectedIndex: number;
    focusedIndex: number;
};
declare class Tabs extends Component<TabsProps, State> {
    headings: HTMLElement[];
    constructor(props: TabsProps);
    componentDidUpdate(prevProps: TabsProps): void;
    onTabSelect(i: number): void;
    /**
     * Handle a11y for heading
     * https://ebay.gitbooks.io/mindpatterns/content/disclosure/tabs.html
     */
    onTabKeyDown(ev: KeyboardEvent, index: number): void;
    render(): ReactElement;
}
export default Tabs;
//# sourceMappingURL=tabs.d.ts.map