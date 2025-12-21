const { isNil, isFunction } = require('../utils');

describe('Utils', () => {
  describe('.isNil', () => {
    it('returns true when value is null', () => {
      const value = null;
      expect(isNil(value)).toEqual(true);
    });

    it('returns true when value is undefined', () => {
      const value = undefined;
      expect(isNil(value)).toEqual(true);
    });

    it('returns false when value is false', () => {
      const value = false;
      expect(isNil(value)).toEqual(false);
    });

    it('returns false when value is 0', () => {
      const value = 0;
      expect(isNil(value)).toEqual(false);
    });

    it('returns false when value is other truthy value', () => {
      const value = 1;
      expect(isNil(value)).toEqual(false);
    });
  });

  describe('.isFunction', () => {
    it('returns false when value is a string', () => {
      const value = 'not a function';
      expect(isFunction(value)).toEqual(false);
    });

    it('returns false when value is an object', () => {
      const value = {};
      expect(isFunction(value)).toEqual(false);
    });

    it('returns false when value is falsy', () => {
      const value = false;
      expect(isFunction(value)).toEqual(false);
    });

    it('returns true when value is an arrow function', () => {
      const value = () => {};
      expect(isFunction(value)).toEqual(true);
    });

    it('returns true when value is a function', () => {
      function value() {}
      expect(isFunction(value)).toEqual(true);
    });
  });
});
