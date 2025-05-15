var objecttype = require('./objects')

var header = '<!DOCTYPE HTML>\n \
            \ <html lang=\'en\'>\n \
            \   <head>\n \
            \       <meta charset="utf-8">\n \
            \       <meta name="viewport" content="width=device-width, initial-scale=1.0">'

var bodytg = '\
          \     </head>\n \
          \     <body>\n'

var ending = '  </body>\n \
          \ </html>'

const JSDocument = (function() {
    var currentrep;
    var currentreq;

    function JSDocument() {
        this.JSObjects = [];
        this.JSHeaderObjects = [];
    }

    function AddObject(Object) {
        if (Object.ObjectType != undefined && Object.ObjectType == "JSDocument") {
            this.JSObjects.push(Object)
        }
    }
    JSDocument.prototype.AddObject = AddObject;

    function AddHeaderObject(Object) {
        if (Object.ObjectType != undefined && Object.ObjectType == "JSDocument") {
            this.JSHeaderObjects.push(Object)
        }
    }
    JSDocument.prototype.AddHeaderObject = AddHeaderObject;

    function GetRawResponse() {
        return currentrep
    }
    JSDocument.prototype.GetRawResponse = GetRawResponse;

    function GetRawHTML() {
        var document = header;

        this.JSHeaderObjects.forEach(function(v, i, array) {
            var tag = `<${v.Type} ${v.Arguments}>${v.Text}</${v.Type}>\n`;
            document += tag;
        })

        document += bodytg

        this.JSObjects.forEach(function(v, i, array) {
            var tag = `<${v.Type} ${v.Arguments}>${v.Text}</${v.Type}>\n`;
            document += tag;
        })

        document += ending

        return document;
    }
    JSDocument.prototype.GetRawHTML = GetRawHTML;
    return JSDocument
}())

module.exports = JSDocument