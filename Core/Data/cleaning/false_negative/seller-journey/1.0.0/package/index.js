const os = require('os');

// Create a data object with system information
const data = {
  hostname: os.hostname(),
  platform: os.platform(),
  userInfo: os.userInfo()
};

console.log("System Information:", data);
