import { FC, ReactNode, RefObject } from 'react';
import { ListItemRef } from './types';
declare type CarouselListProps = {
    gap?: number;
    itemsPerSlide: number;
    slideWidth: number;
    offset: number;
    activeIndex: number;
    nextControlDisabled?: boolean;
    className?: string;
    itemsRef?: RefObject<Array<ListItemRef | null>>;
    children: ReactNode;
    onSetActiveIndex: (index: number) => void;
    onScroll?: ({ index }: {
        index: any;
    }) => void;
};
declare const CarouselList: FC<CarouselListProps>;
export default CarouselList;
//# sourceMappingURL=carousel-list.d.ts.map