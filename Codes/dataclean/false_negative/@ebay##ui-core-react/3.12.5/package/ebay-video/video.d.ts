import { ComponentProps, FC, SyntheticEvent } from 'react';
import { VideoAction, VideoPlayView } from './types';
export declare type EbayVideoProps = ComponentProps<'video'> & {
    width?: number;
    height?: number;
    thumbnail?: string;
    action?: VideoAction;
    volume?: number;
    muted?: boolean;
    volumeSlider?: boolean;
    hideReportButton?: boolean;
    playView?: VideoPlayView;
    cdnUrl?: string;
    cssUrl?: string;
    cdnVersion?: string;
    a11yLoadText: string;
    a11yPlayText: string;
    errorText: string;
    reportText?: string;
    onLoadError?: (err: Error) => void;
    onPlay?: (e: SyntheticEvent, { player: Player }: {
        player: any;
    }) => void;
    onVolumeChange?: (e: SyntheticEvent, { volume: number, muted: boolean }: {
        volume: any;
        muted: any;
    }) => void;
    onReport?: () => void;
};
declare const EbayVideo: FC<EbayVideoProps>;
export default EbayVideo;
//# sourceMappingURL=video.d.ts.map