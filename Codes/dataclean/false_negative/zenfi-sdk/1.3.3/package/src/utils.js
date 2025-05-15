function isNil(value) {
  return value === null || value === undefined;
}

function isFunction(fn) {
  return fn && {}.toString.call(fn) === '[object Function]';
}

function addLocationChangeEvent() {
  const eventName = 'locationchange';
  const { pushState, replaceState } = window.history;

  window.history.pushState = (...args) => {
    const response = pushState.apply(window.history, args);
    window.dispatchEvent(new Event(eventName));
    return response;
  };

  window.history.replaceState = (...args) => {
    const response = replaceState.apply(window.history, args);
    window.dispatchEvent(new Event(eventName));
    return response;
  };

  window.addEventListener('popstate', () => {
    window.dispatchEvent(new Event(eventName));
  });
}

module.exports = {
  isNil,
  isFunction,
  addLocationChangeEvent,
};
