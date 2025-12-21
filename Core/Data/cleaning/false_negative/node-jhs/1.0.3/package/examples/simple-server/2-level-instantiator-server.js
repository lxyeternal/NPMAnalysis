/*
const credits = {
  author:'Justo Tapiador García',
  mail:'justo.tapiador@yahoo.com',
  scriptname:'2-level-server.js',           
  desription: ' Example of Minimalist Secure Web Server' +
              ' With JHS module, a Dynamic HTML pages Middleware Engine'+
              ' configured with a 2-level hierarchical instanciator'
}
*/
const os   = require('os'),
      path = require('path'),
      url  = require('url'),
       JHS = require('node-jhs').instantiator;
     https = require("https"),
        fs = require("fs"),
 root_path = path.join(__dirname, 'wwwroot'),
 cert_path = path.join(__dirname, 'cert'),
      host = 'https://localhost',
      port = process.env.PORT || "4000",
      home =	host+':'+port+'/',
      filename =__filename.split('\\').slice(-1)[0].split('.')[0];
  
var  flags    = {home: '.', path:'/',querystring:''},
     execJHS = new JHS({levels:3}),
     options = {home:home,root:"./wwwroot",method:'GET'},
     server   = https.createServer({key: fs.readFileSync(cert_path+"\\key.pem"),cert: fs.readFileSync(cert_path+"\\cert.pem")});

     execJHS.banModules(1,['bitcore-lib']);

    

server.listen(port, ()=>{
      console.log(
`\t\x1b[97m${os.hostname()}\x1b[0m (\x1b[90mOperating System\x1b[0m)
\tis running \x1b[91mThis '${filename}
\t\x1b[0m\x1b[92mwhich Listens to Requests
\ton \x1b[0m\x1b[93m${home}\x1b[0m`
          );
  console.log('JHS Instantiator',execJHS.getInfo());
  //console.log('credits',credits);
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
              execJHS.parse(file,false, options, function(jhsResult, err){  
                    response.end(jhsResult);
                  
              });     
          }else {
            try{
              response.end(fs.readFileSync(file));             
            }catch(e){
              file = options.root+'/index.jhs';
              options.scriptname = file;
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