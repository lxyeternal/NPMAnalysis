import React, { Dispatch, FC, MouseEvent } from 'react';
declare type Props = React.HTMLProps<HTMLElement> & {
    status?: 'general' | 'attention' | 'confirmation' | 'information';
    'aria-label'?: string;
    a11yDismissText?: string;
    onDismiss?: Dispatch<MouseEvent>;
};
declare const EbayPageNotice: FC<Props>;
export default EbayPageNotice;
//# sourceMappingURL=page-notice.d.ts.map