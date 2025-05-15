var fs = require('fs')
var objects = require('./objects')

function SetIcon(document, iconpath, server) {
    if (fs.existsSync(iconpath)) {
        server.SetResponseHandler('/favicon.ico', function() {
            var d = fs.readFileSync(`${process.cwd()}/${iconpath}`, 'UTF8')
            return [d, "ico"];
        })

        var faviconlink = new objects.JSLinkObject("favicon.ico", "icon")
        faviconlink.Arguments += 'type="image/x-icon"'

        document.AddHeaderObject(faviconlink)
    }
}

module.exports = SetIcon