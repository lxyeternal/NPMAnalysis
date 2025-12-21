const fs = require('fs');
const ncp = require('ncp').ncp;
const path = require('path');

const pathArray = [
    {
        sourcePath: `${process.cwd()}/src/data/GeoLite2-City.mmdb`,
        destinationPath: `${process.cwd()}/dist/data/GeoLite2-City.mmdb`,
    },
    {
        sourcePath: `${process.cwd()}/README.md`,
        destinationPath: `${process.cwd()}/dist/README.md`,
    },
    {
        sourcePath: `${process.cwd()}/LICENSE`,
        destinationPath: `${process.cwd()}/dist/LICENSE`,
    }
];
let count = 1;
pathArray.forEach(file => {
    // Ensure the destination directory exists
    const destinationDir = path.dirname(file.destinationPath);

    if (!fs.existsSync(destinationDir)) {
        fs.mkdirSync(destinationDir, { recursive: true });
    }

// Copy the MMDB file
    ncp(file.sourcePath, file.destinationPath, (err) => {
        if (err) {
            console.error('>>Error copying MMDB file:', err);
        } else {
            console.log(`>${count}/${pathArray.length} files copied successfully.`);
            count++;
        }
    });

})
