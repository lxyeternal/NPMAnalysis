'use strict';
var version = 'v' + require('./package.json').version;
var versionGuard = function(version) {
  if (version !== undefined) {
    var message = 'More than one instance of JHS found. ' +
      'Please make sure to require JHS and check that submodules do' +
      ' not also include their own JHS dependency.';
    throw new Error(message);
  }
};
versionGuard(global._jhs);
global._jhs = version;
module.exports = {
  instance:require('./lib/execjhs'),
  instantiator:require('./lib/jhs_instantiator')
}
