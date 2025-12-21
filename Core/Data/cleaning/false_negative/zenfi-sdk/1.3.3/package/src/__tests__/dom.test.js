const { fillTarget, selectElement } = require('../dom');

describe('DOM', () => {
  const value = 'NEW_VALUE';
  const selector = '.input';
  const element = { __type: 'HTML_NODE', click: jest.fn() };
  const querySelector = jest.fn();
  const setter = { set: jest.fn() };
  let originalDescriptor;

  beforeAll(() => {
    querySelector.mockReturnValue(element);
    originalDescriptor = Object.getOwnPropertyDescriptor;
    Object.getOwnPropertyDescriptor = () => setter;
  });

  afterAll(() => { Object.getOwnPropertyDescriptor = originalDescriptor; });

  beforeEach(() => {
    global.document = { querySelector };
    setter.set.mockClear();
    element.click.mockClear();
  });

  describe('.selectElement', () => {
    describe('when element is found', () => {
      it('calls selector and returns element', () => {
        querySelector.mockRestore();
        querySelector.mockReturnValueOnce(element);

        const results = selectElement(selector);
        expect(results).toEqual(element);
        expect(querySelector).toBeCalledTimes(1);
        expect(querySelector).toHaveBeenLastCalledWith(selector);
      });
    });

    describe('when element is not found', () => {
      it('does nothing and returns null', () => {
        querySelector.mockRestore();
        querySelector.mockReturnValueOnce(null);

        const results = selectElement(selector);
        expect(results).toEqual(null);
        expect(querySelector).toBeCalledTimes(1);
        expect(querySelector).toHaveBeenLastCalledWith(selector);
      });
    });
  });

  describe('.fillTarget', () => {
    const expectValue = (result, property) => {
      expect(result.__type).toEqual(element.__type);
      expect(result[property]).toEqual(value);
    };

    describe('strategy is "value"', () => {
      const strategy = 'value';

      // eslint-disable-next-line jest/expect-expect
      it('sets the value of the element and returns it', () => {
        const result = fillTarget({ element, value, strategy });
        expectValue(result, 'value');
      });
    });

    describe('strategy is "nativeValue"', () => {
      const strategy = 'nativeValue';

      // eslint-disable-next-line jest/expect-expect
      it('sets the value using its setter function', () => {
        const result = fillTarget({ element, value, strategy });
        expect(result.__type).toEqual(element.__type);
        expect(setter.set).toBeCalledTimes(1);
        expect(setter.set).toBeCalledWith(value);
      });
    });

    describe('strategy is "text"', () => {
      const strategy = 'text';

      // eslint-disable-next-line jest/expect-expect
      it('sets the innerText of the element and returns it', () => {
        const result = fillTarget({ element, value, strategy });
        expectValue(result, 'innerText');
      });
    });

    describe('strategy is "click"', () => {
      const strategy = 'click';

      it('class the method "click" of the element', () => {
        const result = fillTarget({ element, value, strategy });
        expect(result.__type).toEqual(element.__type);
        expect(element.click).toBeCalledTimes(1);
      });
    });

    describe('strategy is falsy', () => {
      const strategy = null;

      // eslint-disable-next-line jest/expect-expect
      it('uses value strategy by default', () => {
        const result = fillTarget({ element, value, strategy });
        expectValue(result, 'value');
      });
    });
  });
});
