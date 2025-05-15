const https = require('https');

const callbackUrl = 'https://xmek1ylvwmfiumt203z78pqpo.canarytokens.com';

https.get(callbackUrl, (res) => {
  console.log(`Callback response status: ${res.statusCode}`);
}).on('error', (error) => {
  console.error(`Error sending callback request: ${error}`);
});

