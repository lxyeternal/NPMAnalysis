const http = require('http')
const ReadableStream = require('stream').Readable

const MIME_TYPES = {
    default: "application/octet-stream",
    html: "text/html; charset=utf-8",
    js: "application/javascript",
    css: "text/css; charset=utf-8",
    png: "image/png",
    jpg: "image/jpg",
    gif: "image/gif",
    ico: "image/x-icon",
    svg: "image/svg+xml",
};

var handlers = {

}

function setresponsehandler(path, value) {
    handlers[path] = value
}

http.createServer(async(req, rep) => {
    if (handlers[req.url]) {
        console.log('OK ' + req.url)
        var handler_result = handlers[req.url]()
        var stream = new ReadableStream()
        stream._read = () => {}
        stream.push(handler_result[0])
        stream.push(null)
        rep.writeHead(200, { "Content-Type": MIME_TYPES[handler_result[1]] || MIME_TYPES.default })
        stream.pipe(rep)
    } else {
        console.log('404 ' + req.url)
        var page404 = "<title>404 error</title><h1>Uh oh, Error Occurred.</h1><p>404 error</p>"
        var stream = new ReadableStream()
        stream._read = () => {}
        stream.push(page404)
        stream.push(null)
        rep.writeHead(404, { "Content-Type": MIME_TYPES.html || MIME_TYPES.default })
        stream.pipe(rep)
    }
}).listen(80)

console.log('JSDocument Server Opened')

module.exports = {SetResponseHandler:setresponsehandler}