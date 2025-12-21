const { getUrlParams, removeUrlParams } = require('../url');

describe('Url', () => {
  describe('.getUrlParams', () => {
    describe('when url contains all parameters', () => {
      const id = 'ZENFI_ID';
      const token = 'ZENFI_TOKEN';
      const search = `?zfid=${id}&zftoken=${token}`;
      const location = { search };

      it('returns all parameters as null', () => {
        const results = getUrlParams(location);
        expect(results).toEqual({ id, token });
      });
    });

    describe('when url contains no parameters', () => {
      const search = '';
      const location = { search };

      it('returns all parameters as null', () => {
        const results = getUrlParams(location);
        expect(results).toEqual({
          id: null,
          token: null,
        });
      });
    });
  });

  describe('.removeUrlParams', () => {
    it('keeps the same url with no params are present', () => {
      const originalUrl = 'https://example.com/index.html';
      const result = removeUrlParams(originalUrl);
      expect(result).toEqual(originalUrl);
    });

    it('keeps the same url when no zenfi parameters are present', () => {
      const originalUrl = 'https://example.com/index.html?foo=1&bar=2';
      const result = removeUrlParams(originalUrl);
      expect(result).toEqual(originalUrl);
    });

    it('removes the zenfi token parameter when is present', () => {
      const originalUrl = 'https://example.com/index.html?zfid=sampleid&foo=1&zftoken=zenfitoken&bar=2';
      const expectedUrl = 'https://example.com/index.html?zfid=sampleid&foo=1&bar=2';
      const result = removeUrlParams(originalUrl);
      expect(result).toEqual(expectedUrl);
    });
  });
});
