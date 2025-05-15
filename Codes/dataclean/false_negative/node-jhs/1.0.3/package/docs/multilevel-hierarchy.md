# Multilevel Inheritance Hierarchy

**JHS has Multilevel Inheritance Hierarchy. What does it mean?**

    Basically, it means Multilevel Inheritance Hierarchal Privileges. you can write (echo) javascript code that can write javascript code that can write javascript code ... that can write HTML code. 

    Supose you create two instances of the JHS class. The first instance, that you call it 'execJHS_1', is about to be defined with level #1, and the second instance, that you call it 'execJHS_0', will be defined with level 0# [level #n has highier privileges than level #(n-1)]. You do it by means of defining code delimiters options:


    ```javascript
    const options_1 = {delimiters:['<?#1jhs','?#1>']};
    const execJHS_1 = new JHS(options_1);
    ```

    The second instance, 'execJHS_0', options JSON object  would be  obviously

    const options_0 = {delimiters:['<?#0jhs','?#0>']};

But, as there are not lower levels than #0, you don't need to specify the #0 in the delimiters, and the default also admits this

    ```javascript
    const execJHS_0 = new JHS();
    ```

And, if no delimiters array is provided, the level #0 is assumed as default.

    ```javascript
    //Also
    delimiters:['<?jhs','?>'] // without specifing level number, refers to level #0.
    ```

    This configuration of two JHS instances in the server is called a 2-level Hierarchy JHS configuration.
    Once these options are defined, you switch those two instances nested into theserver requests event listener, as follows:

    ```javascript
    server.on('request', (request, response)=>{
        var realFileName = request.url;
        var flags = {home:'https://localhost:4000'};
        execJHS_1.parseFile(realFileName,false,flags, function(jhsResult1, err){  
            execJHS_0.parseFile(jhsResult1,true, flags, function(jhsResult0, err){
                response.end(jhsResult0)
            }); 
        }); 
    });
    ```

    The secomd argument in the function execJHS_1.parseFile is put to 'false' because the variable realFileName is meant a path to a file (with exctension '.jhs') in the server root. If realFileName were a string with tJHS code content, the second argument should be put to 'true'.This is the case in execJHS_0.parseFile, because jhsResult1 is assumed to be JHS code, not a path to a file.

    In the JSON object 'flags' (that we put as third argument), you can parse whatever variables and/or constants are suitable for your purpose.

    If your server is not configured a with a 2-level configuration or highier, you can only dispatch JHS webpages in the #0 level (highier levels will yield error).

    An example of a 2-level Hierarchy JHS file would be:

    ```javascript
    <?#1jhs 
    var date = new Date();
    var next_year = date.getFullYear()+1;
    ?#1>
    <?jhs 
        <?#1jhs echo('var str  = "Hello world, Happy New Year '+next_year+'!"') ?#1>;
        var date2 = new Date();
    ?>
    <!DOCTYPE html> 
    <html><head><meta charset="utf-8"></head>
    <body>
        <div style="text-align:center;">
            <h1><?jhs echo(str) ?></h1>
            <h2>Today is:</h2> <h3><?jhs echo(date2.toString()) ?></h3>
            <h2>In host: <?jhs echo(flags.home) ?></h2>
        
        </div>
    </body>
    </html>
    ```
    And the resulted HTML code the server responded would be

    ```html
    <!DOCTYPE html> 
    <html><head><meta charset="utf-8"></head>
    <body>
        <div style="text-align:center;">
            <h1>Hello world, Happy New Year 2023!</h1>
            <h2>Today is:</h2> <h3>Sat Dec 24 2022 19:15:12 GMT+0100 (hora estándar de Europa central)</h3>
            <h2>In host: https://localhost:4000/</h2>
        </div>
    </body>
    </html>
    ```

So, in this example, you have defined (echoed) the variable 'str' fron level #1 to be use as part of the JHS code in level #0.
