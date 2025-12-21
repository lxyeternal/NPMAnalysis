import { ReactElement, ReactNode, RefObject } from 'react';
import { ListItemRef, MovementDirection, RelativeRect } from './types';
export declare function getRelativeRects(el: Element): RelativeRect;
export declare const isNativeScrolling: (el: Element) => boolean;
export declare const getMaxOffset: (items: ListItemRef[], slideWidth: number) => number;
export declare const getOffset: (items: ListItemRef[], index: number, slideWidth: number) => number;
export declare const alterChildren: (children: ReactNode, itemsRef: RefObject<Array<ListItemRef | null>>, itemsPerSlide?: number, slideWidth?: number, offset?: number, gap?: number) => ReactElement[];
/**
 * Gets the slide for a given index.
 * Defaults to the current index if none provided.
 */
export declare const getSlide: (activeIndex: number, itemsPerSlide?: number, nextIndex?: number) => undefined | number;
export declare const getNextIndex: (direction: MovementDirection, activeIndex: number, items?: ListItemRef[], slideWidth?: number, itemsPerSlide?: number) => number;
export declare const getClosestIndex: (scrollLeft: number, items: ListItemRef[], slideWidth: number, itemsPerSlide?: number, gap?: number) => number;
//# sourceMappingURL=helpers.d.ts.map