export interface ISubject {
    postMessage(message: any, targetOrigin: string, transfer?: any[]): void;
    addEventListener(type: 'message', listener: (event: MessageEvent) => void): any;
    removeEventListener(type: 'message', listener?: any, options?: any): void;
}
