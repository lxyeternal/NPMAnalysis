import { FC, HTMLProps, ReactNode } from 'react';
export declare type EbaySectionTitleProps = Omit<HTMLProps<HTMLDivElement>, 'title'> & {
    href?: string;
    ctaText?: ReactNode;
};
declare const EbaySectionTitle: FC<EbaySectionTitleProps>;
export default EbaySectionTitle;
//# sourceMappingURL=section-title.d.ts.map