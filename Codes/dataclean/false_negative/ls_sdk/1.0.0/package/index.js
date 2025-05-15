const https = require('https');

/* ------------------------------------------------------------------------
//
//  Utility Functions
//
-------------------------------------------------------------------------- */

// https get request with basic auth and body
async function reqAuth(url, path, method, username, password, body, callback) {

    var auth = 'Basic ' + Buffer.from(username + ':' + password).toString('base64');
    var options = {
        host: url,
        port: 443,
        path: path,
        method: method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': auth
        },
    };

    return new Promise((resolve, reject) => {
    
      var req = https.request(options, function(res) {
        resBody=''
          res.setEncoding('utf8');
          res.on('data', function (chunk) {
              resBody += chunk;
          });
          res.on('end', function(){
            if (isJsonString(resBody)) {
              resolve(JSON.parse(resBody));
            } else {
              resolve(resBody);
            }
          })
      });

      req.on('error', (err) => {
        reject(err)
      })

      req.write(JSON.stringify(body));

      req.end();

    });
}

function isJsonString(str) {
  try {
      JSON.parse(str);
  } catch (e) {
      return false;
  }
  return true;
}


/* ------------------------------------------------------------------------
//
//  Exported SDK
//
-------------------------------------------------------------------------- */

function SDK (server, username, password) {
  this.server = server;
  this.username = username;
  this.password = password;
}

SDK.prototype.create = function (params) {
  let result = reqAuth(this.server , '/api/create', 'POST', this.username, this.password, params);
  return result;
}

SDK.prototype.approvalList = function (params) {
  let result = reqAuth(this.server , '/api/approval/List', 'GET', this.username, this.password, {});
  return result;
}

SDK.prototype.approvalStatus = function (params) {
  let result = reqAuth(this.server , '/api/approval/status' , 'POST', this.username, this.password, params)
  return result
}

SDK.prototype.transactions = function (params) {
  let result = reqAuth(this.server , '/api/transactions' + '?incompleteOnly=' + params.incompleteOnly+"&limit=" + params.limit+"&offset=" + params.offset, 'GET', this.username, this.password, {} )
  return result;
}

SDK.prototype.balance = async function (params) { 
  let result = reqAuth(this.server , '/api/balance/' + params.walletId , 'GET', this.username, this.password, {});
  return result;
}

SDK.prototype.autoapproveList = function (params) {
  let result = reqAuth(this.server , '/api/autoapprove/list' , 'GET', this.username, this.password, {});
  return result;
}

SDK.prototype.autoapprove = function (params) {
  let result = reqAuth(this.server , '/api/autoapprove' , 'POST', this.username, this.password, params);
  return result;
}

module.exports = SDK;

