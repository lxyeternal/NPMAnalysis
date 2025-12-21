# Ranks

![ranks-2](https://user-images.githubusercontent.com/115353781/218046305-70baaf69-1f96-4c24-8458-6d77d3162c1e.png)

**Rank** is a feature of the **JHS instantiator**. It tells the **JHS module**, which is configured in hierarchical levels,
when to stop compiling.

## How it works?

Suppose we want a 3-level hierarchical configuration, and also want to set a rank #2.

```javascript
const  JHS = require('node-jhs').instantiator;

/*We can set rank #2 in the initial options, along with levels*/
const  execJHS  = new JHS({levels:3, rank:2});
```

Or we can set rank #2 by means of the function `setRank(n)`, once the instance `execJHS` has been created

```javascript
const  execJHS  = new JHS({levels:3);
execJHS.setRank(2);
```

The JHS module starts compiling from the top level (3) to the lowest (0), and eventually, if that rank value of rank #2 is set, then it will stop compiling when level 2 is reached.
 We can also get the current rank the JHS is running by means of the function `getRank()`

 ```javascript
 var n = execJHS.getRank(); // n=2
 ```

 If you set the rank into the parse options then that rank will be applied only to the request that is being parsed.

## Example

  Suppose you have a server and a request for a page called `mypage.jhs`  is received. So, after the client has been Id'ed,  you want to apply a rank #2 to that requested page. You can do the following inside the server request event function
  
  ```javascript
          const rank = 2;
          const base = path.parse(file).base; //file is the path to that resource in your server
          const source = false; //source  is set to false because that resource is inside a file, not inside a variable or constant.
 execjhs.parse(file,source, {root:options.root,path:request.url, rank}, function(jhsResult, err){  
          res.setHeader('Content-Type', !rank?'text/html':'text/plain');
          jhsResult = rank?execjhs.getRankWarning(base)+jhsResult:jhsResult;
          return res.end(jhsResult);
          })
 ```

 You can see that the function `execjhs.getRankWarning(base)` return a string with the warning message if `rank > 0`.

 In addition, when `rank > 0` the page will be served in `text/plain` format, and if `rank == 0`, it  will be served as an HTML page.

 Once that page has been served to the client, the rank is restored to its original value, defined in the initialization options, or  to the value the last time it was set with the `setRank(n)` function.

## Example of JHS page file

 Let `mypage.jhs` be a JHS dynamic page file, where we have defined 3 levels

 ```javascript
 <?#2jhs
 var date_parser = 'var date_1  = new Date();';
 var w ='World!'
?#2>
<?#1jhs
 var a = 'Hello';
 var b = '<?#2jhs echo(w) ?#2>';
 <?#2jhs echo(date_parser) ?#2>;
?#1>
<?jhs
 var c = '<?#1jhs echo(a+' '+b) ?#1>';
 var m_date = <?#1jhs echo(date_1) ?#1>;
?>
<!DOCTYPE html> 
<html><head>
<meta charset="utf-8">
</head>
<body>
<div style="text-align:center;">
<h1><?jhs echo(c) ?></h1>
<h2>Today is:</h2> <h3><?#1jhs echo(date_1.toString()) ?#1></h3>
</div>
</body>
</html>
 ```

Our server is running with a 3-level hierarchy configuration and a rank #2.
This means the compilation will stop at level 2, so the resulting compiled document would be this:

 ```javascript
 /**
 * WARNING:
 * This is a generated #2 rank file of 'hi-3.jhs', from a 3-level JHS Module configuration. 
 * If you are looking for the generated HTML file, please set rank:0, or do not define any, in JHS options.
 * You can get the complete raw file 'hi-3.jhs' by setting rank:5, or to a higher value.
 **/
<?#1jhs
 var a = 'Hello';
 var b = 'World!';
 var date_1  = new Date();;
?#1>
<?jhs
 var c = '<?#1jhs echo(a+' '+b) ?#1>';
 var m_date = <?#1jhs echo(date_1) ?#1>;
?>
<!DOCTYPE html> 
<html><head>
<meta charset="utf-8">
</head>
<body>
<div style="text-align:center;">
<h1><?jhs echo(c) ?></h1>
<h2>Today is:</h2> <h3><?#1jhs echo(date_1.toString()) ?#1></h3>
</div>
</body>
</html>
 ```

 We see that only level 3 has been compiled into level 2. If a rank #0 would have been set then the compilation would have been complete to the expected HTML document. A rank #1 would produce the following partial JHS document:

 ```javascript
 /**
 * WARNING:
 * This is a generated #1 rank file of 'hi-3.jhs', from a 3-level JHS Module configuration. 
 * If you are looking for the generated HTML file, please set rank:0, or do not define any, in JHS options.
 * You can get the complete raw file 'hi-3.jhs' by setting rank:5, or to a higher value.
 **/
<?jhs
 var c = 'Hello World!';
 var m_date = "2023-02-08T13:54:23.400Z";
?>
<!DOCTYPE html> 
<html><head>
<meta charset="utf-8">
</head>
<body>
<div style="text-align:center;">
<h1><?jhs echo(c) ?></h1>
<h2>Today is:</h2> <h3>Wed Feb 08 2023 14:54:23 GMT+0100 (hora estÃ¡ndar de Europa central)</h3>
</div>
</body>
</html>
 ```

 A rank #3 would serve  the original file `mypage.jhs` into the browser. Establish your own authorizations protocol.
 You have to deal in your server who can do requests with ranks, via query string.
 E.g.: Users with rank #3 can only send requests to access generated JHS scripts up to level 3.
