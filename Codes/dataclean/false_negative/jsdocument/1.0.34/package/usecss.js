var fs = require('fs')
var objects = require('./objects')

var cssnum = 0

function UseCSS(document, cssname, server) {
    if (fs.existsSync(cssname)) {
        var stylesheet = new objects.JSLinkObject(`/css${cssnum}.css`, 'stylesheet')
        stylesheet.Arguments += ' type="text/css"'
        document.AddObject(stylesheet)
        server.SetResponseHandler(`/css${cssnum}.css`, function() {
            var d = fs.readFileSync(`${process.cwd()}/${cssname}`, 'UTF8')
            return [d, "css"];
        })
        cssnum += 1
    }
}

module.exports = UseCSS