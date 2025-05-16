import React, { ComponentProps, FC } from 'react';
declare type CarouselProps = ComponentProps<'div'> & {
    className?: string;
    gap?: number;
    index?: number;
    imageTreatment?: boolean;
    itemsPerSlide?: number;
    a11yPreviousText?: string;
    a11yNextText?: string;
    onNext?: (event: React.SyntheticEvent) => void;
    onPrevious?: (event: React.SyntheticEvent) => void;
    onScroll?: ({ index }: {
        index: any;
    }) => void;
    onSlide?: ({ slide }: {
        slide: any;
    }) => void;
    onPlay?: (event: React.SyntheticEvent) => void;
    onPause?: (event: React.SyntheticEvent) => void;
};
declare const EbayCarousel: FC<CarouselProps>;
export default EbayCarousel;
//# sourceMappingURL=carousel.d.ts.map