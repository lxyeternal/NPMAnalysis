const { buildCookies } = require('./cookies');
const { fillTarget, selectElement } = require('./dom');
const { fetchLeadInfo, trackEvent } = require('./fetcher');
const { getUrlParams, removeUrlParams } = require('./url');
const { isNil, isFunction, addLocationChangeEvent } = require('./utils');

class ZenfiSDK {
  constructor({ partnerName, cookiesDomain, targets } = {}) {
    this._id = null;
    this._token = null;
    this.leadInfo = null;
    this.partnerName = partnerName;
    this.targets = targets;
    this.cookies = buildCookies({ domain: cookiesDomain });
    this._handleUrlParams();
  }

  _handleUrlParams() {
    // eslint-disable-next-line no-restricted-globals
    const { id, token } = getUrlParams(location);
    if (id) this.id = id;
    if (token) {
      this.token = token;
      // eslint-disable-next-line no-restricted-globals
      history.replaceState(null, null, removeUrlParams(location.href));
    }
  }

  set id(id) {
    this._id = id || null;
    this.cookies.setId(this._id);
  }

  get id() {
    if (!this._id) this._id = this.cookies.getId();
    return this._id;
  }

  set token(token) {
    this._token = token || null;
    if (!this._token) {
      this.cookies.removeToken();
      return;
    }
    this.cookies.setToken(this._token);
  }

  get token() {
    if (!this._token) this._token = this.cookies.getToken();
    return this._token;
  }

  async fetchData() {
    if (!this.token) return null;
    try {
      if (!this.leadInfo) this.leadInfo = await fetchLeadInfo(this.token);
    } catch (error) {
      if (error.message.includes('UNAUTHORIZED')) this.token = null;
    }
    return this.leadInfo;
  }

  async fillTargets() {
    await this.fetchData();
    (this.targets || []).forEach((config) => {
      const {
        dataKey,
        strategy,
        beforeAction,
        afterAction,
      } = config || {};

      const value = (this.leadInfo || {})[dataKey];
      if (isNil(value)) return;

      const selector = isFunction(config.selector)
        ? config.selector({ dataKey, strategy, value })
        : config.selector;
      const params = { value, selector, strategy };

      let element = selectElement(selector);
      if (isFunction(beforeAction)) beforeAction({ ...params, element });

      // Try to find the element again in case beforeAction changed the DOM
      element = element || selectElement(selector);
      if (!element) return;

      element = fillTarget({ ...params, element });
      if (isFunction(afterAction)) afterAction({ ...params, element });
    });
  }

  trackEvent(type, name, properties) {
    if (!this.token) return null;
    if (!this.partnerName) throw new Error('Parameter "partnerName" is required to track events');
    return trackEvent({
      type,
      partner: this.partnerName,
      zenfiId: this.id,
      event: name,
      meta: properties,
    });
  }

  trackConversion(name, properties) {
    this.trackEvent('converted', name, properties);
  }

  trackAbortion(name, properties) {
    this.trackEvent('aborted', name, properties);
  }

  trackPageView() {
    const properties = {
      href: window.location.href,
      hash: window.location.hash,
      search: window.location.search,
      protocol: window.location.protocol,
      hostname: window.location.hostname,
      pathname: window.location.pathname,
    };
    this.trackConversion('PageView', properties);
  }

  initPageViewsTracking() {
    this.trackPageView();
    addLocationChangeEvent();
    window.addEventListener('locationchange', () => this.trackPageView());
  }
}

module.exports = ZenfiSDK;
