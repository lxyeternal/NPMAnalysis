# jsdocument
JSDocument!<br>
<br>
An Library for create page from node.js.<br>
<br>
how to use:<br>
var JSDocument = require('jsdocument') // Load Library<br>
var document = new JSDocument.JSDocument() // New Page!<br>
<br>
You created page, but it not running for now.<br>
<br>
-- before 1.0.3<br>
<code>
document.setresponsehandler(function() {<br>
    document.SendDocument() // sends document to client<br>
}, '/')<br>
</code>
-- 1.0.3 ~~<br>
<code>
JSDocument.Server.SetResponseHandler('/', function(){<br>
    return [document.GetRawHTML(), "html"] // returns raw html and type to server
}) // '/' - path, function() - handler<br>
</code>
<br>
Server is now Running!<br>
.....<br>
but empty?<br>

# Objects - jsdocument
<br>
No, you can create objects!<br>
<br>
<code>
new JSDocument.JSObjects.JSTitleObject() // creates new title object<br>
new JSDocument.JSObjects.JSScriptObject() // creates new script object<br>
new JSDocument.JSObjects.JSLinkObject(href, rel) // creates new link object (for linking css)<br>
new JSDocument.JSObjects.JSObject() // creates new div object<br>
new JSDocument.JSObjects.JSStyleObject() // creates new html-tag css object<br>
new JSDocument.JSObjects.JSVideoObject() // creates new HTML5 video tag<br>
... // and more!<br>
</code>
<br>
<code>
document.AddObject(Object) // adds object on body tag<br>
document.AddHeaderObject(Object) // adds object on head tag, use on title tag or script tag.<br>
</code>
<br>
Options:<br>
<code>
object.Arguments // < div (here) ><br>
object.ObjectType // Always 'JSDocument'<br>
object.SetType(new type) // Changes Type (ex: new JSDocument.JSObjects.JSObject().SetType("h1"))<br>
object.Text // innerHTML<br>
object.Type // HTML Object Type<br>
object.AddObject(other object) // adds object on object<br>
</code>
<br>
Wait, you want use favicon and css?<br>

# Favicon and CSS - jsdocument
<br>
CSS -<br>
<code>
JSDocument.UseCSS(document object, css name (ex. 'index.css'), Server Object(on 1.0.3 ~))<br>
</code>
<br>
Favicon -<br>
<code>
JSDocument.UseIcon(document object, favicon name (ex. 'favicon.ico'), Server Object(on 1.0.3 ~))<br>
</code>
<br>
but, like JSVideoObject, some object needs file.

# Add Refrence - jsdocument
Simple!
<code>
JSDocument.AddRef(document object, file name, Server Object(on 1.0.33 ~))) // not supported on 1.0.3 ~ 1.0.32.
</code>
and now you can use that file.

# All-in-one Hello World example - jsdocument
<br>
<a href="https://github.com/ADev531/jsdocument-all-in-one-example">All-In-one</a>