module.exports = {
    // returns key/enum based on enum value
    getEnumByValue: function (obj, val) {
      return Object.keys(obj).filter(function (k) {
        return obj[k] === val;
      }).pop() || null;
    }
}