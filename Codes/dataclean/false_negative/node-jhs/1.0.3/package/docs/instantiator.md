# The JHS Instantiator

## A built-in instantiator and configurator

It arranges the new intances in a standardized and controlled hirachical mode

## Examples

### A 3-level hierarchy Server

```javascript
const path = require('path'),
       JHS = require('node-jhs').instantiator,
      http = require("http"),
        fs = require("fs"),
      host = 'http://localhost',
      port = process.env.PORT || "4000",
      home = host+':'+port+'/';
  
var  flags    = {home: '.', path:'/',querystring:''},
     execJHS  = new JHS({levels:3}),
     options  = {home:home,root:"./wwwroot",method:'GET'},
     server   = http.createServer();

server.listen(port, ()=>{
      console.log(`\t\x1b[0m\x1b[92mListening to Requests\ton \x1b[0m\x1b[93m${home}\x1b[0m`);
});
server.on('request', function(request, response) {
        options.path = request.url;
        options.method = request.method;
        switch(options.method){
          case 'GET':
          var p = options.path.split('?')[0];
          var file = options.root+p;
              p = path.parse(p);
          if(p.ext == '.jhs'){
              execJHS.parse(file,false, options, function(jhsResult, err){  
                response.end(jhsResult);
              });     
          }else {
            try{
              response.end(fs.readFileSync(file));             
            }catch(e){
              execJHS.parse(file,false, options, function(jhsResult, err){  
                response.end(jhsResult);
              });   
          }
        }
          break;
          default:
          break;
         }
  });
```

As you can see, there is only one asynchronous function (the execJHS.parse function), not the hierarchivcall nested ones, because the instantiator nests them for you. A difference between the JHS class members 'intance ' and 'instantiator' is the name of the parser function. For the member 'instance' that function is called 'parseFile', whereas for 'instantiator' it is just 'parse'. Another remarkable differente betwee both members is that in 'instantiator' you can't define delimiters for the new instances, because they are fixed.
