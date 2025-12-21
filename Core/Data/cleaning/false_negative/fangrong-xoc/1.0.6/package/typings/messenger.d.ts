import { Message } from "./message";
import { ISubject } from "./subject";
import { MessageType } from "./message-type";
import { IHandler } from "./handler";
export declare class Messenger {
    private sender;
    private handlers;
    private messageEventListener;
    constructor(sender: ISubject);
    post(target: ISubject, messageType: MessageType, data: any, callback?: (message: Message) => void): void;
    postMessage(target: ISubject, message: Message, callback?: (message: Message) => void): void;
    createMessage(type: MessageType, data?: any): Message;
    addHandler(handler: IHandler): void;
    dispose(): void;
}
