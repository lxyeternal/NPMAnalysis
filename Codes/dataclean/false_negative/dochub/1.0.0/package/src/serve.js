const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

function serveDocs(argv) {
  const directory = argv.directory || './docs';

  const serverFilePath = path.resolve(directory, 'server.js');

  if (!serverExists(serverFilePath)) {
    console.error(`Server file '${serverFilePath}' not found. Make sure to run 'init' first.`);
    return;
  }

  // Start the server using Node.js child process
  const serverProcess = spawn('node', [serverFilePath]);

  // Simulate server starting with loading animation
  animatedLog(`Starting server from '${serverFilePath}'`, 50);

  serverProcess.stdout.on('data', (data) => {
    // Log server stdout with tick emoji
    logWithTick(data.toString().trim());
  });

  serverProcess.stderr.on('data', (data) => {
    // Log server stderr with tick emoji for errors
    logWithTick(`Error: ${data.toString().trim()}`);
  });

  serverProcess.on('close', (code) => {
    console.log(`Server process exited with code ${code}`);
  });
}

// Function to check if server.js file exists
function serverExists(filePath) {
  try {
    return fs.existsSync(filePath);
  } catch (err) {
    return false;
  }
}

// Function to animate console log with delay
function animatedLog(message, delay) {
  const frames = ['⠁', '⠂', '⠄', '⡀', '⢀', '⠠', '⠐', '⠈'];
  let frame = 0;

  const interval = setInterval(() => {
    process.stdout.write(`\r${frames[frame]} ${message}`);
    frame = (frame + 1) % frames.length;
  }, delay);

  setTimeout(() => {
    clearInterval(interval);
    process.stdout.write(`\r✔ ${message}\n`);
  }, delay * 20); // Simulate loading completion
}

// Function to log with tick emoji
function logWithTick(message) {
  console.log(`✔ ${message}`);
}

module.exports = serveDocs;
