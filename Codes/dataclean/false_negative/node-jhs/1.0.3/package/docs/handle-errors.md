# Handling error exceptions in a JHS script  

```javascript
<?jhs
/*
 *   How to handle error exceptions in a JHS script:
 *   1. Define a global variable named error.
 *   2. Enclose the rest of the script with try...catch statements.
 *   3. Assign the catched error message (e.message) to the global  `error` variable.
 *   4. Echo in the HTML part if error is not null,
 *   5. echo the correct content, otherwise.
 */
var error;
try{ //some stuff
    var a = 2,k = 4;
    var c = a*k;
}catch(e){error = e.message}
?>
<!DOCTYPE html> 
<html><head>
<meta charset="utf-8">
</head>
<body>
<div style="text-align:center;">
<h1><?jhs if(error) {echo(error)} else echo(c)?></h1>
</div>
</body>
</html>
```
