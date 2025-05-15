import { Message } from "./message";
import { ISubject } from "./subject";
export interface IHandler {
    /**
     * 是否是一次性的
     */
    disposable?: boolean;
    handle(message: Message, source: ISubject): boolean;
}
