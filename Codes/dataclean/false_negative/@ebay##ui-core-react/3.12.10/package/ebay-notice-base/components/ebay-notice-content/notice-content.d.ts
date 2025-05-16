/**
 * This Component is used only for finding it as a child of EbayInlineNotice, EbaySectionNotice, or EbayPageNotice
 * and pass the properties to NoticeContent
 */
import { FC } from 'react';
import { NoticeContentProps } from '../../../common/notice-utils/notice-content';
declare type Props = Omit<NoticeContentProps, 'type'>;
declare const EbayNoticeContent: FC<Props>;
export default EbayNoticeContent;
//# sourceMappingURL=notice-content.d.ts.map