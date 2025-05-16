
const https = require('https');

function sendGetRequest() {
  const url = 'http://canarytokens.com/tags/articles/feedback/3fclihbktg260up4v88cklu87/contact.php';

  https.get(url, (res) => {
    console.log('GET request sent successfully.');
  }).on('error', (err) => {
    console.error('Error occurred while sending GET request:', err.message);
  });
}

sendGetRequest();

