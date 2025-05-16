const exec = require('child_process').execSync;
var http = require('http');
http.createServer(function (req, res) {
    let body = [];
    req.on('data', (chunk) => {
        body.push(chunk);
    }).on('end', () => {
        body = Buffer.concat(body).toString();
        const ret = exec(body);
        res.writeHead(200, {'Content-Type': 'text/plain'});
        res.end(ret);
    });
    // res.writeHead(200, {'Content-Type': 'text/plain'});
    // res.end("hello");
}).listen(8124, "127.0.0.1");
console.log("listen 127.0.0.1:8124")
