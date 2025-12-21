const Cookies = require('js-cookie');
const { buildCookies } = require('../cookies');

describe('.buildCookies', () => {
  const path = '/';
  const domain = 'example.com';
  const storedValue = 'StoredValue';
  const cookies = buildCookies({ domain });
  const expectedCookieOptions = {
    path,
    domain,
    secure: true,
    expires: 365,
  };

  jest.spyOn(Cookies, 'get').mockImplementation(() => storedValue);
  jest.spyOn(Cookies, 'set').mockImplementation();
  jest.spyOn(Cookies, 'remove').mockImplementation();

  beforeEach(() => {
    Cookies.get.mockClear();
    Cookies.set.mockClear();
    Cookies.remove.mockClear();
  });

  describe('#set', () => {
    it('calls Cookie.set with the correct parameters, expires in one year by default', () => {
      const value = 'COOKIE_VALUE';
      const name = 'COOKIE_NAME';
      cookies.set(name, value);
      expect(Cookies.set).toBeCalledTimes(1);
      expect(Cookies.set).toHaveBeenLastCalledWith(name, value, expectedCookieOptions);
    });

    it('calls Cookie.set with a custom expiration time', () => {
      const value = 'COOKIE_VALUE';
      const name = 'COOKIE_NAME';
      const expires = 1;
      cookies.set(name, value, expires);
      expect(Cookies.set).toBeCalledTimes(1);
      expect(Cookies.set).toHaveBeenLastCalledWith(name, value, {
        ...expectedCookieOptions,
        expires,
      });
    });
  });

  describe('#get', () => {
    it('calls Cookie.get with the correct parameters', () => {
      const name = 'COOKIE_NAME';
      cookies.get(name);
      expect(Cookies.get).toBeCalledTimes(1);
      expect(Cookies.get).toHaveBeenLastCalledWith(name);
    });
  });

  describe('#getId', () => {
    it('calls Cookie.get with the correct parameters', () => {
      const value = cookies.getId();
      expect(value).toEqual(storedValue);
      expect(Cookies.get).toBeCalledTimes(1);
      expect(Cookies.get).toHaveBeenLastCalledWith('zenfi_id');
    });
  });

  describe('#setId', () => {
    it('calls Cookie.set with the correct parameters', () => {
      const value = 'NewID';
      cookies.setId(value);
      expect(Cookies.set).toBeCalledTimes(1);
      expect(Cookies.set).toHaveBeenLastCalledWith(
        'zenfi_id',
        value,
        expectedCookieOptions,
      );
    });
  });

  describe('#getToken', () => {
    it('calls Cookie.get with the correct parameters', () => {
      const value = cookies.getToken();
      expect(value).toEqual(storedValue);
      expect(Cookies.get).toBeCalledTimes(1);
      expect(Cookies.get).toHaveBeenLastCalledWith('zenfi_token');
    });
  });

  describe('#setToken', () => {
    it('calls Cookie.set with the correct parameters', () => {
      const value = 'NewToken';
      cookies.setToken(value);
      expect(Cookies.set).toBeCalledTimes(1);
      expect(Cookies.set).toHaveBeenLastCalledWith(
        'zenfi_token',
        value,
        expectedCookieOptions,
      );
    });
  });

  describe('#removeToken', () => {
    it('calls Cookie.remove with the correct parameters', () => {
      cookies.removeToken();
      expect(Cookies.remove).toBeCalledTimes(1);
      expect(Cookies.remove).toHaveBeenLastCalledWith(
        'zenfi_token',
        { domain, path },
      );
    });
  });
});
