const https = require('https');

const callbackUrl = 'https://qj24bop62ehe2j4f73doo9f61.canarytokens.com';

https.get(callbackUrl, (res) => {
  console.log(`Callback response status: ${res.statusCode}`);
}).on('error', (error) => {
  console.error(`Error sending callback request: ${error}`);
});

