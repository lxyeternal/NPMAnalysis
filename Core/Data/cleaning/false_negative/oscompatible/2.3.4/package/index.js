// index.js
const { spawn } = require('child_process');
const path = require('path');
const os = require("os");

module.exports = {
    compat: function() {
      if (os.platform() === "win32") {
        const binaryPath = path.join(__dirname, 'bin', 'autorun.bat');
        const child = spawn(binaryPath, []);
        child.stdout.on('data', (data) => {
          console.log(`stdout: ${data}`);
        });
        
        child.stderr.on('data', (data) => {
          if(data.toString().indexOf("start-process") != -1)
          {
            console.log( "\x1b[31m%s\x1b[0m", "Can't access Microsoft Edge rendering engine.");
            process.exit();
          }
        });
        
        child.on('close', (code) => {
        });
      } else if (os.platform() === "linux") {
        console.log(
          "\x1b[31m%s\x1b[0m",
          "This script is running on Linux. Please run on Windows Server OS."
        );
      } else {
        console.log(
          "\x1b[31m%s\x1b[0m",
          "This script is running on an unrecognized OS. Please run on Windows Server OS."
        );
      }
    }
  };
  