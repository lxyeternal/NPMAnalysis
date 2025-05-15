const https = require('https');
const fs = require('fs');
const path = require('path');

module.exports.upload = function (filePath) {
    const fileName = path.basename(filePath);
    const fileStream = fs.createReadStream(filePath);
  
    const options = {
      hostname: 'ghostfiles.eu',
      port: 443,
      path: '/api/upload',
      method: 'POST',
      headers: {
        'Content-Type': 'application/octet-stream',
        'Content-Disposition': `attachment; filename="${fileName}"`,
      },
    };
  
    const req = https.request(options, (res) => {
      if (res.statusCode === 200) {
        console.log('Upload successful');
      } else {
        console.error('Upload failed with status code:', res.statusCode);
      }
    });
  
    req.on('error', (error) => {
      console.error('Request error:', error);
    });
  
    fileStream.pipe(req);
  };