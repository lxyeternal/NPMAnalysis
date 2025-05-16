import { ComponentProps, FC, ReactNode } from 'react';
import { Icon } from '../ebay-icon';
declare type Props = ComponentProps<'div'> & {
    ctaText?: ReactNode;
    href?: string;
    icon?: Icon;
};
declare const Cta: FC<Props>;
export default Cta;
//# sourceMappingURL=cta.d.ts.map