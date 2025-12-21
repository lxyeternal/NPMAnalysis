import { MessageType } from "./message-type";
export declare type MessageId = string;
export declare const MESSAGE_ID_PREFIX = "xoc_";
/**
 *
 */
export declare class Message {
    type: MessageType;
    data: any;
    readonly id: MessageId;
    /**
     * 是否需要回复
     */
    needReply: boolean;
    constructor(type: MessageType, data?: any, id?: MessageId);
}
