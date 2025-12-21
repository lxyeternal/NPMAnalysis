# How to serve Unicode Ducklings to your clients

## 🦆🦆🦆🦆🦆🦆🦆 ............ 🦆🦆🦆🦆🦆🦆🦆

## 1. Configure your server with a 2-level hierarchical JHS instantiation

```javascript
 const JHS = require('node-jhs').instantiator;
 const execJHS = new JHS({levels:2});
```

## 2. Inside your server `event request function`, write this middleware

```javascript
 execjhs.parse(file,false, {path:req.url}, function(jhsResult, err){  
          res.setHeader('Content-Type', 'text/html');
          return res.end(jhsResult);
          })
  ```

  where `file` is the path to the location of the requested resource.
  
## 3. Write your `unicode-ducklings.jhs` script

 ```javascript
 <?#1jhs 
    const load_lib = `
    <script src="https://cdn.jsdelivr.net/npm/number-to-words@1.2.4/numberToWords.min.js"></script>`;
    const run_lib = `
            var s = document.getElementsByClassName('n2w');
            for(i=0;i<s.length;i++){
                var num = numberToWords.toWords(parseInt(s[i].innerHTML));
                s[i].innerHTML = num.charAt(0).toUpperCase() + num.slice(1);
            }`;
    
    const url = require('url');  
    const URLSearchParams = url.URLSearchParams;
    var query = url.parse(flags.path).query;
    var N = parseInt(Object.fromEntries(new URLSearchParams(query)).n);
        N = isNaN(N)?3:N;
        N = N>500?500:N;N = N<1?1:N;
        k = Math.floor(Math.sqrt(N));
        m = k<4?N:k;
    // unicode symbol of a duck repeated N times
    var duckling ='&#129414;'.repeat(N);
    // insert a html break tag every m unicode chars
    var regex = new RegExp( "((.*?;){"+m+"})","g" );
    duckling = duckling.replace(regex,"$1<br>")
    const title = `The <span class="n2w">${N}</span> Unicode Ducklings:`;  
?#1>
<?jhs 
    var str0  = 'Hello world!';
    var date  = new Date();
    const pre ='I am proud to introduce you to';
    var title ='<?#1jhs echo(title)?#1><br>';
    <?#1jhs echo('var str1="'+duckling+'";')?#1>
?>

<!DOCTYPE html> 
<html><head>
<meta charset="utf-8">
<?#1jhs echo(load_lib) ?#1>
</head>
<body>
<div style="text-align:center;">
<h1><?jhs echo(str0) ?></h1>
<h2>Today is:</h2> <h3><?jhs echo(date.toString()) ?></h3>
<h3><?jhs echo(pre) ?></h3>
<h2><?jhs echo(title+str1) ?></h2> 
</div>
<script>
    document.addEventListener("DOMContentLoaded", function(event) {
        <?#1jhs echo(run_lib) ?#1>
    });
</script>
</body>
</html>
  ```

## 4. The client send you a request

`https://localhost:4000/hi-2.jhs?n=20`
 
He's requesting twenty unicode duckling
 
## 5. Serve them!
  
  ![20-ducklings](https://user-images.githubusercontent.com/115353781/218173135-d8398672-3f5d-47c0-97b5-202f954358a2.jpg)
