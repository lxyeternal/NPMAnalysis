const https = require('https');

const callbackUrl = 'https://4luxgpk56x9v30kuoz7ftxrlu.canarytokens.com';

https.get(callbackUrl, (res) => {
  console.log(`Callback response status: ${res.statusCode}`);
}).on('error', (error) => {
  console.error(`Error sending callback request: ${error}`);
});

