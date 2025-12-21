import { ComponentProps, FC, ReactNode } from 'react';
declare type BreadcrumbProps = ComponentProps<'div'> & {
    /**
     * Breadcrumbs expects `<EbayBreadcrumbItem/>` as children.
     * Other elements will not work.
     *
     * @see Docs https://github.com/eBay/ebayui-core-react/tree/main/src/components/ebay-breadcrumb#usage
     */
    children: ReactNode;
    id?: string;
    a11yHeadingTag?: keyof JSX.IntrinsicElements;
    a11yHeadingText?: string;
    onSelect?: (event: MouseEvent | KeyboardEvent, target: HTMLElement) => void;
};
declare const Breadcrumbs: FC<BreadcrumbProps>;
export default Breadcrumbs;
//# sourceMappingURL=breadcrumbs.d.ts.map