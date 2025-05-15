var MessageType;
(function (MessageType) {
    MessageType[MessageType["Register"] = 0] = "Register";
    MessageType[MessageType["Navigation"] = 1] = "Navigation";
})(MessageType || (MessageType = {}));

var MESSAGE_ID_PREFIX = 'xoc_';
/**
 *
 */
var Message = /** @class */ (function () {
    function Message(type, data, id) {
        this.type = type;
        this.data = data;
        /**
         * 是否需要回复
         */
        this.needReply = false;
        this.id = (undefined === id) ? (MESSAGE_ID_PREFIX + (new Date).getTime()) : id;
    }
    return Message;
}());

var Messenger = /** @class */ (function () {
    function Messenger(sender) {
        var _this = this;
        this.sender = sender;
        this.messageEventListener = function (ev) {
            var message = extractMessage(ev);
            if (!message)
                return;
            for (var i = _this.handlers.length - 1; i >= 0; i--) {
                var handler = _this.handlers[i];
                var handled = handler.handle(message, ev.source);
                if (handler.disposable) {
                    _this.handlers.splice(i, 1);
                }
                if (handled)
                    break;
            }
        };
        this.handlers = [];
        this.sender.addEventListener('message', this.messageEventListener);
    }
    Messenger.prototype.post = function (target, messageType, data, callback) {
        var message = this.createMessage(messageType, data);
        return this.postMessage(target, message, callback);
    };
    Messenger.prototype.postMessage = function (target, message, callback) {
        if ('function' === typeof callback) {
            var handler = {
                disposable: true,
                handle: function (m) {
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
    };
    Messenger.prototype.createMessage = function (type, data) {
        return new Message(type, data);
    };
    Messenger.prototype.addHandler = function (handler) {
        this.handlers = this.handlers || [];
        this.handlers.push(handler);
    };
    Messenger.prototype.dispose = function () {
        this.handlers = null;
        this.sender.removeEventListener('message', this.messageEventListener);
    };
    return Messenger;
}());
function extractMessage(ev) {
    var data = ev.data || {};
    var id = data.id;
    if (id && id.startsWith(MESSAGE_ID_PREFIX)) {
        return data;
    }
    return null;
}

export { MessageType, Messenger };
