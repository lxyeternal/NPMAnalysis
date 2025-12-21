# Node JHS Module

[![NPM Package](https://img.shields.io/npm/v/node-jhs.svg?style=flat-square)](https://www.npmjs.org/package/node-jhs)

<h1 align="left">
  <img width="180" height="180" src="https://github.com/Justo-Tapiador/node-jhs/assets/115353781/fa616814-de3c-45e9-8923-cdc5507da2e4" alt="JHS Module">
</h1>

## Synopsis

**A fast and pure NODE.js server-side module, and simple tool for making dynamic  and interactive Web pages.**

## Principles

JHS module is just pure javascript code, processed on a NODE.js web server by a JHS interpreter implemented as a NODE.js module. On a web server, the result of the interpreted and executedJHS code – which may be any type of data, such as generated HTML or binary image data – would form the whole or part of an HTTP response.

## Get Started

```sh
npm install node-jhs
```

## Documentation

The complete docs are hosted here: [JHS Documentation](https://github.com/Justo-Tapiador/node-jhs/blob/main/docs/)

* [Some server configurations](https://github.com/Justo-Tapiador/node-jhs/blob/main/docs/server-configurations.md)
* [Multilevel hierarchical JHS Mode](https://github.com/Justo-Tapiador/node-jhs/blob/main/docs/multilevel-hierarchy.md)
* [Ban some required modules](https://github.com/Justo-Tapiador/node-jhs/blob/main/docs/banned-require.md)
* [The Instantiator](https://github.com/Justo-Tapiador/node-jhs/blob/main/docs/instantiator.md)
* [Dynamic JHS Pages](https://github.com/Justo-Tapiador/node-jhs/blob/main/docs/dynamic-jhs-pages.md)
* [Using ranks](https://github.com/Justo-Tapiador/node-jhs/blob/main/docs/using-ranks.md)
* [Four ways of echoing JHS list into an HTML document](https://github.com/Justo-Tapiador/node-jhs/blob/main/docs/echoing-lists.md)
* [How to serve Unicode Ducklings to your clients](https://github.com/Justo-Tapiador/node-jhs/blob/main/docs/serving-unicode-ducklings.md)
* [How to handle error exceptions in a JHS script](https://github.com/Justo-Tapiador/node-jhs/blob/main/docs/handle-errors.md)

## Example

The simplest way of using this middleware module involves two parts: Firstly, write a webpage file with your favorite text editor, and name it with extension `.jhs`. Save it to your web server root directory (or any other folder under the root). Use code  delimiters `<?jhs` and `?>` to insert javascript code into the html code (this code will be executed in the server side, not in the client side). As you already know, code delimiters `<script> </script>` are html tags where you can insert javascript code that will be executed in the client side, but JHS delimiters are not HTML tags). There is a JHS `echo` function which is similar to the PHP echo function. Here it is a simple 'HELLO WORLD' page example, written with JHS, you may call it `hello-world.jhs`:

 ```javascript
        <?jhs 
            var str  = 'Hello world!';
            var date = new Date();
        ?>
        <!DOCTYPE html> 
        <html>
         <head>
            <meta charset="utf-8">
        </head>
        <body>
            <div style="text-align:center;">
                <h1><?jhs echo(str) ?></h1>
                <h2>Today is:</h2> <h3><?jhs echo(date.toString()) ?></h3>
            </div>
        </body>
        </html>
```

Secondly, in your NODE.js server script, the JHS module must be required, instantiated and called, like any other middleware engine:

```javascript
             ...
            const   JHS  = require('node-jhs').instance,
                    options = {root:"./wwwroot"},
                    parse_options = {},
                    file = options.root+'\\hello-world.jhs',
                    notfilepath = false,
                    execJHS = new JHS(options);
            ...
        /*  Call execJHS.parseFile async function, in your server request event listener */

            server.on('request', function(request, response){
            ...
            /*  when a request for the 'hello-world.jhs' file is received, 
                you use the middleware JHS engine for the response 
            */
                execJHS.parseFile(file, notfilepath, parse_options, function(jhsResult, err){  
                    response.end(jhsResult);
                }); 
            ...
    });
```

## Security

You can use JHS module in production,  but please use common sense when doing anything related to finances! I take no responsibility for your implementation decisions.

If you find a security issue, please email me,  [Justo Tapiador](mailto:justo.tapiador@gmail.com).

## License

Code released under the MIT license.
Copyright (c) 2022 Justo Tapiador García
