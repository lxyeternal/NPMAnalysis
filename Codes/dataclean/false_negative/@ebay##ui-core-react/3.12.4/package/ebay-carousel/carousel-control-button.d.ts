import { FC, SyntheticEvent } from 'react';
import { CarouselControlType } from './types';
declare type CarouselControlProps = {
    label?: string;
    hidden?: boolean;
    type: CarouselControlType;
    disabled?: boolean;
    onClick: (event: SyntheticEvent<HTMLButtonElement>, { direction }: {
        direction: any;
    }) => void;
};
declare const CarouselControlButton: FC<CarouselControlProps>;
export default CarouselControlButton;
//# sourceMappingURL=carousel-control-button.d.ts.map