/*****************************JUSTO-TAPIADOR-GARCIA*****************************
 ******* An Example of A Minimalist Secure Web Server (simple-server.js) *******
 *******      With JHS module, a Dynamic HTML pages Middleware Engine    *******
 *****************************JUSTO-TAPIADOR-GARCIA*****************************/
const os   = require('os'),
      path = require('path'),
      url  = require('url'),
       JHS = require('node-jhs').instance;
     https = require("https"),
        fs = require("fs"),
 root_path = path.join(__dirname, 'wwwroot'),
 cert_path = path.join(__dirname, 'cert'),
      host = 'https://localhost',
      port = process.env.PORT || "4000",
      home =	host+':'+port+'/';
  
var  flags    = {home: '.', path:'/',querystring:''},
     execJHS = new JHS(),
     options = {home:home,root:"./wwwroot",method:'GET'},
     server   = https.createServer({key: fs.readFileSync(cert_path+"\\key.pem"),cert: fs.readFileSync(cert_path+"\\cert.pem")});

server.listen(port, ()=>{
      console.log(
`\t\x1b[97m${os.hostname()}\x1b[0m (\x1b[90mOperating System\x1b[0m)
\tis running \x1b[91mThis webServer
\t\x1b[0m\x1b[92mwhich Listens to Requests
\ton \x1b[0m\x1b[93m${home}\x1b[0m`
          );
});

server.on('request', function(request, response) {
        const queryObject = url.parse(request.url, true).query;		
        options.path = request.url;
        options.method = request.method;
        
        switch(options.method){
          case 'GET':
          var p = options.path.split('?')[0];
          var file = options.root+p;
              p = path.parse(p);
              options.scriptname = file;
          if(p.ext == '.jhs'){
              execJHS.parseFile(file,false, options, function(jhsResult, err){  
                response.end(jhsResult);
              });     
          }else {
            try{
              response.end(fs.readFileSync(file));             
            }catch(e){
              file = options.root+'/index.jhs';
              options.scriptname = file;
              execJHS.parseFile(file,false, options, function(jhsResult, err){  
                response.end(jhsResult);
              }); 
          }
        }
          break;
          default:
          break;
         }
  });