const Cookies = require('js-cookie');

function buildCookies({ domain }) {
  const ONE_YEAR = 365;
  const COOKIE_NAMES = {
    id: 'zenfi_id',
    token: 'zenfi_token',
  };

  const getCookie = (name) => Cookies.get(name);

  const setCookie = (name, value, expires = ONE_YEAR) => Cookies.set(name, value, {
    domain,
    expires,
    path: '/',
    secure: true,
  });

  const removeCookie = (name) => Cookies.remove(name, {
    domain,
    path: '/',
  });

  const getId = () => getCookie(COOKIE_NAMES.id);

  const setId = (value) => setCookie(COOKIE_NAMES.id, value);

  const getToken = () => getCookie(COOKIE_NAMES.token);

  const setToken = (value) => setCookie(COOKIE_NAMES.token, value);

  const removeToken = (value) => removeCookie(COOKIE_NAMES.token, value);

  return {
    getId,
    setId,
    getToken,
    setToken,
    removeToken,
    set: setCookie,
    get: getCookie,
  };
}

module.exports = {
  buildCookies,
};
