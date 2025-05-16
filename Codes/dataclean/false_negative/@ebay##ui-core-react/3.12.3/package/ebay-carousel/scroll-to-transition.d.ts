/**
 * Checks on an interval to see if the element is scrolling.
 * When the scrolling has finished it then calls the function.
 *
 * @param {HTMLElement} el The element which scrolls.
 * @param {(offset: number)=>{}} fn The function to call after scrolling completes.
 * @return {function} A function to cancel the scroll listener.
 */
declare type ReturnFunctionType = () => void;
/**
 * Utility to animate scroll position of an element using an `ease-out` curve over 250ms.
 * Cancels the animation if the user touches back down.
 *
 * @param {HTMLElement} el The element to scroll.
 * @param {number} to The offset to animate to.
 * @param {function} fn A function that will be called after the transition completes.
 * @return {function} A function that cancels the transition.
 */
export declare function scrollTransition(el: HTMLElement, to: number, fn: () => void): ReturnFunctionType;
export {};
//# sourceMappingURL=scroll-to-transition.d.ts.map