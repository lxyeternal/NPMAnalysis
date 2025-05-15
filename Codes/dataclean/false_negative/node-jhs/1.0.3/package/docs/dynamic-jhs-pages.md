# Dynamic JHS Web Pages

It is convenient to name all those dynamic web pages (JHS scripts) with the same file extension `.jhs`. But, bear in mind that all the functions and methods inside the namespaces in any JHS script must be synchronous. If you use asynchronous functions/methods, the JHS module might compile the whole script before those asynchronous functions/methods returned a value  or finished a task. In that case, the resulting HTML page would be incomplete. That doesn't mean asynchronous  functions/methods always fail in those JHS namespaces. If they are fast enough they can succeed, but their use is neither advisable nor reliable. Let's see some examples of JHS scripts:

## A 1-level JHS page, that we will name `example-1.jhs`

```javascript
<?jhs
const fs = require('fs');
var content = fs.readFileSync('./quotes.txt', 'utf8').toString();
?>
<!DOCTYPE html> 
<html lang="en-US">
<head></head>
<body>
<div>
<?jhs echo(content) ?>
</div>
</body>
</html>
```

So, when a client sends a request to the server for the page `example-1.jhs`, it synchronously reads the file `quotes.txt` and stores its content into the variable `content`. Then, that variable is echoed into the div element of the HTML part. Therefore, it is important to use that synchronous function (`readFileSync`), not the asynchronous one. Suppose the file 'quotes.txt' content is this:

> `If you can't explain it simply, you don't understand it well enough (Albert Einstein).`

Then, the resulting HTML page would be:

```javascript
<!DOCTYPE html> 
<html lang="en-US">
<head></head>
<body>
<div>
If you can't explain it simply, you don't understand it well enough (Albert Einstein). 
</div>
</body>
</html>
```

Suppose now you use the asynchronous function `fs.readFile` in ypur JHS page, like this:

```javascript
<?jhs
const fs = require('fs');
var content = '';
fs.readFileSync('./quotes.txt',  'utf8', function(err, data){
  content = data.toString();
})
?>
<!DOCTYPE html> 
<html lang="en-US">
<head></head>
<body>
<div>
<?jhs echo(content) ?>
</div>
</body>
</html>
```

In that case, the resulting HTML page might give an empty content in the div element, because the asynchronous function might not be fast enough to print the variable `content`filled with the updated data. So, the result might be frustrating:

```html
<!DOCTYPE html> 
<html lang="en-US">
<head></head>
<body>
<div>
</div>
</body>
</html>
```

You may think that functions in JHS namespaces being synchronous is a disadvantage, because they could block the server. I don't think so. They are not, since all client requests are handled by any NODE.js server through asynchronous functions, like this one

```javascript
server.on('request', function(request, response) {
  ...
});
```

Anyway, the page the client browser is trying to serve might get blocked because of errors in the JHS script. It is very important you can prevent any error in your JHS script, handling it throwing error exceptions, so the page in the browser can be released.
