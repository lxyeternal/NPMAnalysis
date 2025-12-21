/// <reference types="node" />
import { Agent, ClientRequest, RequestOptions } from 'agent-base';
import createHttpProxyAgent, { HttpProxyAgent } from 'http-proxy-agent';
import createHttpsProxyAgent, { HttpsProxyAgent } from 'https-proxy-agent';
import { Socket } from 'net';
import 'nodejs-encrypt-agent';
import createSocksProxyAgent, { SocksProxyAgent } from 'socks-proxy-agent';
import { CookieJar } from 'tough-cookie';
declare module 'agent-base' {
    interface ClientRequest {
        _header: string | null;
        _headerSent: boolean;
        _implicitHeader(): void;
        _onPendingData(amount: number): void;
        outputData: Array<{
            callback: unknown;
            data: string;
            encoding: string;
        }>;
        outputSize: number;
    }
}
declare abstract class BaseCookieProxyAgent extends Agent {
    private readonly jar;
    private readonly proxyAgent;
    constructor(jar: CookieJar, proxyAgent: HttpProxyAgent | HttpsProxyAgent | SocksProxyAgent);
    private updateRequestCookies;
    private updateRequestEmit;
    callback(req: ClientRequest, opts: RequestOptions): Promise<Socket>;
}
export declare class HttpCookieProxyAgent extends BaseCookieProxyAgent {
    constructor(jar: CookieJar, proxy: string | createHttpProxyAgent.HttpProxyAgentOptions);
}
export declare class HttpsCookieProxyAgent extends BaseCookieProxyAgent {
    constructor(jar: CookieJar, proxy: string | createHttpsProxyAgent.HttpsProxyAgentOptions);
}
export declare class SocksCookieProxyAgent extends BaseCookieProxyAgent {
    constructor(jar: CookieJar, proxy: string | createSocksProxyAgent.SocksProxyAgentOptions);
}
export {};
