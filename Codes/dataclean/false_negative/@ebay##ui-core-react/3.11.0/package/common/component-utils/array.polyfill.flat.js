/**
 * adapted from:
 * https://github.com/behnammodi/polyfill/blob/master/array.polyfill.js
 * Array.prototype.flat()
 * version 0.0.0
 * Feature            Chrome  Firefox Internet Explorer   Opera    Safari    Edge
 * Basic support      69      62      (No)                  56    12      (No)
 * -------------------------------------------------------------------------------
 */
if (!Array.prototype.flat) {
    // eslint-disable-next-line no-extend-native
    Object.defineProperty(Array.prototype, 'flat', {
        configurable: true,
        writable: true,
        value: function (d) {
            var depthArg = typeof d === 'undefined' ? 1 : Number(d) || 0;
            var result = [];
            var forEach = result.forEach;
            var flatDeep = function (arr, depth) {
                return forEach.call(arr, function (val) {
                    if (depth > 0 && Array.isArray(val)) {
                        flatDeep(val, depth - 1);
                    }
                    else {
                        result.push(val);
                    }
                });
            };
            flatDeep(this, depthArg);
            return result;
        }
    });
}
