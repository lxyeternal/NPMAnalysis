var MessageType;
(function (MessageType) {
    MessageType[MessageType["Register"] = 0] = "Register";
    MessageType[MessageType["Navigation"] = 1] = "Navigation";
})(MessageType || (MessageType = {}));

const MESSAGE_ID_PREFIX = 'xoc_';
/**
 *
 */
class Message {
    constructor(type, data, id) {
        this.type = type;
        this.data = data;
        /**
         * 是否需要回复
         */
        this.needReply = false;
        this.id = (undefined === id) ? (MESSAGE_ID_PREFIX + (new Date).getTime()) : id;
    }
}

class Messenger {
    constructor(sender) {
        this.sender = sender;
        this.messageEventListener = (ev) => {
            let message = extractMessage(ev);
            if (!message)
                return;
            for (let i = this.handlers.length - 1; i >= 0; i--) {
                let handler = this.handlers[i];
                let handled = handler.handle(message, ev.source);
                if (handler.disposable) {
                    this.handlers.splice(i, 1);
                }
                if (handled)
                    break;
            }
        };
        this.handlers = [];
        this.sender.addEventListener('message', this.messageEventListener);
    }
    post(target, messageType, data, callback) {
        let message = this.createMessage(messageType, data);
        return this.postMessage(target, message, callback);
    }
    postMessage(target, message, callback) {
        if ('function' === typeof callback) {
            let handler = {
                disposable: true,
                handle(m) {
                    if (m.id === message.id) {
                        callback(message);
                        return true;
                    }
                    return false;
                }
            };
            this.addHandler(handler);
        }
        target.postMessage(message, '*');
    }
    createMessage(type, data) {
        return new Message(type, data);
    }
    addHandler(handler) {
        this.handlers = this.handlers || [];
        this.handlers.push(handler);
    }
    dispose() {
        this.handlers = null;
        this.sender.removeEventListener('message', this.messageEventListener);
    }
}
function extractMessage(ev) {
    let data = ev.data || {};
    let id = data.id;
    if (id && id.startsWith(MESSAGE_ID_PREFIX)) {
        return data;
    }
    return null;
}

export { MessageType, Messenger };
