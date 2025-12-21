import { FC, ReactNode } from 'react';
import { NoticeStatus } from './types';
declare type Props = {
    status?: NoticeStatus;
    onNoticeShow?: () => void;
    'aria-label': string;
    hidden?: boolean;
    className?: string;
    children?: ReactNode;
};
declare const EbayInlineNotice: FC<Props>;
export default EbayInlineNotice;
//# sourceMappingURL=inline-notice.d.ts.map