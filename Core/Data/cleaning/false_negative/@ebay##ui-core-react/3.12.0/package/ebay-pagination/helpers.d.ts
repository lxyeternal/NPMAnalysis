import { ItemState, PaginationVariant } from './types';
export declare function pageNumbersAround(totalPages: number, selectedPage: number, maxVisiblePages?: number, variant?: PaginationVariant): ItemState[];
export declare function calcPageState(selectedPage: number, visiblePages: number, totalPages: number, variant?: PaginationVariant): ItemState[];
/**
 * Calculates the maximum width for an element within its container.
 *
 * Based on eBayUI Core Marko implementation.
 * See https://github.com/eBay/ebayui-core/blob/v8.6.0/src/components/ebay-pagination/component.js#L119-L132
 */
export declare function getMaxWidth(el?: HTMLElement): number;
//# sourceMappingURL=helpers.d.ts.map