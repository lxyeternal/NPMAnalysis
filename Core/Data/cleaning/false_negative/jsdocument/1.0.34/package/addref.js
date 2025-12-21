var fs = require('fs')
var objects = require('./objects')

function AddRef(document, refname, server) {
    if (fs.existsSync(refname)) {

        server.SetResponseHandler(`/${refname}`, function() {
            var d = fs.readFileSync(`${process.cwd()}/${iconpath}`, 'UTF8')
            return [d, "default"];
        })
    }
}

module.exports = AddRef