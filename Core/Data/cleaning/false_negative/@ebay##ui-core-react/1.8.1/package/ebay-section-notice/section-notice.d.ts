import React, { FC } from 'react';
declare type Props = React.HTMLProps<HTMLElement> & {
    status?: 'general' | 'none' | 'attention' | 'confirmation' | 'information';
    'aria-label'?: string;
    'aria-roledescription'?: string;
    className?: string;
};
declare const EbaySectionNotice: FC<Props>;
export default EbaySectionNotice;
//# sourceMappingURL=section-notice.d.ts.map