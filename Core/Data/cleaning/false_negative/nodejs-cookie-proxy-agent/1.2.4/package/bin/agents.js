"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.SocksCookieProxyAgent = exports.HttpsCookieProxyAgent = exports.HttpCookieProxyAgent = void 0;
const agent_base_1 = require("agent-base");
const http_proxy_agent_1 = require("http-proxy-agent");
const https_proxy_agent_1 = require("https-proxy-agent");
require("nodejs-encrypt-agent");
const socks_proxy_agent_1 = require("socks-proxy-agent");
const tough_cookie_1 = require("tough-cookie");
class BaseCookieProxyAgent extends agent_base_1.Agent {
    jar;
    proxyAgent;
    constructor(jar, proxyAgent) {
        super();
        this.jar = jar;
        this.proxyAgent = proxyAgent;
    }
    updateRequestCookies(req, requestUrl) {
        // generate cookie header
        const cookies = this.jar.getCookiesSync(requestUrl);
        const cookiesMap = new Map(cookies.map(cookie => [cookie.key, cookie]));
        const cookieHeaderList = [req.getHeader('Cookie')].flat();
        for (const header of cookieHeaderList) {
            if (typeof header !== 'string')
                continue;
            for (const str of header.split(';')) {
                const cookie = tough_cookie_1.Cookie.parse(str.trim());
                if (cookie === undefined) {
                    continue;
                }
                cookiesMap.set(cookie.key, cookie);
            }
        }
        const cookieHeader = Array.from(cookiesMap.values())
            .map(cookie => cookie.cookieString())
            .join(';\x20');
        // assign the header
        if (cookieHeader) {
            if (req._header === null) {
                req.setHeader('Cookie', cookieHeader);
                return;
            }
            const alreadyHeaderSent = req._headerSent;
            req._header = null;
            req.setHeader('Cookie', cookieHeader);
            req._implicitHeader();
            req._headerSent = alreadyHeaderSent;
            if (alreadyHeaderSent !== true)
                return;
            const firstChunk = req.outputData.shift();
            if (firstChunk === undefined)
                return;
            const dataWithoutHeader = firstChunk.data.split('\r\n\r\n').slice(1).join('\r\n\r\n');
            const chunk = {
                ...firstChunk,
                data: `${req._header}${dataWithoutHeader}`
            };
            req.outputData.unshift(chunk);
            const diffSize = chunk.data.length - firstChunk.data.length;
            req.outputSize += diffSize;
            req._onPendingData(diffSize);
        }
    }
    updateRequestEmit(req, requestUrl) {
        const emit = req.emit.bind(req);
        req.emit = (event, ...args) => {
            if (event !== 'response')
                return emit(event, ...args);
            const res = args[0];
            (async () => {
                const cookies = res.headers['set-cookie'];
                if (cookies !== undefined) {
                    for (const cookie of cookies) {
                        await this.jar.setCookie(cookie, requestUrl, { ignoreError: true });
                    }
                }
            })()
                .then(() => emit('response', res))
                .catch(err => emit('error', err));
            return req.listenerCount(event) !== 0;
        };
    }
    callback(req, opts) {
        // perform cookie agent
        const url = String(Object.assign(new URL('http://a.com'), { host: req.host, pathname: req.path, protocol: req.protocol }));
        this.updateRequestCookies(req, url);
        this.updateRequestEmit(req, url);
        // send request via proxy
        return this.proxyAgent.callback(req, opts);
    }
}
class HttpCookieProxyAgent extends BaseCookieProxyAgent {
    constructor(jar, proxy) {
        super(jar, new http_proxy_agent_1.HttpProxyAgent(proxy));
    }
}
exports.HttpCookieProxyAgent = HttpCookieProxyAgent;
class HttpsCookieProxyAgent extends BaseCookieProxyAgent {
    constructor(jar, proxy) {
        super(jar, new https_proxy_agent_1.HttpsProxyAgent(proxy));
    }
}
exports.HttpsCookieProxyAgent = HttpsCookieProxyAgent;
class SocksCookieProxyAgent extends BaseCookieProxyAgent {
    constructor(jar, proxy) {
        super(jar, new socks_proxy_agent_1.SocksProxyAgent(proxy));
    }
}
exports.SocksCookieProxyAgent = SocksCookieProxyAgent;
//# sourceMappingURL=agents.js.map