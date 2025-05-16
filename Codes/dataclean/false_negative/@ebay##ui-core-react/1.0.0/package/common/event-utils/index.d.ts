declare type Callback = () => void;
export declare function handleEnterKeydown(e: KeyboardEvent, callback: Callback): void;
export declare function handleActionKeydown(e: KeyboardEvent, callback: Callback): void;
export declare function handleEscapeKeydown(e: KeyboardEvent, callback: Callback): void;
export declare function handleUpDownArrowsKeydown(e: KeyboardEvent, callback: Callback): void;
export declare function handleLeftRightArrowsKeydown(e: KeyboardEvent, callback: Callback): void;
export declare function handleTextInput(e: KeyboardEvent, callback: Callback): void;
export declare function preventDefaultIfHijax(e: KeyboardEvent, hijax: boolean): void;
declare type Handler = (e: KeyboardEvent) => void;
export declare function addEventListener(_: unknown, handler: Handler): void;
export declare function removeEventListener(_: unknown, handler: Handler): void;
export declare function handleResize(e: KeyboardEvent): void;
export declare function wrapEvent(parentEventHandler: Handler, localEventHandler: Handler): (e: KeyboardEvent) => void;
export {};
//# sourceMappingURL=index.d.ts.map