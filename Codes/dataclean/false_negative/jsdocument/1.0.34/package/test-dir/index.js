var jsdocument = require('jsdocument')

var js_document = new jsdocument.JSDocument();
var object = new jsdocument.JSObjects.JSPObject();
var title = new jsdocument.JSObjects.JSTitleObject();

jsdocument.UseCSS(js_document, 'index.css', jsdocument.Server)

title.SetTitle("MY JSDOCUMENT SITE!")
object.Text = "TEST-DIR"
js_document.AddHeaderObject(title)
js_document.AddObject(object)

jsdocument.Server.SetResponseHandler('/', function() {
    return [js_document.GetRawHTML(), "html"]
})